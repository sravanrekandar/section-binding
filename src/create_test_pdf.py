#!/usr/bin/env python3
"""
Create a test PDF with numbered pages for testing section binding.

This script creates a PDF with the specified number of pages, where each page
displays its page number in large text. Useful for testing the section binding
algorithm and verifying that pages are reordered correctly.
"""

import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, red
import os


def create_numbered_pdf(filename: str, num_pages: int = 101, page_size=letter):
    """
    Create a PDF with numbered pages.

    Args:
        filename: Output PDF filename
        num_pages: Number of pages to create (default: 101)
        page_size: Page size tuple (default: letter)
    """
    print(f"Creating PDF '{filename}' with {num_pages} pages...")

    # Create canvas
    c = canvas.Canvas(filename, pagesize=page_size)
    width, height = page_size

    for page_num in range(1, num_pages + 1):
        # Clear the page
        c.setFillColor(black)

        # Title at top
        c.setFont("Helvetica-Bold", 24)
        title = "PDF Section Binding Test Document"
        title_width = c.stringWidth(title, "Helvetica-Bold", 24)
        c.drawString((width - title_width) / 2, height - 1 * inch, title)

        # Large page number in center
        c.setFillColor(blue)
        c.setFont("Helvetica-Bold", 144)  # Very large font
        page_text = str(page_num)
        text_width = c.stringWidth(page_text, "Helvetica-Bold", 144)
        text_height = 144  # Approximate height

        # Center the page number
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        c.drawString(x, y, page_text)

        # Add some metadata
        c.setFillColor(black)
        c.setFont("Helvetica", 12)

        # Page info at bottom
        info_text = f"Page {page_num} of {num_pages}"
        info_width = c.stringWidth(info_text, "Helvetica", 12)
        c.drawString((width - info_width) / 2, 1 * inch, info_text)

        # Add corners for orientation reference
        c.setFillColor(red)
        c.setFont("Helvetica-Bold", 10)

        # Top-left corner
        c.drawString(0.5 * inch, height - 0.5 * inch, "TL")

        # Top-right corner
        tr_text = "TR"
        tr_width = c.stringWidth(tr_text, "Helvetica-Bold", 10)
        c.drawString(width - 0.5 * inch - tr_width, height - 0.5 * inch, tr_text)

        # Bottom-left corner
        c.drawString(0.5 * inch, 0.3 * inch, "BL")

        # Bottom-right corner
        br_text = "BR"
        br_width = c.stringWidth(br_text, "Helvetica-Bold", 10)
        c.drawString(width - 0.5 * inch - br_width, 0.3 * inch, br_text)

        # Show progress every 10 pages
        if page_num % 10 == 0:
            print(f"  Created page {page_num}...")

        # Start new page (except for the last page)
        if page_num < num_pages:
            c.showPage()

    # Save the PDF
    c.save()
    print(f"✅ Successfully created '{filename}' with {num_pages} pages")

    # Show file size
    size = os.path.getsize(filename)
    size_mb = size / (1024 * 1024)
    print(f"📊 File size: {size_mb:.2f} MB")


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Create a test PDF with numbered pages for section binding testing",
        epilog="""
Examples:
  %(prog)s                             # Create 101-page test document in ../tests/test-data/
  %(prog)s -n 50                       # Create 50-page document
  %(prog)s -o ../tests/test-data/custom.pdf # Custom output filename
  %(prog)s -n 24 -s A4                # 24 pages in A4 format
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-n",
        "--num-pages",
        type=int,
        default=101,
        help="Number of pages to create (default: 101)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="../tests/test-data/test_document.pdf",
        help="Output PDF filename (default: ../tests/test-data/test_document.pdf)",
    )

    parser.add_argument(
        "-s",
        "--size",
        choices=["letter", "A4"],
        default="letter",
        help="Page size (default: letter)",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.num_pages < 1:
        print("Error: Number of pages must be at least 1")
        return 1

    if args.num_pages > 1000:
        print("Error: Number of pages should not exceed 1000 (file would be too large)")
        return 1

    # Set page size
    page_size = letter if args.size == "letter" else A4

    try:
        create_numbered_pdf(args.output, args.num_pages, page_size)

        print("\n🎯 Test with section binding:")
        print(f"pdf-section-binding {args.output} --dry-run")
        print(f"pdf-section-binding {args.output} -s 8")
        print(f"pdf-section-binding {args.output} -s 16 -v")

        return 0

    except ImportError:
        print("❌ Error: Missing required library.")
        print("Install with: pip install reportlab")
        return 1

    except (OSError, IOError) as e:
        print(f"❌ Error creating PDF: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
