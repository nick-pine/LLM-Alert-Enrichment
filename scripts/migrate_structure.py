#!/usr/bin/env python3
"""
Migration script to reorganize the LLM Alert Enrichment codebase.
Moves files to the new src/ directory structure and updates imports.
"""
import os
import shutil
from pathlib import Path

def create_directory_if_not_exists(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def move_file_if_exists(src, dst):
    """Move file if source exists."""
    if os.path.exists(src):
        create_directory_if_not_exists(os.path.dirname(dst))
        shutil.move(src, dst)
        print(f"Moved: {src} -> {dst}")
    else:
        print(f"Not found: {src}")

def main():
    """Execute the migration."""
    base_dir = Path(__file__).parent
    
    print("Starting directory restructuring...")
    
    # Create new directory structure
    directories = [
        "src/api",
        "src/core", 
        "src/providers",
        "src/schemas",
        "tests",
        "scripts",
        "config"
    ]
    
    for directory in directories:
        create_directory_if_not_exists(base_dir / directory)
    
    # Move files to new locations
    moves = [
        # Move core files
        ("core/debug.py", "src/core/debug.py"),
        ("core/engine.py", "src/core/engine.py"),
        ("core/io.py", "src/core/io.py"),
        ("core/logger.py", "src/core/logger.py"),
        ("core/preprocessing.py", "src/core/preprocessing.py"),
        ("core/utils.py", "src/core/utils.py"),
        ("core/wazuh_alert_schema.py", "src/core/wazuh_alert_schema.py"),
        ("core/yara_integration.py", "src/core/yara_integration.py"),
        
        # Move providers
        ("providers/ollama.py", "src/providers/ollama.py"),
        
        # Move API files
        ("api/api_server.py", "src/api/server.py"),
        ("api/api_schema.py", "src/api/schema.py"),
        
        # Move schemas (consolidate into unified)
        ("schemas/unified.py", "src/schemas/__init__.py"),
        
        # Move config (if we created separate settings.py)
        ("config/settings.py", "config/settings.py") if os.path.exists("config/settings.py") else None,
        
        # Move utility scripts
        ("test_enrichment.py", "scripts/test_enrichment.py"),
        
        # Main entry point stays at root level
        # ("llm_enrichment.py", "main.py"),
    ]
    
    for move in moves:
        if move is not None:
            src, dst = move
            src_path = base_dir / src
            dst_path = base_dir / dst
            move_file_if_exists(str(src_path), str(dst_path))
    
    print("\\nDirectory restructuring completed!")
    print("\\nNext steps:")
    print("1. Update import statements in moved files")
    print("2. Update any hardcoded paths")
    print("3. Test the application")
    print("4. Remove empty directories")

if __name__ == "__main__":
    main()
