#!/usr/bin/env python3
"""
Demonstration of section binding page order calculation.
This script shows how pages are reordered for different signature sizes.
"""


def demonstrate_signature_order(total_pages, signature_size):
    """Demonstrate how section binding reorders pages."""
    print(f"\n{'='*60}")
    print("SECTION BINDING DEMONSTRATION")
    print(f"Total pages: {total_pages}")
    print(f"Signature size: {signature_size}")
    print("=" * 60)

    # Pad pages to make them divisible by signature size
    padded_pages = (
        (total_pages + signature_size - 1) // signature_size
    ) * signature_size

    # Create list of pages (1-indexed)
    pages = list(range(1, total_pages + 1))

    # Add blank pages if needed
    while len(pages) < padded_pages:
        pages.append("BLANK")

    print(
        f"Padded to {padded_pages} pages "
        f"(added {padded_pages - total_pages} blank pages)"
    )
    print(f"Number of signatures: {padded_pages // signature_size}")
    print(f"Pages per signature: {signature_size}")
    print(f"Sheets per signature: {signature_size // 2}")

    # Process each signature
    for sig_num in range(padded_pages // signature_size):
        signature_start = sig_num * signature_size
        signature_end = signature_start + signature_size

        print(f"\n--- SIGNATURE {sig_num + 1} ---")
        print(f"Original page order: {pages[signature_start:signature_end]}")

        # Calculate reordered pages for this signature
        signature_order = []
        sheet_info = []

        for i in range(signature_size // 2):
            left_page = signature_start + i
            right_page = signature_start + signature_size - 1 - i

            # Add the pages for this sheet
            sheet_pages = [pages[right_page], pages[left_page]]
            signature_order.extend(sheet_pages)

            sheet_info.append(
                {
                    "sheet": i + 1,
                    "pages": sheet_pages,
                    "positions": [
                        right_page + 1,
                        left_page + 1,
                    ],  # 1-indexed for display
                }
            )

        print(f"Reordered for binding: {signature_order}")

        print("\nSheet breakdown:")
        for sheet in sheet_info:
            print(
                f"  Sheet {sheet['sheet']}: {sheet['pages']} "
                f"(positions {sheet['positions']})"
            )

        print("\nWhen folded and stacked, this signature will read:")
        original_order = pages[signature_start:signature_end]
        print("  " + " -> ".join(map(str, original_order)))


if __name__ == "__main__":
    # Demonstrate with small examples
    print("SECTION BINDING PAGE ORDER DEMONSTRATION")

    # Example 1: 8 pages, 4-page signatures
    demonstrate_signature_order(8, 4)

    # Example 2: 12 pages, 8-page signatures
    demonstrate_signature_order(12, 8)

    # Example 3: 6 pages, 4-page signatures (needs padding)
    demonstrate_signature_order(6, 4)
