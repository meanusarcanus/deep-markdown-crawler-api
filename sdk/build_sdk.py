#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def main():
    sdk_dir = Path(__file__).parent.resolve()
    print("=" * 60)
    print(" 📦 BUILDING DEEP MARKDOWN CRAWLER PYPI PACKAGE")
    print("=" * 60)

    for item in ["build", "dist", "deep_markdown_crawler.egg-info"]:
        path = sdk_dir / item
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"✓ Removed old directory: {item}")

    print("\n[Step 1] Building distribution files...")
    subprocess.run(["python3", "setup.py", "sdist", "bdist_wheel"], cwd=sdk_dir, check=True)

    print("\n[Step 2] Validating package metadata with twine...")
    subprocess.run(["twine", "check", "dist/*"], cwd=sdk_dir, check=True)

    print("\n" + "=" * 60)
    print(" 🚀 READY TO UPLOAD TO PYPI!")
    print(" Run command: twine upload dist/*")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
