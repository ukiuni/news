#!/usr/bin/env python3
"""
Fix YAML front matter in Jekyll posts - Version 2.
- Wraps values in double quotes
- Handles multi-line titles by merging them properly
- Escapes internal double quotes
- Handles edge cases like lines starting with - that are not list items
"""

import os
import re
import glob

def fix_yaml_frontmatter(content):
    """Fix YAML front matter in a markdown file content."""
    
    # Check if the file starts with front matter
    if not content.startswith('---'):
        return content
    
    # Find the end of the front matter
    lines = content.split('\n')
    
    # Find the second ---
    end_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_idx = i
            break
    
    if end_idx == -1:
        return content
    
    frontmatter_lines = lines[1:end_idx]
    rest_lines = lines[end_idx:]  # includes the closing ---
    
    known_keys = [
        'layout', 'title', 'date', 'categories', 'tags', 'source_url',
        'source_title', 'source_id', 'excerpt', 'hn_id', 'hn_score', 'hn_comments'
    ]
    
    # First pass: merge broken multi-line values
    merged_lines = []
    for line in frontmatter_lines:
        stripped = line.strip()
        
        # Check if this line starts a new key
        is_new_key = False
        for key in known_keys:
            if stripped.startswith(key + ':'):
                is_new_key = True
                break
        
        # Check for list items that are actual list items (part of categories/tags)
        # These should have a certain indentation pattern
        if stripped.startswith('- ') and merged_lines:
            # Check if the previous line was categories: or tags: (without value)
            # or was itself a list item
            prev_stripped = merged_lines[-1].strip()
            is_list_item = False
            
            # If previous line was 'categories:' or 'tags:' with no value, this is a list item
            if prev_stripped in ['categories:', 'tags:']:
                is_list_item = True
            # If previous line was a list item at same or higher level, this is a list item
            elif prev_stripped.startswith('- '):
                is_list_item = True
            
            if is_list_item:
                merged_lines.append(line)
                continue
            # Otherwise, this is a continuation of the previous value
        
        if is_new_key or not merged_lines:
            merged_lines.append(line)
        else:
            # This line continues the previous value - merge with a space
            merged_lines[-1] = merged_lines[-1].rstrip() + ' ' + stripped
    
    # Second pass: quote all values
    fixed_lines = []
    i = 0
    while i < len(merged_lines):
        line = merged_lines[i]
        stripped = line.strip()
        
        # Handle list format like: categories: [tech, world-news]
        if re.match(r'^(categories|tags):\s*\[.*\]', stripped):
            fixed_lines.append(line)
            i += 1
            continue
        
        # Handle list items (lines starting with -)
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
            
            # For categories/tags with no inline value (list follows)
            if key in ['categories', 'tags'] and not value:
                fixed_lines.append(line)
                i += 1
                continue
            
            if not value:
                # Empty value, keep as is
                fixed_lines.append(line)
                i += 1
                continue
            
            # Remove existing quotes if present
            if (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            elif (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
                # Handle escaped single quotes inside
                value = value.replace("''", "'")
            
            # Unescape any existing escaped quotes
            value = value.replace('\\"', '"')
            # Now escape all double quotes
            value = value.replace('"', '\\"')
            
            # Wrap in double quotes
            fixed_lines.append(f'{indent}{key}: "{value}"')
            i += 1
            continue
        
        # Any other line
        fixed_lines.append(line)
        i += 1
    
    # Reconstruct the content
    result_lines = ['---'] + fixed_lines + rest_lines
    return '\n'.join(result_lines)


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
