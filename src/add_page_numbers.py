#!/usr/bin/env python3
"""
Utility script to add page numbers to a PDF file.

This script adds page numbers to each page of a PDF document.
The page numbers are positioned at the bottom center of each page.
"""

import argparse
import os
import sys
from pathlib import Path
from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def create_page_number_overlay(page_num, page_width, page_height, font_size=12):
    """
    Create a PDF overlay with just a page number.

    Args:
        page_num (int): The page number to display
        page_width (float): Width of the page in points
        page_height (float): Height of the page in points
        font_size (int): Font size for the page number

    Returns:
        BytesIO: PDF overlay as bytes
    """
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Set font (Helvetica is built-in)
    can.setFont("Helvetica", font_size)

    # Position page number at bottom center, with some margin
    margin_bottom = 30
    text_width = can.stringWidth(str(page_num), "Helvetica", font_size)
    x_position = (page_width - text_width) / 2
    y_position = margin_bottom

    # Draw the page number
    can.drawString(x_position, y_position, str(page_num))
    can.save()

    packet.seek(0)
    return packet


def add_page_numbers_to_pdf(input_path, output_path, start_number=1, font_size=12):
    """
    Add page numbers to a PDF file.

    Args:
        input_path (str): Path to input PDF file
        output_path (str): Path to output PDF file
        start_number (int): Starting page number (default: 1)
        font_size (int): Font size for page numbers (default: 12)

    Returns:
        dict: Information about the processed PDF
    """
    try:
        # Read the input PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()

        total_pages = len(reader.pages)
        print(f"Processing {total_pages} pages...")

        for i, page in enumerate(reader.pages):
            page_num = start_number + i

            # Get page dimensions
            page_box = page.mediabox
            page_width = float(page_box.width)
            page_height = float(page_box.height)

            # Create overlay with page number
            overlay_pdf = create_page_number_overlay(
                page_num, page_width, page_height, font_size
            )
            overlay_reader = PdfReader(overlay_pdf)
            overlay_page = overlay_reader.pages[0]

            # Merge the overlay with the original page
            page.merge_page(overlay_page)
            writer.add_page(page)

            # Show progress
            if (i + 1) % 10 == 0 or (i + 1) == total_pages:
                print(f"Processed {i + 1}/{total_pages} pages...")

        # Write the output PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        result = {
            "input_path": input_path,
            "output_path": output_path,
            "total_pages": total_pages,
            "start_number": start_number,
            "font_size": font_size,
            "success": True,
        }

        return result

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Input file not found: {input_path}") from e
    except PermissionError as e:
        raise PermissionError(f"Permission error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {e}") from e


def main():
    """Main function to run the page numbering tool."""
    parser = argparse.ArgumentParser(
        description="Add page numbers to a PDF file",
        epilog="""
Examples:
  python add_page_numbers.py input.pdf
  python add_page_numbers.py input.pdf -o numbered_output.pdf
  python add_page_numbers.py input.pdf -s 5 --font-size 14
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("input", help="Input PDF file path")

    parser.add_argument(
        "-o", "--output", help="Output PDF file path (default: input_name_numbered.pdf)"
    )

    parser.add_argument(
        "-s",
        "--start-number",
        type=int,
        default=1,
        help="Starting page number (default: 1)",
    )

    parser.add_argument(
        "--font-size",
        type=int,
        default=12,
        help="Font size for page numbers (default: 12)",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    # Generate output filename if not provided
    if not args.output:
        input_path = Path(args.input)
        args.output = str(input_path.parent / f"{input_path.stem}_numbered.pdf")

    # Check if output file exists
    if os.path.exists(args.output):
        response = input(f"Output file '{args.output}' exists. Overwrite? (y/N): ")
        if response.lower() not in ["y", "yes"]:
            print("Operation cancelled.")
            sys.exit(0)

    # Validate arguments
    if args.start_number < 1:
        print("Error: Start number must be at least 1.", file=sys.stderr)
        sys.exit(1)

    if args.font_size < 6 or args.font_size > 72:
        print("Error: Font size must be between 6 and 72.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.verbose:
            print(f"Input file: {args.input}")
            print(f"Output file: {args.output}")
            print(f"Start number: {args.start_number}")
            print(f"Font size: {args.font_size}")
            print()

        result = add_page_numbers_to_pdf(
            args.input, args.output, args.start_number, args.font_size
        )

        print("✅ Successfully added page numbers!")
        print(f"📄 Input: {result['input_path']}")
        print(f"📄 Output: {result['output_path']}")
        print(f"📋 Total pages: {result['total_pages']}")
        print(
            f"🔢 Page numbers: {result['start_number']} to "
            f"{result['start_number'] + result['total_pages'] - 1}"
        )

    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(13)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
