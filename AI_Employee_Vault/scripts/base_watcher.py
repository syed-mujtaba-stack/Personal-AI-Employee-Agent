#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Watcher - Abstract base class for all watcher scripts.

Watchers are lightweight Python scripts that run continuously in the background,
monitoring various inputs (Gmail, WhatsApp, filesystems) and creating actionable
.md files in the /Needs_Action folder for Claude Code to process.

All custom watchers should inherit from this base class and implement:
- check_for_updates(): Return list of new items to process
- create_action_file(item): Create .md file in Needs_Action folder
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher implementations.
    
    Provides common functionality:
    - Logging setup
    - Vault path management
    - Action file creation with standard format
    - Error handling and recovery
    - Processed item tracking
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.processed_log = self.vault_path / 'scripts' / f'{self.__class__.__name__}_processed.log'
        self.check_interval = check_interval
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Track processed items to avoid duplicates
        self.processed_ids = self._load_processed_ids()
        
        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f'{self.__class__.__name__} initialized for vault: {vault_path}')
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging to file and console."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = self.vault_path / 'scripts' / f'{self.__class__.__name__}.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        return logger
    
    def _load_processed_ids(self) -> set:
        """Load set of previously processed item IDs."""
        if self.processed_log.exists():
            try:
                with open(self.processed_log, 'r') as f:
                    return set(line.strip() for line in f if line.strip())
            except Exception as e:
                self.logger.warning(f'Could not load processed IDs: {e}')
        return set()
    
    def _save_processed_id(self, item_id: str):
        """Save a processed item ID to the log."""
        try:
            self.processed_log.parent.mkdir(parents=True, exist_ok=True)
            with open(self.processed_log, 'a') as f:
                f.write(f'{item_id}\n')
            self.processed_ids.add(item_id)
        except Exception as e:
            self.logger.error(f'Failed to save processed ID: {e}')
    
    def _is_processed(self, item_id: str) -> bool:
        """Check if an item has already been processed."""
        return item_id in self.processed_ids
    
    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new items to process.
        
        Returns:
            List of new items (format depends on watcher type)
        
        Example for Gmail:
            [{'id': 'msg123', 'snippet': '...', 'from': '...'}]
        
        Example for FileSystem:
            [Path('/path/to/new/file.pdf')]
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create a .md action file in the Needs_Action folder.
        
        Args:
            item: Item returned from check_for_updates()
        
        Returns:
            Path to created file, or None if creation failed
        
        The action file should follow this format:
        ---
        type: <item_type>
        source: <source_system>
        created: <ISO timestamp>
        priority: <low|normal|high|urgent>
        status: pending
        ---
        
        ## Content
        <item content>
        
        ## Suggested Actions
        - [ ] <action 1>
        - [ ] <action 2>
        """
        pass
    
    def _create_standard_action_file(self, item_type: str, source: str, 
                                      content: str, suggested_actions: List[str],
                                      filename: str, priority: str = 'normal',
                                      metadata: Optional[dict] = None) -> Path:
        """
        Helper to create a standard-formatted action file.
        
        Args:
            item_type: Type of item (email, file_drop, message, etc.)
            source: Source system (gmail, whatsapp, filesystem, etc.)
            content: Main content of the action file
            suggested_actions: List of checkbox actions
            filename: Base filename (without .md extension)
            priority: low, normal, high, or urgent
            metadata: Additional frontmatter fields
        
        Returns:
            Path to created file
        """
        # Build frontmatter
        frontmatter = {
            'type': item_type,
            'source': source,
            'created': datetime.now().isoformat(),
            'priority': priority,
            'status': 'pending'
        }
        
        # Add custom metadata
        if metadata:
            frontmatter.update(metadata)
        
        # Format frontmatter as YAML
        frontmatter_text = '---\n'
        for key, value in frontmatter.items():
            frontmatter_text += f'{key}: {value}\n'
        frontmatter_text += '---\n\n'
        
        # Build suggested actions section
        actions_text = '## Suggested Actions\n\n'
        for action in suggested_actions:
            if not action.strip().startswith('- [ ]'):
                actions_text += f'- [ ] {action}\n'
            else:
                actions_text += f'{action}\n'
        
        # Combine all parts
        full_content = f'{frontmatter_text}{content}\n\n{actions_text}'
        
        # Write file
        filepath = self.needs_action / f'{filename}.md'
        filepath.write_text(full_content, encoding='utf-8')
        
        self.logger.info(f'Created action file: {filepath.name}')
        return filepath
    
    def run(self):
        """
        Main watcher loop.
        
        Continuously checks for updates and creates action files.
        Runs until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__} (interval: {self.check_interval}s)')
        
        try:
            while True:
                try:
                    # Check for new items
                    items = self.check_for_updates()
                    
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        
                        for item in items:
                            try:
                                self.create_action_file(item)
                            except Exception as e:
                                self.logger.error(f'Failed to create action file: {e}')
                    else:
                        self.logger.debug('No new items')
                    
                except Exception as e:
                    self.logger.error(f'Error in check loop: {e}')
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Watcher crashed: {e}')
            raise


def main():
    """Example usage - this should be overridden by subclasses."""
    print("BaseWatcher is an abstract class. Create a subclass to use.")
    print("\nExample subclass:")
    print("""
class MyWatcher(BaseWatcher):
    def check_for_updates(self):
        # Return list of new items
        return []
    
    def create_action_file(self, item):
        # Create .md file in Needs_Action
        return self._create_standard_action_file(...)
""")


if __name__ == '__main__':
    main()
