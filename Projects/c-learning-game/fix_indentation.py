#!/usr/bin/env python3

import sys
import re

def convert_indentation_to_tabs(content):
    """Convert leading spaces to tabs while preserving spaces within code."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.strip() == '':
            result.append('')
            continue
            
        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip(' '))
        rest_of_line = line[leading_spaces:]
        
        # Convert groups of 4 spaces to tabs
        tabs = leading_spaces // 4
        remaining_spaces = leading_spaces % 4
        
        new_line = '\t' * tabs + ' ' * remaining_spaces + rest_of_line
        result.append(new_line)
    
    return '\n'.join(result)

def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_indentation.py <file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = convert_indentation_to_tabs(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed indentation in {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
