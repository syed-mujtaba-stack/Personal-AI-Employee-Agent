#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Verification Script

Verifies all Bronze Tier deliverables are complete and functional:
1. Obsidian vault with Dashboard.md and Company_Handbook.md
2. One working Watcher script (File System Monitor)
3. Claude Code integration ready
4. Basic folder structure: /Inbox, /Needs_Action, /Done
5. Agent skill documentation (SKILL.md)

Usage:
    python verify_bronze_tier.py /path/to/vault

Or with defaults:
    python verify_bronze_tier.py
"""

import sys
from pathlib import Path
from typing import List, Tuple


class BronzeTierVerifier:
    """Verifies Bronze Tier deliverables."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.results: List[Tuple[str, bool, str]] = []
    
    def check(self, name: str, condition: bool, message: str = ""):
        """Record a check result."""
        self.results.append((name, condition, message))
        status = "✓" if condition else "✗"
        print(f"  {status} {name}")
        if message and not condition:
            print(f"    → {message}")
    
    def verify(self) -> bool:
        """Run all verification checks."""
        print("\n=== Bronze Tier Verification ===")
        print(f"Vault: {self.vault_path}\n")
        
        print("1. Required Files:")
        self.check_file_exists("Dashboard.md", self.vault_path / "Dashboard.md")
        self.check_file_exists("Company_Handbook.md", self.vault_path / "Company_Handbook.md")
        self.check_file_exists("Business_Goals.md", self.vault_path / "Business_Goals.md")
        
        print("\n2. Folder Structure:")
        self.check_folder_exists("Inbox", self.vault_path / "Inbox")
        self.check_folder_exists("Needs_Action", self.vault_path / "Needs_Action")
        self.check_folder_exists("Done", self.vault_path / "Done")
        self.check_folder_exists("Plans", self.vault_path / "Plans")
        self.check_folder_exists("Pending_Approval", self.vault_path / "Pending_Approval")
        self.check_folder_exists("Approved", self.vault_path / "Approved")
        self.check_folder_exists("Accounting", self.vault_path / "Accounting")
        self.check_folder_exists("Briefings", self.vault_path / "Briefings")
        
        print("\n3. Watcher Scripts:")
        self.check_file_exists("base_watcher.py", self.vault_path / "scripts" / "base_watcher.py")
        self.check_file_exists("filesystem_watcher.py", self.vault_path / "scripts" / "filesystem_watcher.py")
        self.check_file_exists("orchestrator.py", self.vault_path / "scripts" / "orchestrator.py")
        
        print("\n4. Documentation:")
        self.check_file_exists("SKILL.md", self.vault_path / "scripts" / "SKILL.md")
        self.check_file_exists("README.md", self.vault_path / "README.md")
        self.check_file_exists("requirements.txt", self.vault_path / "scripts" / "requirements.txt")
        
        print("\n5. Functional Tests:")
        self.check_watcher_functional()
        
        print("\n" + "=" * 40)
        self.print_summary()
        
        return all(result[1] for result in self.results)
    
    def check_file_exists(self, name: str, path: Path):
        """Check if a required file exists."""
        exists = path.exists()
        message = f"Expected at: {path}" if not exists else ""
        self.check(name, exists, message)
    
    def check_folder_exists(self, name: str, path: Path):
        """Check if a required folder exists."""
        exists = path.exists() and path.is_dir()
        message = f"Expected at: {path}" if not exists else ""
        self.check(name, exists, message)
    
    def check_watcher_functional(self):
        """Check if the watcher has created any action files."""
        needs_action = self.vault_path / "Needs_Action"
        action_files = list(needs_action.glob("*.md")) if needs_action.exists() else []
        
        has_action_files = len(action_files) > 0
        message = f"Found {len(action_files)} action file(s)" if has_action_files else "No action files yet (drop a file in Inbox to test)"
        self.check("Watcher creates action files", has_action_files, message)
    
    def print_summary(self):
        """Print verification summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r[1])
        failed = total - passed
        
        print(f"\nResults: {passed}/{total} checks passed")
        
        if failed == 0:
            print("\n🎉 Bronze Tier Verification PASSED!")
            print("\nYour AI Employee foundation is ready.")
            print("\nNext steps:")
            print("  1. Drop a file in Inbox/ to test the watcher")
            print("  2. Run: python scripts/orchestrator.py")
            print("  3. Review processed items in Done/")
        else:
            print(f"\n⚠️ {failed} check(s) failed. Please review the issues above.")
            print("\nTo complete Bronze Tier, ensure all required files and folders exist.")


def main():
    """Run verification."""
    # Default vault path (parent of scripts directory)
    vault_path = Path(__file__).parent.parent
    
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    verifier = BronzeTierVerifier(vault_path)
    success = verifier.verify()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
