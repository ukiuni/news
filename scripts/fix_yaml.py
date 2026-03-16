#!/usr/bin/env python3
"""
Fix YAML front matter in Jekyll posts.
- Wraps values in double quotes
- Handles multi-line titles by merging them
- Escapes internal double quotes
"""

import os
import re
import glob
import yaml

def fix_yaml_frontmatter(content):
    """Fix YAML front matter in a markdown file content."""
    
    # Check if the file starts with front matter
    if not content.startswith('---'):
        return content
    
    # Find the end of the front matter
    # Match the second ---
    match = re.search(r'^---\s*\n(.*?)\n---\s*$', content, re.MULTILINE | re.DOTALL)
    if not match:
        return content
    
    frontmatter_raw = match.group(1)
    rest_of_content = content[match.end():]
    
    # First, we need to merge broken multi-line values
    # Lines that don't start with a known key and don't start with - (list item)
    # should be merged with the previous line
    
    known_keys = [
        'layout', 'title', 'date', 'categories', 'tags', 'source_url',
        'source_title', 'source_id', 'excerpt', 'hn_id', 'hn_score', 'hn_comments'
    ]
    
    lines = frontmatter_raw.split('\n')
    merged_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check if this line starts a new key
        is_new_key = False
        for key in known_keys:
            if stripped.startswith(key + ':'):
                is_new_key = True
                break
        
        # Also check for list items (lines starting with -)
        if stripped.startswith('-'):
            is_new_key = True
        
        if is_new_key or not merged_lines:
            merged_lines.append(line)
        else:
            # Merge with previous line (add a space between)
            if merged_lines:
                merged_lines[-1] = merged_lines[-1].rstrip() + ' ' + stripped
    
    # Now process each line
    fixed_lines = []
    i = 0
    while i < len(merged_lines):
        line = merged_lines[i]
        stripped = line.strip()
        
        # Handle list format: categories: [tech, world-news]
        if re.match(r'^(categories|tags):\s*\[.*\]', stripped):
            fixed_lines.append(line)
            i += 1
            continue
        
        # Handle list items
        if stripped.startswith('- '):
            fixed_lines.append(line)
            i += 1
            continue
        
        # Check if this is a key-value line
        key_match = re.match(r'^(\s*)([a-z_]+):\s*(.*)$', line)
        if key_match:
            indent = key_match.group(1)
            key = key_match.group(2)
            value = key_match.group(3).strip()
            
            # Collect additional lines if value continues
            # This shouldn't be needed after merge, but just in case
            
            if key in ['categories', 'tags'] and not value:
                # This is a list starting on next line
                fixed_lines.append(line)
                i += 1
                continue
            
            if not value:
                # Empty value, keep as is
                fixed_lines.append(line)
                i += 1
                continue
            
            # Check if value is already properly quoted
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                # Already quoted, but we should normalize to double quotes
                # Extract the inner value
                inner = value[1:-1]
                # Escape any unescaped double quotes inside
                inner = inner.replace('\\"', '"')  # First unescape
                inner = inner.replace('"', '\\"')  # Then escape all
                fixed_lines.append(f'{indent}{key}: "{inner}"')
                i += 1
                continue
            
            # Escape double quotes in the value
            value = value.replace('\\"', '"')  # First unescape any
            value = value.replace('"', '\\"')  # Then escape all
            
            # Wrap in double quotes
            fixed_lines.append(f'{indent}{key}: "{value}"')
            i += 1
            continue
        
        # Any other line (like just -)
        fixed_lines.append(line)
        i += 1
    
    # Reconstruct the content
    new_frontmatter = '\n'.join(fixed_lines)
    return f'---\n{new_frontmatter}\n---{rest_of_content}'


def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_yaml_frontmatter(content)
        
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    posts_dir = '/home/unirdp/news/_posts'
    files = glob.glob(os.path.join(posts_dir, '*.md'))
    
    modified_count = 0
    for filepath in sorted(files):
        if process_file(filepath):
            modified_count += 1
            print(f"Fixed: {os.path.basename(filepath)}")
    
    print(f"\nTotal files processed: {len(files)}")
    print(f"Files modified: {modified_count}")


if __name__ == '__main__':
    main()
