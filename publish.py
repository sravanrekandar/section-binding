#!/usr/bin/env python3
"""
Publishing helper script for pdf-section-binding package.

This script helps automate the publishing process to PyPI.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr}")
        return False


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")

    # Check if dist directory exists and has files
    dist_dir = Path("dist")
    if not dist_dir.exists() or not list(dist_dir.glob("*.whl")):
        print("❌ No built packages found. Run 'python -m build' first.")
        return False

    # Check if tests pass
    if not run_command("python -m pytest", "Running tests"):
        return False

    # Check linting
    if not run_command(
        "python -m pylint src/pdf_section_binding/", "Checking code quality"
    ):
        return False

    print("✅ All prerequisites met")
    return True


def publish_to_testpypi():
    """Publish to TestPyPI."""
    print("\n📦 Publishing to TestPyPI...")
    cmd = "python -m twine upload --repository testpypi dist/*"
    return run_command(cmd, "Uploading to TestPyPI")


def publish_to_pypi():
    """Publish to PyPI."""
    print("\n📦 Publishing to PyPI...")

    # Confirm with user
    response = input(
        "Are you sure you want to publish to PyPI? This cannot be undone. (yes/no): "
    )
    if response.lower() != "yes":
        print("❌ Publishing cancelled")
        return False

    cmd = "python -m twine upload dist/*"
    return run_command(cmd, "Uploading to PyPI")


def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    import shutil

    for path in ["build", "dist", "src/pdf_section_binding.egg-info"]:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"   Removed {path}")

    print("✅ Build artifacts cleaned")


def build_package():
    """Build the package."""
    return run_command("python -m build", "Building package")


def main():
    """Main publishing workflow."""
    print("🚀 PDF Section Binding Publishing Helper")
    print("=" * 50)

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
    else:
        print("\nChoose an action:")
        print("1. Build package")
        print("2. Check package")
        print("3. Publish to TestPyPI")
        print("4. Publish to PyPI")
        print("5. Clean build artifacts")
        print("6. Full workflow (build + check + testpypi)")

        choice = input("\nEnter choice (1-6): ").strip()
        action_map = {
            "1": "build",
            "2": "check",
            "3": "testpypi",
            "4": "pypi",
            "5": "clean",
            "6": "workflow",
        }
        action = action_map.get(choice, "help")

    if action == "build":
        clean_build()
        build_package()

    elif action == "check":
        if not run_command("python -m twine check dist/*", "Checking package"):
            sys.exit(1)

    elif action == "testpypi":
        if not check_prerequisites():
            sys.exit(1)
        publish_to_testpypi()

    elif action == "pypi":
        if not check_prerequisites():
            sys.exit(1)
        publish_to_pypi()

    elif action == "clean":
        clean_build()

    elif action == "workflow":
        print("🔄 Running full workflow...")
        clean_build()
        if not build_package():
            sys.exit(1)
        if not check_prerequisites():
            sys.exit(1)
        if not run_command("python -m twine check dist/*", "Final package check"):
            sys.exit(1)
        print("\n🎉 Package is ready for publishing!")
        print("\nNext steps:")
        print("1. Test on TestPyPI: python publish.py testpypi")
        print("2. If all looks good: python publish.py pypi")

    else:
        print("Usage: python publish.py [build|check|testpypi|pypi|clean|workflow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
