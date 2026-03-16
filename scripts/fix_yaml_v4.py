#!/usr/bin/env python3
"""
Fix YAML front matter in Jekyll posts - Version 4.
Handles complex cases where:
- Values span multiple lines with embedded key names (e.g., "title: ... date: ...")
- Values need to be properly quoted
- Special characters need escaping
- Preserves hyphenated category/tag names like 'world-news'
"""

import os
import re
import glob

# All known YAML keys in order of priority for detection
KNOWN_KEYS = [
    'layout', 'title', 'date', 'categories', 'tags', 'source_url',
    'source_title', 'source_id', 'excerpt', 'hn_id', 'hn_score', 'hn_comments'
]

def extract_frontmatter(content):
    """Extract front matter from content, return (frontmatter_text, rest_of_content)"""
    if not content.startswith('---'):
        return None, content
    
    # Find the second ---
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, content
    
    frontmatter_text = match.group(1)
    rest = content[match.end():]
    return frontmatter_text, rest

def parse_frontmatter_robust(text):
    """
    Parse frontmatter text robustly, handling embedded keys.
    Returns a list of (key, value) tuples preserving order.
    """
    # Create a pattern that matches any known key at the start of a word boundary
    # Use word boundary but also require it not to be preceded by alphanumeric
    key_pattern = r'(?<![a-zA-Z0-9_-])(' + '|'.join(KNOWN_KEYS) + r'):\s*'
    
    # Find all key positions
    key_matches = list(re.finditer(key_pattern, text))
    
    if not key_matches:
        return []
    
    result = []
    for i, match in enumerate(key_matches):
        key = match.group(1)
        start = match.end()
        
        # End is either the start of the next key or end of text
        if i + 1 < len(key_matches):
            end = key_matches[i + 1].start()
        else:
            end = len(text)
        
        value = text[start:end].strip()
        result.append((key, value))
    
    return result

def parse_list_value(value):
    """Parse a list value (categories or tags) and return list items."""
    value = value.strip()
    
    # Format: [item1, item2, ...]
    if value.startswith('[') and ']' in value:
        bracket_end = value.index(']')
        inner = value[1:bracket_end]
        items = [item.strip().strip('"').strip("'") for item in inner.split(',')]
        return [item for item in items if item]
    
    # Format: multiline list with - items
    # Extract items like "- tech" or "- world-news"
    items = re.findall(r'-\s+([^\s][^\n]*?)(?=\s+-\s|\s*$)', value)
    if items:
        return [item.strip() for item in items if item.strip()]
    
    # Single value
    if value:
        return [value]
    
    return []

def format_value(key, value):
    """Format a value appropriately for YAML."""
    value = value.strip()
    
    # Empty value
    if not value:
        return ''
    
    # Remove existing quotes
    if len(value) >= 2:
        if (value.startswith('"') and value.endswith('"')):
            value = value[1:-1]
        elif (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
            value = value.replace("''", "'")
    
    # Escape internal double quotes
    value = value.replace('\\"', '"')  # First unescape
    value = value.replace('"', '\\"')  # Then escape
    
    return f'"{value}"'

def fix_yaml_frontmatter(content):
    """Fix YAML front matter in a markdown file content."""
    frontmatter_text, rest = extract_frontmatter(content)
    
    if frontmatter_text is None:
        return content
    
    # Normalize the text: replace newlines with spaces for easier parsing
    # But preserve actual list structures
    normalized = re.sub(r'\n', ' ', frontmatter_text)
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Parse the frontmatter
    parsed = parse_frontmatter_robust(normalized)
    
    if not parsed:
        return content
    
    # Build new frontmatter
    new_lines = []
    for key, value in parsed:
        if key == 'categories' or key == 'tags':
            items = parse_list_value(value)
            if items:
                new_lines.append(f'{key}:')
                for item in items:
                    new_lines.append(f'- {item}')
            else:
                new_lines.append(f'{key}: []')
        else:
            formatted = format_value(key, value)
            new_lines.append(f'{key}: {formatted}')
    
    # Reconstruct the content
    new_frontmatter = '\n'.join(new_lines)
    return f'---\n{new_frontmatter}\n---{rest}'


def validate_yaml(content):
    """Validate YAML frontmatter."""
    import yaml
    frontmatter_text, _ = extract_frontmatter(content)
    if frontmatter_text is None:
        return True, None
    try:
        yaml.safe_load(frontmatter_text)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)


def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_yaml_frontmatter(content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    posts_dir = '/home/unirdp/news/_posts'
    files = glob.glob(os.path.join(posts_dir, '*.md'))
    
    processed = 0
    errors = 0
    
    for filepath in sorted(files):
        if process_file(filepath):
            processed += 1
        else:
            errors += 1
    
    print(f"\nTotal files processed: {processed}")
    print(f"Errors: {errors}")
    
    # Validate all files
    print("\nValidating YAML...")
    invalid_count = 0
    for filepath in sorted(files):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        valid, error = validate_yaml(content)
        if not valid:
            print(f"Invalid YAML in {os.path.basename(filepath)}: {error}")
            invalid_count += 1
    
    print(f"Invalid files: {invalid_count}")


if __name__ == '__main__':
    main()
