#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Monitors a drop folder for new files.

This is the Bronze Tier watcher - it monitors a folder for new files
and creates action files in the Needs_Action folder for Claude to process.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder

Or with defaults:
    python filesystem_watcher.py

Default drop folder: <vault>/Inbox
Default check interval: 30 seconds
"""

import sys
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """
    Watches a folder for new files and creates action items.
    
    Use cases:
    - Drop PDFs for summarization
    - Drop images for OCR/description
    - Drop documents for processing
    - Drop data files for analysis
    """
    
    def __init__(self, vault_path: str, drop_folder: Optional[str] = None, 
                 check_interval: int = 30):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            drop_folder: Folder to watch (default: <vault>/Inbox)
            check_interval: Seconds between checks (default: 30)
        """
        super().__init__(vault_path, check_interval)
        
        self.drop_folder = Path(drop_folder) if drop_folder else self.inbox
        self.hash_log = self.vault_path / 'scripts' / 'filesystem_hashes.log'
        
        # Ensure drop folder exists
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Load processed file hashes
        self.processed_hashes = self._load_hashes()
        
        self.logger.info(f'Watching folder: {self.drop_folder}')
    
    def _load_hashes(self) -> set:
        """Load set of processed file hashes."""
        if self.hash_log.exists():
            try:
                with open(self.hash_log, 'r') as f:
                    return set(line.strip() for line in f if line.strip())
            except Exception as e:
                self.logger.warning(f'Could not load hashes: {e}')
        return set()
    
    def _save_hash(self, file_hash: str):
        """Save a file hash to the processed log."""
        try:
            with open(self.hash_log, 'a') as f:
                f.write(f'{file_hash}\n')
            self.processed_hashes.add(file_hash)
        except Exception as e:
            self.logger.error(f'Failed to save hash: {e}')
    
    def _get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _get_file_size_human(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f'{size_bytes:.1f} {unit}'
            size_bytes /= 1024
        return f'{size_bytes:.1f} TB'
    
    def _determine_priority(self, filepath: Path) -> str:
        """Determine priority based on filename patterns."""
        name_lower = filepath.name.lower()
        
        # Urgent patterns
        urgent_keywords = ['urgent', 'asap', 'emergency', 'immediate', 'priority']
        if any(kw in name_lower for kw in urgent_keywords):
            return 'urgent'
        
        # High priority patterns
        high_keywords = ['invoice', 'payment', 'contract', 'legal', 'tax']
        if any(kw in name_lower for kw in high_keywords):
            return 'high'
        
        return 'normal'
    
    def _get_suggested_actions(self, filepath: Path) -> List[str]:
        """Generate suggested actions based on file type."""
        suffix = filepath.suffix.lower()
        actions = []
        
        # Common actions based on file type
        if suffix in ['.pdf', '.doc', '.docx', '.txt', '.md']:
            actions.append('Read and summarize content')
            actions.append('Extract action items')
            actions.append('File in appropriate category')
        
        elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            actions.append('Describe image content')
            actions.append('Extract any text (OCR)')
            actions.append('Determine if action is needed')
        
        elif suffix in ['.xlsx', '.xls', '.csv']:
            actions.append('Analyze data content')
            actions.append('Generate summary statistics')
            actions.append('Identify trends or issues')
        
        elif suffix in ['.py', '.js', '.ts', '.java', '.cpp']:
            actions.append('Review code')
            actions.append('Check for errors or improvements')
            actions.append('Document functionality')
        
        elif suffix == '.json':
            actions.append('Parse and analyze JSON structure')
            actions.append('Extract relevant data')
        
        elif suffix in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            actions.append('List archive contents')
            actions.append('Extract if needed')
        
        else:
            actions.append('Identify file type and content')
            actions.append('Determine appropriate action')
        
        # Always add these
        actions.append('Move original file to appropriate archive folder')
        actions.append('Update Dashboard.md with progress')
        
        return actions
    
    def check_for_updates(self) -> List[Path]:
        """
        Check drop folder for new files.
        
        Returns:
            List of new file paths not yet processed
        """
        new_files = []
        
        try:
            # Get all files in drop folder (not subdirectories)
            for filepath in self.drop_folder.iterdir():
                if filepath.is_file():
                    file_hash = self._get_file_hash(filepath)
                    
                    if not self._is_processed(file_hash):
                        new_files.append(filepath)
                        
        except Exception as e:
            self.logger.error(f'Error scanning drop folder: {e}')
        
        return new_files
    
    def create_action_file(self, filepath: Path) -> Optional[Path]:
        """
        Create action file for a dropped file.
        
        Args:
            filepath: Path to the new file
        
        Returns:
            Path to created action file
        """
        try:
            # Calculate file hash for tracking
            file_hash = self._get_file_hash(filepath)
            
            # Get file info
            file_size = self._get_file_size_human(filepath.stat().st_size)
            modified = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            priority = self._determine_priority(filepath)
            
            # Build content
            content = f'''## File Information

- **Original Name:** {filepath.name}
- **Size:** {file_size}
- **Type:** {filepath.suffix.upper()}
- **Dropped:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Last Modified:** {modified}
- **Location:** `{filepath}`

## Content Summary

*Awaiting AI analysis*

## Processing Notes

- File hash: `{file_hash}`
- Auto-detected priority: {priority.upper()}
'''
            
            # Get suggested actions
            suggested_actions = self._get_suggested_actions(filepath)
            
            # Create filename (sanitize original name)
            safe_name = filepath.stem.replace(' ', '_').replace('-', '_')[:50]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'FILE_DROP_{safe_name}_{timestamp}'
            
            # Create metadata
            metadata = {
                'original_name': filepath.name,
                'file_size': file_size,
                'file_type': filepath.suffix.upper(),
                'file_hash': file_hash,
                'drop_location': str(filepath)
            }
            
            # Create the action file
            action_file = self._create_standard_action_file(
                item_type='file_drop',
                source='filesystem',
                content=content,
                suggested_actions=suggested_actions,
                filename=filename,
                priority=priority,
                metadata=metadata
            )
            
            # Mark file as processed
            self._save_hash(file_hash)
            
            self.logger.info(f'Created action file for: {filepath.name}')
            return action_file
            
        except Exception as e:
            self.logger.error(f'Failed to create action file for {filepath}: {e}')
            return None


def main():
    """Run the file system watcher."""
    # Default paths
    vault_path = Path(__file__).parent.parent
    drop_folder = vault_path / 'Inbox'
    
    # Allow command line override
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        drop_folder = Path(sys.argv[2])
    
    print(f'=== File System Watcher ===')
    print(f'Vault: {vault_path}')
    print(f'Drop Folder: {drop_folder}')
    print(f'Press Ctrl+C to stop\n')
    
    watcher = FileSystemWatcher(
        vault_path=str(vault_path),
        drop_folder=str(drop_folder),
        check_interval=30
    )
    
    watcher.run()


if __name__ == '__main__':
    main()
