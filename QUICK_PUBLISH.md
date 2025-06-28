# Quick PyPI Publishing Reference

## 🚀 Ready to Publish!

Your package is ready to be published to PyPI. Here's the quick process:

### Before You Start

1. **Update your information** in these files:
   - `setup.py`: Update GitHub URLs (replace "yourusername")
   - `pyproject.toml`: Update author name and email
   - `src/pdf_section_binding/version.py`: Update author info

2. **Create PyPI accounts**:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

3. **Get API tokens**:
   - PyPI: Account Settings → API tokens → Create token
   - TestPyPI: Same process on TestPyPI
   - Save tokens securely!

### Quick Publishing Commands

```bash
# Method 1: Use the helper script
python publish.py workflow          # Build + check everything
python publish.py testpypi          # Publish to TestPyPI
python publish.py pypi              # Publish to PyPI

# Method 2: Manual commands
python -m build                     # Build package
python -m twine check dist/*        # Check package
twine upload --repository testpypi dist/*   # Upload to TestPyPI
twine upload dist/*                 # Upload to PyPI
```

### Authentication

When uploading, use:
- **Username**: `__token__`
- **Password**: Your API token (starts with `pypi-`)

### Test Installation

After publishing to TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pdf-section-binding
```

After publishing to PyPI:
```bash
pip install pdf-section-binding
```

### Current Package Status

✅ **Package built successfully**
✅ **All tests pass** (21/21)
✅ **Linting clean** (10.00/10 pylint score)
✅ **PyPI compliance check passed**
✅ **Ready for publishing!**

### Package Details

- **Name**: `pdf-section-binding`
- **Version**: `1.0.0`
- **CLI Commands**: `pdf-section-binding`, `section-binding`
- **Dependencies**: `PyPDF2>=3.0.0`
- **Python**: `>=3.7`

### Next Steps

1. Update author information
2. Test on TestPyPI first
3. If everything works, publish to PyPI
4. Tag your release: `git tag v1.0.0 && git push origin v1.0.0`

📖 See `PUBLISHING.md` for the complete guide.
