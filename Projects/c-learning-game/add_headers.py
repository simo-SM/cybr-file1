#!/usr/bin/env python3

import sys
import os
from datetime import datetime

def get_42_header(filename):
    """Generate a standard 42 header for the given filename."""
    basename = os.path.basename(filename)
    current_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    header = f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {basename:<51} :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: student <student@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {current_date} by student          #+#    #+#             */
/*   Updated: {current_date} by student         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

"""
    return header

def add_header_to_file(file_path):
    """Add 42 header to file if it doesn't already have one."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has a header
        if content.startswith('/*') and '************************************************************************' in content[:500]:
            print(f"Header already exists in {file_path}")
            return
        
        header = get_42_header(file_path)
        new_content = header + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added header to {file_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python add_headers.py <file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    add_header_to_file(file_path)

if __name__ == '__main__':
    main()
