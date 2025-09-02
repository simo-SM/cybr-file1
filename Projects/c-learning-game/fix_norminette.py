#!/usr/bin/env python3

import sys
import re
import os

def fix_file_common_issues(content):
    """Fix common norminette issues in C files."""
    lines = content.split('\n')
    result = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip header lines
        if line.startswith('/*') and i < 15:
            result.append(line)
            i += 1
            continue
        
        # Fix function declarations
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(', line):
            # Function declaration line - ensure proper format
            line = re.sub(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', r'\1\t\2(', line)
            # Fix pointer spaces
            line = re.sub(r'\*\s+', r'*', line)
            line = re.sub(r'\s+\*', r'\t*', line)
            
            # Check if function declaration ends with brace on same line
            if line.endswith('{'):
                result.append(line[:-1].rstrip())
                result.append('{')
            elif line.rstrip().endswith(') {'):
                result.append(line.replace(') {', ')'))
                result.append('{')
            else:
                result.append(line)
        
        # Fix variable declarations and assignments
        elif re.match(r'^\s*(const\s+)?[a-zA-Z_][a-zA-Z0-9_]*\s*\*?\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', line):
            # Variable declaration with assignment - split if needed
            parts = line.split('=', 1)
            if len(parts) == 2:
                decl = parts[0].strip()
                assign = parts[1].strip().rstrip(';')
                # Fix pointer placement
                decl = re.sub(r'\*\s+', r'*', decl)
                decl = re.sub(r'\s+\*', r'\t*', decl)
                result.append('\t' + decl + ';')
                var_name = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*(?=\s*=|\s*;)', decl)[-1]
                result.append(f'\t{var_name} = {assign};')
            else:
                line = re.sub(r'\*\s+', r'*', line)
                line = re.sub(r'\s+\*', r'\t*', line)
                result.append(line)
        
        # Fix return statements
        elif re.match(r'^\s*return\s+', line) and not re.match(r'^\s*return\s*\(', line):
            # Add parentheses around return value
            match = re.match(r'^(\s*)return\s+([^;]+);?$', line)
            if match:
                indent = match.group(1)
                value = match.group(2).strip()
                if value != '':
                    result.append(f'{indent}return ({value});')
                else:
                    result.append(f'{indent}return;')
            else:
                result.append(line)
        
        # Fix control structures
        elif re.match(r'^\s*(if|while|for)\s*\(', line):
            # Ensure space after keyword
            line = re.sub(r'^(\s*)(if|while|for)\s*\(', r'\1\2 (', line)
            
            # Check for statements on same line
            if line.count('{') > 0 or line.count(';') > 1:
                # Split into multiple lines
                if '{' in line:
                    parts = line.split('{', 1)
                    result.append(parts[0].rstrip())
                    result.append('\t{')
                    if len(parts) > 1 and parts[1].strip():
                        result.append('\t\t' + parts[1].strip())
                else:
                    result.append(line)
            else:
                result.append(line)
        
        # Fix multiple instructions per line
        elif ';' in line and line.count(';') > 1:
            # Split multiple statements
            statements = [s.strip() for s in line.split(';') if s.strip()]
            indent = re.match(r'^(\s*)', line).group(1)
            for stmt in statements:
                if stmt:
                    result.append(f'{indent}{stmt};')
        
        # Standard line processing
        else:
            # Fix pointer spacing
            line = re.sub(r'\*\s+([a-zA-Z_])', r'*\1', line)
            line = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s+\*', r'\1\t*', line)
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)

def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_norminette.py <file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_file_common_issues(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed norminette issues in {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
