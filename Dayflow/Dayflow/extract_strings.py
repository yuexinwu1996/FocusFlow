#!/usr/bin/env python3
"""
Extract all user-visible strings from Dayflow Swift files for i18n
"""

import re
import json
import os
from pathlib import Path
from collections import OrderedDict

# Regex patterns for extracting user-visible strings
PATTERNS = [
    # Text("string") or Text("string \(variable)")
    r'Text\("([^"]+)"\)',
    # String(localized: "key")
    r'String\(localized:\s*"([^"]+)"',
    # title: "string"
    r'title:\s*"([^"]+)"',
    # subtitle: "string"
    r'subtitle:\s*"([^"]+)"',
    # placeholder: "string"
    r'placeholder:\s*"([^"]+)"',
    # .alert(title: Text("string"))
    r'\.alert\([^)]*Text\("([^"]+)"\)',
    # Button action labels
    r'Button\([^)]*\)\s*{\s*Text\("([^"]+)"\)',
]

# Strings to exclude (system strings, variable names, etc.)
EXCLUDE_PATTERNS = [
    r'^[a-z_]+$',  # single lowercase words (likely variable names)
    r'^\d+$',  # pure numbers
    r'^https?://',  # URLs
    r'^[A-Z_]+$',  # CONSTANTS
    r'^SF\s',  # SF font names
    r'^Instrument',  # Font names
    r'^Nunito',  # Font names
]

def should_exclude(text):
    """Check if a string should be excluded from localization"""
    for pattern in EXCLUDE_PATTERNS:
        if re.match(pattern, text):
            return True
    return False

def extract_strings_from_file(filepath):
    """Extract all localizable strings from a Swift file"""
    strings = set()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        for pattern in PATTERNS:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                # Clean up the string
                text = match.strip()
                if text and not should_exclude(text):
                    # Don't include strings with only interpolation
                    if not re.match(r'^\\(.+)$', text):
                        strings.add(text)

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return strings

def main():
    base_dir = Path(__file__).parent
    views_dir = base_dir / "Views"
    menu_dir = base_dir / "Menu"

    all_strings = set()
    file_count = 0

    # Process Views directory
    for swift_file in views_dir.rglob("*.swift"):
        strings = extract_strings_from_file(swift_file)
        all_strings.update(strings)
        file_count += 1
        if strings:
            print(f"Found {len(strings)} strings in {swift_file.name}")

    # Process Menu directory
    for swift_file in menu_dir.rglob("*.swift"):
        strings = extract_strings_from_file(swift_file)
        all_strings.update(strings)
        file_count += 1
        if strings:
            print(f"Found {len(strings)} strings in {swift_file.name}")

    print(f"\n{'='*60}")
    print(f"Processed {file_count} files")
    print(f"Found {len(all_strings)} unique localizable strings")
    print(f"{'='*60}\n")

    # Sort strings for consistent output
    sorted_strings = sorted(all_strings)

    # Output to file for review
    output_file = base_dir / "extracted_strings.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in sorted_strings:
            f.write(f"{s}\n")

    print(f"Extracted strings saved to: {output_file}")

    return sorted_strings

if __name__ == "__main__":
    main()
