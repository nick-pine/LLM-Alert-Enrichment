#!/usr/bin/env python3
"""
Cleanup script to remove old duplicate directories after migration.
Only runs after verifying the new structure works.
"""
import os
import sys
import shutil
from pathlib import Path

def main():
    """Remove old duplicate directories safely."""
    base_dir = Path(__file__).parent.parent  # Go up from scripts/ to root
    
    # Add the project root to Python path for imports
    sys.path.insert(0, str(base_dir))
    
    print("🧹 Cleaning up old duplicate directories...")
    
    # Test that new structure works first
    try:
        print("Testing new structure...")
        
        # Test schema imports
        from src.schemas import WazuhAlertInput, EnrichedAlertOutput
        print("✅ Schema imports work")
        
        # Test provider imports  
        from src.providers.ollama import query_ollama
        print("✅ Provider imports work")
        
        # Test core imports
        from src.core.logger import log
        print("✅ Core imports work")
        
    except Exception as e:
        print(f"❌ New structure has issues: {e}")
        print("Aborting cleanup to prevent breaking the code!")
        return
    
    # If tests pass, proceed with cleanup
    directories_to_remove = [
        "core",
        "providers", 
        "api",
        "schemas"
    ]
    
    for directory in directories_to_remove:
        dir_path = base_dir / directory
        if dir_path.exists():
            print(f"Removing old {directory}/ directory...")
            shutil.rmtree(str(dir_path))
            print(f"✅ Removed {directory}/")
        else:
            print(f"ℹ️  {directory}/ already removed")
    
    # Also clean up old test file (we moved it to scripts/)
    old_test_file = base_dir / "test_enrichment.py"
    if old_test_file.exists():
        print("Removing old test_enrichment.py (moved to scripts/)...")
        old_test_file.unlink()
        print("✅ Removed old test_enrichment.py")
    
    print("\\n🎉 Cleanup completed successfully!")
    print("The old duplicate directories have been removed.")
    print("Your code is now using the clean new src/ structure.")

if __name__ == "__main__":
    main()
