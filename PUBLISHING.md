# Publishing to PyPI Guide

This guide walks you through publishing the `pdf-section-binding` package to PyPI.

## 🚀 Quick Publishing Reference

### Essential Commands (Copy & Paste Ready)

```bash
# 1. Clean and build
rm -rf dist/ build/ *.egg-info/
python -m build

# 2. Check package
python -m twine check dist/*

# 3. Test on TestPyPI first
python -m twine upload --repository testpypi dist/*

# 4. Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-section-binding

# 5. If everything works, publish to PyPI
python -m twine upload dist/*
```

### Authentication for twine uploads
- **Username**: `__token__`
- **Password**: Your API token (starts with `pypi-`)

### Quick Pre-flight Checklist
- [ ] Tests pass: `python -m pytest`
- [ ] Linting clean: `python -m pylint src/pdf_section_binding/`
- [ ] Version updated in `src/pdf_section_binding/version.py`
- [ ] Author info updated in `setup.py` and `pyproject.toml`
- [ ] GitHub URLs updated in `setup.py`
- [ ] Package builds: `python -m build`
- [ ] Package validates: `python -m twine check dist/*`

### Helper Script Commands
```bash
python publish.py workflow          # Full build + check workflow
python publish.py testpypi          # Publish to TestPyPI
python publish.py pypi              # Publish to PyPI
python publish.py clean             # Clean build artifacts
```

---

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. **API Tokens**: For secure publishing, create API tokens:
   - Go to Account Settings → API tokens
   - Create a token with "Entire account" scope
   - Save the token securely (you'll need it later)

## Step 1: Pre-Publishing Checklist

Before publishing, ensure everything is ready:

### 1.1 Update Package Information

Edit these files with your actual information:

**setup.py**:
```python
url="https://github.com/YOURUSERNAME/pdf-section-binding",
project_urls={
    "Bug Reports": "https://github.com/YOURUSERNAME/pdf-section-binding/issues",
    "Source": "https://github.com/YOURUSERNAME/pdf-section-binding",
    "Documentation": "https://github.com/YOURUSERNAME/pdf-section-binding#readme",
},
```

**pyproject.toml**:
```toml
authors = [
    {name = "Your Real Name", email = "your.email@example.com"},
]
```

**src/pdf_section_binding/version.py**:
```python
__author__ = "Your Real Name"
__email__ = "your.email@example.com"
```

### 1.2 Version Management

Update version in `src/pdf_section_binding/version.py`:
```python
__version__ = "1.0.0"  # Use semantic versioning
```

### 1.3 Quality Checks

Run these commands to ensure quality:

```bash
# Run tests
pytest

# Check linting
pylint src/pdf_section_binding/ tests/

# Check package can be built
python -m build --wheel --sdist

# Check package metadata
twine check dist/*
```

## Step 2: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

This creates:
- `dist/*.whl` - Wheel distribution
- `dist/*.tar.gz` - Source distribution

## Step 3: Test on TestPyPI (Recommended)

### 3.1 Upload to TestPyPI

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: Your TestPyPI API token (starting with `pypi-`)

### 3.2 Test Installation from TestPyPI

```bash
# Create a fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-section-binding

# Test the installation
pdf-section-binding --help
section-binding --version

# Test with a sample file
pdf-section-binding your-test.pdf --dry-run

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

## Step 4: Publish to PyPI

If testing was successful:

```bash
# Upload to PyPI
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token

## Step 5: Verify Publication

1. Check your package page: `https://pypi.org/project/pdf-section-binding/`
2. Test installation: `pip install pdf-section-binding`
3. Verify CLI commands work: `pdf-section-binding --help`

## Step 6: Post-Publication

### 6.1 Tag the Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 6.2 Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Use tag `v1.0.0`
4. Add release notes from CHANGELOG.md

### 6.3 Update Documentation

Update README.md installation instructions:

```markdown
## Installation

Install from PyPI:

```bash
pip install pdf-section-binding
```

## Automation (Optional)

### GitHub Actions

Create `.github/workflows/publish.yml` for automated publishing:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Store your PyPI API token in GitHub Secrets as `PYPI_API_TOKEN`.

## 🔧 Common Issues & Troubleshooting

### Build Issues

**Problem**: `ModuleNotFoundError` during build
**Solution**: 
```bash
pip install build twine
python -m build
```

**Problem**: Package validation fails
**Solution**: Check these files exist and are properly formatted:
- `README.md` (valid Markdown)
- `LICENSE` (MIT license text)
- `setup.py` (no syntax errors)
- `pyproject.toml` (valid TOML)

**Problem**: Version already exists on PyPI
**Solution**: 
1. Update version in `src/pdf_section_binding/version.py`
2. Clean and rebuild: `rm -rf dist/ && python -m build`
3. Upload new version

### Upload Issues

**Problem**: Authentication failed
**Solution**: 
- Double-check API token (should start with `pypi-`)
- Use `__token__` as username, not your PyPI username
- Ensure token has correct permissions

**Problem**: Package name conflict
**Solution**: 
- Choose a different package name in `setup.py` and `pyproject.toml`
- Check availability: `pip search your-new-name` or search PyPI

**Problem**: File size too large
**Solution**: 
- Check `.gitignore` excludes test PDFs and build artifacts
- Remove unnecessary files from package
- Use `MANIFEST.in` to exclude specific files

### Testing Issues

**Problem**: Can't install from TestPyPI
**Solution**: 
```bash
# Use both indexes (TestPyPI + PyPI for dependencies)
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-section-binding
```

**Problem**: CLI commands not found after install
**Solution**: 
- Check `entry_points` in `setup.py`
- Reinstall package: `pip uninstall pdf-section-binding && pip install pdf-section-binding`
- Check PATH includes pip install location

## 📋 Post-Publishing Checklist

### Immediate Actions (After PyPI Upload)

1. **Verify Installation**
   ```bash
   # Test fresh install
   pip install pdf-section-binding
   pdf-section-binding --version
   section-binding --help
   ```

2. **Test Basic Functionality**
   ```bash
   # Create test PDF and process it
   ./create_test_pdf -n 8 -o test.pdf
   pdf-section-binding test.pdf --dry-run
   rm test.pdf
   ```

3. **Check Package Page**
   - Visit: `https://pypi.org/project/pdf-section-binding/`
   - Verify description renders correctly
   - Check download stats and links

### Git & GitHub Actions

1. **Tag the Release**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Create GitHub Release**
   - Go to repository → Releases → Create new release
   - Use tag `v1.0.0`
   - Add release notes

3. **Update README.md**
   ```markdown
   ## Installation
   
   Install from PyPI:
   ```bash
   pip install pdf-section-binding
   ```

### Documentation Updates

1. **Update Installation Instructions**
   - Remove development installation from main README
   - Add PyPI installation as primary method

2. **Update Examples**
   - Ensure all examples use published CLI commands
   - Test examples work with installed package

### Maintenance Schedule

**Weekly**: Check for issues and user feedback
**Monthly**: Security updates, dependency updates
**Quarterly**: Feature updates, version bumps

## 🎯 Quick Commands for Future Releases

### Standard Release Process
```bash
# 1. Update version
vim src/pdf_section_binding/version.py

# 2. Run tests
python -m pytest

# 3. Build and check
rm -rf dist/
python -m build
python -m twine check dist/*

# 4. Test on TestPyPI
python -m twine upload --repository testpypi dist/*

# 5. Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-section-binding

# 6. If good, publish to PyPI
python -m twine upload dist/*

# 7. Tag and push
git tag v1.0.X
git push origin v1.0.X
```

### Emergency Hotfix Process
```bash
# For critical bugs requiring immediate fix
git checkout main
# Fix the bug
python -m pytest  # Ensure tests pass
# Increment patch version (1.0.0 → 1.0.1)
# Build and publish immediately (skip TestPyPI)
python -m build
python -m twine upload dist/*
```

## 🔐 Security Notes

- **Never commit API tokens** to version control
- **Rotate tokens** every 6 months
- **Use environment variables** for automation:
  ```bash
  export TWINE_USERNAME=__token__
  export TWINE_PASSWORD=your-api-token
  twine upload dist/*
  ```
- **Enable 2FA** on PyPI account
- **Monitor package** for unauthorized uploads

---

*Last updated: Keep this section current with each release*
