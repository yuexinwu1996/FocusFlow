#!/usr/bin/env python3
"""
Extract localizable strings from Swift files for Dayflow internationalization
"""
import re
import os
import json
from pathlib import Path
from collections import OrderedDict

def extract_text_strings(file_path):
    """Extract Text("...") patterns from Swift file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for Text("...")
    pattern = r'Text\("([^"\\]*(\\.[^"\\]*)*)"\)'
    matches = re.findall(pattern, content)

    strings = []
    for match in matches:
        if isinstance(match, tuple):
            text = match[0]
        else:
            text = match

        # Skip strings with interpolation
        if '\\(' in text:
            continue

        strings.append(text)

    return strings

def extract_label_strings(file_path):
    """Extract label: "..." patterns from Swift file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for label: "...", title: "...", etc.
    pattern = r'(?:label|title|message|placeholder):\s*"([^"\\]*(\\.[^"\\]*)*)"\)'
    matches = re.findall(pattern, content)

    strings = []
    for match in matches:
        if isinstance(match, tuple):
            text = match[0]
        else:
            text = match

        # Skip strings with interpolation
        if '\\(' in text:
            continue

        strings.append(text)

    return strings

def scan_directory(directory):
    """Scan directory for Swift files and extract strings"""
    all_strings = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.swift'):
                file_path = os.path.join(root, file)
                print(f"Scanning: {file_path}")

                text_strings = extract_text_strings(file_path)
                label_strings = extract_label_strings(file_path)

                all_strings.update(text_strings)
                all_strings.update(label_strings)

    return sorted(all_strings)

if __name__ == '__main__':
    dayflow_dir = '/Users/bytedance/Documents/GitHub/FocusFlow/Dayflow/Dayflow'

    print("Extracting strings from Dayflow project...")
    strings = scan_directory(dayflow_dir)

    print(f"\nFound {len(strings)} unique strings")

    # Save to file
    output_file = 'extracted_strings.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in strings:
            f.write(f"{s}\n")

    print(f"Strings saved to {output_file}")
