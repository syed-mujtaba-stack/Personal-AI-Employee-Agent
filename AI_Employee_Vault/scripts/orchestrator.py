#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Processes items in Needs_Action folder and invokes Qwen Code.

This script:
1. Scans /Needs_Action for pending action files
2. Invokes Qwen Code to process each item
3. Tracks completion and moves files to /Done
4. Updates Dashboard.md with progress

Usage:
    python orchestrator.py /path/to/vault

Or with defaults (vault is parent of scripts folder):
    python orchestrator.py
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple


class Orchestrator:
    """
    Orchestrates the AI Employee workflow.

    Coordinates between:
    - Watchers (creating action files)
    - Qwen Code (processing items)
    - File system (moving files between states)
    - Dashboard (updating status)
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.processing_log = self.vault_path / 'scripts' / 'orchestrator.log'
        
        # Ensure directories exist
        self.done.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging to file."""
        import logging
        self.processing_log.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger('Orchestrator')
        self.logger.setLevel(logging.INFO)

        # Clear existing handlers
        self.logger.handlers = []

        # File handler (UTF-8 encoding)
        file_handler = logging.FileHandler(self.processing_log, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

        # Console handler (UTF-8 encoding for Windows compatibility)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_format)
        # Set UTF-8 encoding for console output
        console_handler.stream = open(1, 'w', encoding='utf-8', closefd=False)
        self.logger.addHandler(console_handler)
    
    def get_pending_files(self) -> List[Path]:
        """
        Get all pending action files in Needs_Action folder.
        
        Returns:
            List of .md files sorted by priority (urgent first)
        """
        pending = []
        
        try:
            for filepath in self.needs_action.iterdir():
                if filepath.suffix == '.md' and filepath.is_file():
                    # Check if already being processed
                    if not self._is_processing(filepath):
                        pending.append(filepath)
        except Exception as e:
            self.logger.error(f'Error scanning Needs_Action: {e}')
        
        # Sort by priority (urgent > high > normal > low)
        priority_order = {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}
        
        def get_priority(filepath: Path) -> int:
            content = filepath.read_text(encoding='utf-8')
            match = re.search(r'priority:\s*(\w+)', content)
            if match:
                return priority_order.get(match.group(1), 2)
            return 2
        
        return sorted(pending, key=get_priority)
    
    def _is_processing(self, filepath: Path) -> bool:
        """Check if a file is currently being processed."""
        # Could implement file locking or in-progress tracking here
        return False
    
    def _read_frontmatter(self, filepath: Path) -> dict:
        """Extract YAML frontmatter from a file."""
        content = filepath.read_text(encoding='utf-8')
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        
        if match:
            frontmatter = {}
            for line in match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            return frontmatter
        return {}
    
    def _update_dashboard(self, processed: int, pending: int, errors: int):
        """Update Dashboard.md with current stats."""
        try:
            if not self.dashboard.exists():
                self.logger.warning('Dashboard.md not found')
                return
            
            content = self.dashboard.read_text(encoding='utf-8')
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            # Update stats table
            content = re.sub(
                r'\| Pending Tasks \|.*\|',
                f'| Pending Tasks | {pending} | ➖ |',
                content
            )
            content = re.sub(
                r'\| Completed Today \|.*\|',
                f'| Completed Today | {processed} | ⬆️ |',
                content
            )
            
            # Update inbox status
            content = re.sub(
                r'- \*\*Needs Action:\*\* \d+ items',
                f'- **Needs Action:** {pending} items',
                content
            )
            
            # Update last sync
            content = re.sub(
                r'Last sync:.*',
                f'Last sync: {timestamp}',
                content
            )
            
            # Update quick stats section with processed count
            if processed > 0:
                activity_line = f'\n- [{timestamp}] Processed {processed} item(s)\n'
                # Insert after "Recent Activity" header
                content = re.sub(
                    r'(## 📝 Recent Activity\n)',
                    f'\\1{activity_line}',
                    content
                )
            
            self.dashboard.write_text(content, encoding='utf-8')
            self.logger.info('Dashboard updated')
            
        except Exception as e:
            self.logger.error(f'Failed to update dashboard: {e}')
    
    def _invoke_qwen(self, action_file: Path) -> Tuple[bool, str]:
        """
        Invoke Qwen Code to process an action file.

        Args:
            action_file: Path to the action file to process

        Returns:
            Tuple of (success: bool, summary: str)
        """
        self.logger.info(f'Processing: {action_file.name}')

        # Read the action file
        content = action_file.read_text(encoding='utf-8')
        frontmatter = self._read_frontmatter(action_file)

        # Build the prompt for Qwen
        item_type = frontmatter.get('type', 'unknown')
        priority = frontmatter.get('priority', 'normal')

        prompt = f'''You are the AI Employee. Process the following action file.

**Action File:** {action_file.name}
**Type:** {item_type}
**Priority:** {priority}

**Your Tasks:**
1. Read and understand the content below
2. Perform the suggested actions
3. Update the Dashboard.md with progress
4. When complete, move this file to /Done folder

**Rules from Company Handbook:**
- Always be transparent about actions taken
- Flag payments over $500 for approval
- Response time target: <24 hours
- Log all actions

---
{content}
---

**Instructions:**
1. Analyze the request above
2. Take appropriate actions (read files, analyze content, etc.)
3. Write a summary of what you found/did
4. Update checkboxes with [x] for completed items
5. When ALL actions are complete, output: <promise>TASK_COMPLETE</promise>

Start by acknowledging the task and creating a brief plan.'''

        try:
            # Invoke Qwen Code
            # Note: This requires Qwen Code to be installed and configured
            # Use shell=True on Windows to inherit full PATH
            result = subprocess.run(
                ['qwen', '--prompt', prompt],
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
                shell=True,   # Enable shell to find qwen.cmd on Windows
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            output = result.stdout + result.stderr

            # Check for completion signal
            if '<promise>TASK_COMPLETE</promise>' in output:
                return True, 'Task completed successfully'
            elif result.returncode == 0:
                return True, 'Processed (check output for details)'
            else:
                error_msg = result.stderr[:200] if result.stderr else f'Exit code: {result.returncode}'
                return False, f'Qwen error: {error_msg}'

        except subprocess.TimeoutExpired:
            return False, 'Timeout - task took too long'
        except FileNotFoundError as e:
            self.logger.warning(f'FileNotFoundError: {e}')
            # Try with full path detection
            try:
                # Try using 'where' to find qwen
                where_result = subprocess.run(
                    ['where', 'qwen'],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                if where_result.returncode == 0:
                    qwen_path = where_result.stdout.strip().split('\n')[0].strip()
                    self.logger.info(f'Found qwen at: {qwen_path}')
                    return False, f'Qwen Code found at {qwen_path} but failed to execute. Try running manually: qwen --prompt "test"'
            except:
                pass
            return False, 'Qwen Code not found in PATH. Run "where qwen" to diagnose.'
        except Exception as e:
            return False, f'Error: {str(e)}'
    
    def process_file(self, action_file: Path) -> bool:
        """
        Process a single action file.

        Args:
            action_file: Path to the action file

        Returns:
            True if processing succeeded
        """
        self.logger.info(f'=== Processing: {action_file.name} ===')

        # Invoke Qwen Code
        success, summary = self._invoke_qwen(action_file)
        
        if success:
            # Move to Done folder
            done_folder = self.done / datetime.now().strftime('%Y-%m-%d')
            done_folder.mkdir(parents=True, exist_ok=True)

            dest = done_folder / action_file.name
            action_file.rename(dest)

            self.logger.info(f'[OK] Moved to: {dest}')
            self.logger.info(f'Summary: {summary}')
        else:
            self.logger.error(f'[ERROR] Failed: {summary}')
        
        return success
    
    def run_once(self) -> Tuple[int, int]:
        """
        Process all pending files once.
        
        Returns:
            Tuple of (processed_count, error_count)
        """
        pending = self.get_pending_files()
        
        if not pending:
            self.logger.info('No pending items to process')
            return 0, 0
        
        self.logger.info(f'Found {len(pending)} pending item(s)')
        
        processed = 0
        errors = 0
        
        for action_file in pending:
            if self.process_file(action_file):
                processed += 1
            else:
                errors += 1
        
        # Update dashboard
        remaining = len(pending) - processed
        self._update_dashboard(processed, remaining, errors)
        
        return processed, errors
    
    def run_continuous(self, check_interval: int = 300):
        """
        Run orchestrator continuously.
        
        Args:
            check_interval: Seconds between processing runs (default: 5 minutes)
        """
        import time
        
        self.logger.info(f'Starting Orchestrator (interval: {check_interval}s)')
        self.logger.info('Press Ctrl+C to stop\n')
        
        try:
            while True:
                processed, errors = self.run_once()
                
                if processed > 0 or errors > 0:
                    self.logger.info(f'Run complete: {processed} processed, {errors} errors\n')
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('\nOrchestrator stopped by user')


def main():
    """Run the orchestrator."""
    # Default vault path (parent of scripts folder)
    vault_path = Path(__file__).parent.parent
    
    # Allow command line override
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    
    print('=== AI Employee Orchestrator ===')
    print(f'Vault: {vault_path}')
    print(f'Watching: {vault_path / "Needs_Action"}')
    print(f'Mode: Run once (use --continuous for continuous mode)\n')
    
    orchestrator = Orchestrator(str(vault_path))
    
    # Check for --continuous flag
    if len(sys.argv) > 2 and sys.argv[2] == '--continuous':
        orchestrator.run_continuous(check_interval=300)
    else:
        # Run once
        processed, errors = orchestrator.run_once()
        print(f'\n=== Summary ===')
        print(f'Processed: {processed}')
        print(f'Errors: {errors}')


if __name__ == '__main__':
    main()
