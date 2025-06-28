#!/usr/bin/env python3
"""
PDF Section Binding Page Reordering Script

This script reorders PDF pages for section binding (bookbinding).
Section binding involves arranging pages in signatures (folded sheets)
so that when printed and folded, pages appear in correct order.
"""

import argparse
import sys
import os
from PyPDF2 import PdfReader, PdfWriter


def calculate_signature_order(total_pages, signature_size):
    """
    Calculate the page order for section binding.

    For section binding, pages are arranged so that when printed double-sided
    and folded, they appear in correct reading order.

    Args:
        total_pages (int): Total number of pages in the PDF
        signature_size (int): Number of pages per signature (4, 8, 16, 32)

    Returns:
        list: Ordered list of page numbers for section binding
    """
    # Pad pages to make them divisible by signature size
    padded_pages = (
        (total_pages + signature_size - 1) // signature_size
    ) * signature_size

    # Create list of pages (1-indexed)
    pages = list(range(1, total_pages + 1))

    # Add blank pages if needed
    while len(pages) < padded_pages:
        pages.append(None)  # None represents blank pages

    # Calculate signature order
    reordered_pages = []

    # Process each signature
    for signature_start in range(0, padded_pages, signature_size):
        # Calculate the correct order for this signature
        signature_order = []

        for i in range(signature_size // 2):
            left_page = signature_start + i
            right_page = signature_start + signature_size - 1 - i

            # Add the pages for this sheet
            if right_page < len(pages):
                signature_order.append(pages[right_page])
            if left_page < len(pages):
                signature_order.append(pages[left_page])

        reordered_pages.extend(signature_order)

    return [p for p in reordered_pages if p is not None]


def reorder_pdf_for_section_binding(input_path, output_path, signature_size=8):
    """
    Reorder PDF pages for section binding.

    Args:
        input_path (str): Path to input PDF
        output_path (str): Path to output PDF
        signature_size (int): Pages per signature (default: 8)
    """
    try:
        # Read the input PDF
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)

        print(f"Input PDF: {input_path}")
        print(f"Total pages: {total_pages}")
        print(f"Signature size: {signature_size}")

        # Calculate page order
        page_order = calculate_signature_order(total_pages, signature_size)

        print(f"Reordered page sequence: {page_order}")

        # Create output PDF
        writer = PdfWriter()

        # Add pages in the calculated order
        for page_num in page_order:
            if page_num and page_num <= total_pages:
                writer.add_page(reader.pages[page_num - 1])  # Convert to 0-indexed

        # Write the output PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"Section binding PDF created: {output_path}")
        print(f"Total pages in output: {len(writer.pages)}")

        # Print binding instructions
        print("\n" + "=" * 50)
        print("SECTION BINDING INSTRUCTIONS:")
        print("=" * 50)
        print(f"1. Print the output PDF ({output_path}) double-sided")
        print(f"2. Each {signature_size//4} papers (sheets) forms one signature")
        print("3. Fold each signature in half")
        print("4. Stack signatures in order")
        print("5. Bind along the fold")
        print("=" * 50)

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)
    except (OSError, IOError, ValueError) as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main function to run the section binding tool."""
    parser = argparse.ArgumentParser(
        description="Reorder PDF pages for section binding"
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output PDF file path (default: input_name_section_bound.pdf)",
    )
    parser.add_argument(
        "-s",
        "--signature-size",
        type=int,
        default=8,
        help="Pages per signature (must be multiple of 4, default: 8). "
        "Common: 4, 8, 16, 32, 40",
    )

    args = parser.parse_args()

    # Validate signature size
    if args.signature_size % 4 != 0:
        print("Error: Signature size must be a multiple of 4 (each paper = 4 pages).")
        print(
            f"You specified {args.signature_size}. Try: "
            f"{(args.signature_size // 4) * 4} or "
            f"{((args.signature_size // 4) + 1) * 4}"
        )
        sys.exit(1)

    if args.signature_size < 4:
        print("Error: Signature size must be at least 4 pages (1 paper).")
        sys.exit(1)

    if args.signature_size > 128:
        print(
            f"Error: Signature size too large ({args.signature_size}). "
            "Maximum recommended: 128 pages (32 papers)."
        )
        sys.exit(1)

    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    # Generate output filename if not provided
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}_section_bound.pdf"

    # Process the PDF
    reorder_pdf_for_section_binding(args.input, args.output, args.signature_size)


if __name__ == "__main__":
    main()
