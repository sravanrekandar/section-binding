# PDF Section Binding Tool

[![PyPI version](https://badge.fury.io/py/pdf-section-binding.svg)](https://badge.fury.io/py/pdf-section-binding)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pdf-section-binding)](https://pypi.org/project/pdf-section-binding/)
[![GitHub release](https://img.shields.io/github/release/sravanrekandar/section-binding.svg)](https://github.com/sravanrekandar/section-binding/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This tool reorders PDF pages for section binding (bookbinding), where pages are arranged in signatures (folded sheets) so that when printed and folded, they appear in the correct reading order.

## Quick Links

🚀 **Install**: `pip install pdf-section-binding`  
📦 **PyPI**: [Production Package](https://pypi.org/project/pdf-section-binding/)  
🧪 **TestPyPI**: [Test Package](https://test.pypi.org/project/pdf-section-binding/)  
📖 **Source**: [GitHub Repository](https://github.com/sravanrekandar/section-binding)  
🐛 **Issues**: [Bug Reports](https://github.com/sravanrekandar/section-binding/issues)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [How Section Binding Works](#how-section-binding-works)
- [Library Usage](#library-usage)
- [Development](#development)
- [Requirements](#requirements)
- [Binding Instructions](#binding-instructions)
- [License](#license)
- [Contributing](#contributing)
- [Support](#support)

## Installation

### From PyPI (Recommended)

[![PyPI version](https://badge.fury.io/py/pdf-section-binding.svg)](https://badge.fury.io/py/pdf-section-binding)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pdf-section-binding)](https://pypi.org/project/pdf-section-binding/)

```bash
pip install pdf-section-binding
```

📦 **PyPI Package**: [https://pypi.org/project/pdf-section-binding/](https://pypi.org/project/pdf-section-binding/)  
🧪 **TestPyPI Package**: [https://test.pypi.org/project/pdf-section-binding/](https://test.pypi.org/project/pdf-section-binding/)

### From Source

1. Clone the repository:
```bash
git clone https://github.com/sravanrekandar/pdf-section-binding.git
cd pdf-section-binding
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install in development mode:
```bash
pip install -e .
```

## Usage

After installation, use the `pdf-section-binding` command (or the shorter `section-binding` alias):

```bash
pdf-section-binding input.pdf [options]
```

### Command Line Options

- `-o, --output`: Output PDF file path (default: `input_name_section_bound.pdf`)
- `-s, --signature-size`: Pages per signature - must be multiple of 4 (default: 8)
- `--dry-run`: Preview analysis without creating output file
- `-v, --verbose`: Enable verbose output with progress tracking
- `-q, --quiet`: Suppress all output except errors
- `--force`: Overwrite output file if it exists
- `--version`: Show version information
- `-h, --help`: Show help message

### Examples

```bash
# Basic usage with 8-page signatures (2 papers per signature)
pdf-section-binding book.pdf

# Specify output file and 4-page signatures (1 paper per signature)  
pdf-section-binding book.pdf -o output.pdf -s 4

# Use 16-page signatures (4 papers per signature)
pdf-section-binding book.pdf -s 16

# Use 40-page signatures (10 papers per signature)
pdf-section-binding book.pdf -s 40

# Preview without creating file (dry run)
pdf-section-binding book.pdf --dry-run

# Verbose output with progress tracking
pdf-section-binding book.pdf -v

# Quiet mode (minimal output)
pdf-section-binding book.pdf -q

# Force overwrite existing output
pdf-section-binding book.pdf --force
```

## Features

✨ **Enhanced CLI Tool**
- 🎨 **Colorized output** for better user experience
- 📊 **Progress tracking** for large documents
- 🔍 **Dry run mode** to preview without creating files
- ⚡ **Fast processing** with optimized algorithms
- 🛡️ **Robust error handling** with helpful suggestions
- 📏 **Flexible signature sizes** (any multiple of 4)

🔧 **Advanced Options**
- Verbose and quiet modes
- Force overwrite protection
- Input validation with helpful error messages
- Multiple command aliases (`pdf-section-binding` or `section-binding`)

📦 **Library Usage**
- Use as a Python library in your own projects
- Clean API with `SectionBindingProcessor` class
- Comprehensive test suite included

## CLI Features in Detail

### Smart Error Messages
The tool provides helpful suggestions when you make mistakes:

```bash
$ pdf-section-binding book.pdf -s 15
Error: Signature size must be a multiple of 4 (each paper = 4 pages).
You specified 15. Try: 12 or 16
```

### Progress Tracking
For large documents, see progress in real-time:

```bash
$ pdf-section-binding large-book.pdf -v
PDF Section Binding Tool v1.0.0
==================================================
[INFO] Reading PDF: large-book.pdf
[INFO] Total pages: 1500
[INFO] Signature size: 8
[INFO] Creating reordered PDF...
Creating PDF: [████████████████████████████████████████████████] 100% (1500/1500)
[INFO] Writing output: large-book_section_bound.pdf
✅ Successfully created: large-book_section_bound.pdf
```

### Dry Run Analysis
Preview the binding setup without creating files:

```bash
$ pdf-section-binding book.pdf --dry-run
🔍 DRY RUN ANALYSIS:
Would process 701 pages
Would create 88 signatures  
Would need 176 papers total
Would save to: book_section_bound.pdf
```

Section binding involves:

1. **Signature Creation**: Pages are grouped into signatures (folded sheets)
2. **Page Reordering**: Pages are rearranged so that when printed double-sided and folded, they appear in correct reading order
3. **Printing**: Print the reordered PDF double-sided
4. **Folding**: Fold each signature in half
5. **Binding**: Stack signatures and bind along the fold

## Signature Sizes

- **4 pages**: Each signature uses 1 paper (2 pages front, 2 pages back)
- **8 pages**: Each signature uses 2 papers (4 pages front, 4 pages back)
- **16 pages**: Each signature uses 4 papers (8 pages front, 8 pages back)
- **32 pages**: Each signature uses 8 papers (16 pages front, 16 pages back)
- **40 pages**: Each signature uses 10 papers (20 pages front, 20 pages back)
- **Custom sizes**: Any multiple of 4 pages (e.g., 12=3 papers, 20=5 papers, 24=6 papers)

## Paper Calculation

**Formula**: `Papers per signature = Signature size ÷ 4`

Examples:
- 10 papers = 40 pages per signature
- 6 papers = 24 pages per signature  
- 3 papers = 12 pages per signature

## Example Output

For a 4-page signature with pages 1, 2, 3, 4:
- The reordered sequence would be: [4, 1, 3, 2]
- When printed double-sided and folded, you get pages in order: 1, 2, 3, 4

## Generated Files

This tool was used to process the book in `data/book.pdf`:

- `data/book_section_bound.pdf` - Default 8-page signatures (2 papers each)
- `data/book_40page_signature.pdf` - 40-page signatures (10 papers each)

## Publishing to PyPI

This package is ready for PyPI publication! Here's how to publish it:

### Prerequisites

1. Create accounts on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/)
2. Install build tools:
   ```bash
   pip install build twine
   ```

### Build and Upload

1. **Build the package:**
   ```bash
   python -m build
   ```

2. **Test on TestPyPI first:**
   ```bash
   twine upload --repository testpypi dist/*
   ```

3. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```

### Package Structure

The package follows modern Python packaging standards:

```
pdf-section-binding/
├── src/pdf_section_binding/    # Source code
│   ├── __init__.py
│   ├── cli.py                  # Enhanced CLI interface
│   ├── core.py                 # Core processing logic
│   └── version.py              # Version and metadata
├── tests/                      # Comprehensive test suite
├── pyproject.toml              # Modern packaging config
├── setup.py                    # Fallback setup config
├── LICENSE                     # MIT license
├── README.md                   # This file
└── requirements.txt            # Dependencies

```

### Development Setup

For development work:

```bash
# Clone and setup
git clone <your-repo-url>
cd pdf-section-binding

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Run with coverage
pytest --cov=pdf_section_binding

# Format code
black src/ tests/

# Lint code
pylint src/ tests/

# Type checking
mypy src/
```

## Requirements

- Python 3.7+
- PyPDF2 library

## Binding Instructions

After running the script:

1. Print the output PDF double-sided (flip on long edge)
2. Cut or separate the printed sheets by signature
3. Fold each signature in half along the center
4. Stack all signatures in order
5. Bind along the folded edge using:
   - Saddle stitching (stapling)
   - Perfect binding (glue)
   - Spiral binding
   - Or other binding methods

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

- 📦 **PyPI Package**: [https://pypi.org/project/pdf-section-binding/](https://pypi.org/project/pdf-section-binding/)
- 📖 **Source Code**: [https://github.com/sravanrekandar/section-binding](https://github.com/sravanrekandar/section-binding)
- 🐛 **Report Issues**: [https://github.com/sravanrekandar/section-binding/issues](https://github.com/sravanrekandar/section-binding/issues)

## Author

**Sravan Kumar Rekandar**  
- GitHub: [@sravanrekandar](https://github.com/sravanrekandar)

---

*Made with ❤️ for the bookbinding community*
