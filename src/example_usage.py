#!/usr/bin/env python3
"""
Example usage of the PDF Section Binding package.

This demonstrates how to use the package both as a CLI tool and as a Python
library.
"""

import os
from pdf_section_binding import SectionBindingProcessor, calculate_signature_order


def example_cli_usage():
    """Example showing CLI usage through subprocess."""
    print("=== CLI Usage Examples ===")
    print("Command line usage:")
    print("pdf-section-binding input.pdf --dry-run")
    print("pdf-section-binding input.pdf -s 16 -v")
    print("pdf-section-binding input.pdf -o custom_output.pdf --force")
    print()


def example_library_usage():
    """Example showing library usage."""
    print("=== Library Usage Examples ===")

    # Example 1: Calculate signature order
    print("1. Calculate signature order for 12 pages with 4-page signatures:")
    order = calculate_signature_order(12, 4)
    print(f"   Page order: {order}")
    print()

    # Example 2: Using SectionBindingProcessor
    print("2. Using SectionBindingProcessor class:")

    # Create a processor
    processor = SectionBindingProcessor(verbose=True)

    # Example with dry run (requires actual PDF file)
    if os.path.exists("../tests/test-data/test_document.pdf"):
        print("   Processing test PDF file...")
        try:
            result = processor.process_pdf(
                input_path="../tests/test-data/test_document.pdf",
                output_path="/tmp/test_output.pdf",
                signature_size=8,
                dry_run=True,  # Don't create actual file
            )

            print(f"   Total pages: {result['total_pages']}")
            print(f"   Signatures: {result['total_signatures']}")
            print(f"   Papers needed: {result['total_papers']}")

        except (FileNotFoundError, PermissionError, RuntimeError) as e:
            print(f"   Error: {e}")
    elif os.path.exists("../data/book.pdf"):
        print("   Processing original book PDF file...")
        try:
            result = processor.process_pdf(
                input_path="../data/book.pdf",
                output_path="/tmp/test_output.pdf",
                signature_size=8,
                dry_run=True,  # Don't create actual file
            )

            print(f"   Total pages: {result['total_pages']}")
            print(f"   Signatures: {result['total_signatures']}")
            print(f"   Papers needed: {result['total_papers']}")

        except (FileNotFoundError, PermissionError, RuntimeError) as e:
            print(f"   Error: {e}")
    else:
        print("   (No sample PDF file found for actual processing)")

    print()


def example_signature_calculations():
    """Example showing signature size calculations."""
    print("=== Signature Size Examples ===")

    signature_sizes = [4, 8, 16, 32, 40]

    for sig_size in signature_sizes:
        papers = sig_size // 4
        print(
            f"{sig_size:2d} pages per signature = {papers:2d} papers per " "signature"
        )

    print()
    print("Custom examples:")
    custom_sizes = [12, 20, 24, 28, 36, 44]
    for sig_size in custom_sizes:
        papers = sig_size // 4
        print(
            f"{sig_size:2d} pages per signature = {papers:2d} papers per " "signature"
        )

    print()


def main():
    """Run all examples."""
    print("PDF Section Binding Tool - Usage Examples")
    print("=" * 50)
    print()

    example_cli_usage()
    example_library_usage()
    example_signature_calculations()

    print("For more information, run: pdf-section-binding --help")


if __name__ == "__main__":
    main()
