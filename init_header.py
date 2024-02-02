import os
import shutil
import nbformat
import argparse
from pathlib import Path

def copy_folder(src_folder, dest_folder):
    # Check if destination folder already exists
    if os.path.exists(dest_folder):
        proceed = input(f"The folder {dest_folder} already exists. Overwrite? (yes/no(default)): ")
        if proceed.lower() not in ['yes', 'y']:
            print(f"Skipping copying {src_folder}")
            return
        # If overwrite is confirmed, remove the existing folder
        shutil.rmtree(dest_folder)
    
    # Copy the folder
    shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)
    print(f"Copied {src_folder} to {dest_folder}")

def copy_stylesheet(path):
    # Determine the parent folder of the provided path
    parent_folder = os.path.dirname(path)
    # Path to the style folder
    curruent_folder = os.path.dirname(os.path.abspath(__file__))
    style_folder = curruent_folder + "/style"

    # Copy style folder to the parent directory
    dest_folder = os.path.join(parent_folder, os.path.basename(style_folder))
    copy_folder(style_folder, dest_folder)

def copy_extensions(path):
    # Determine the parent folder of the provided path
    parent_folder = os.path.dirname(path)
    curruent_folder = os.path.dirname(os.path.abspath(__file__))
    # Path to the _extension folder
    extension_folder = curruent_folder + "/_extensions"

    # Copy _extension folder to the parent directory
    dest_folder = os.path.join(parent_folder, os.path.basename(extension_folder))
    copy_folder(extension_folder, dest_folder)


def modify_file(path, title, subtitle, self_contained):
    if path.endswith('.ipynb'):
        # Read the Jupyter Notebook
        with open(path, 'r', encoding='utf-8') as file:
            notebook = nbformat.read(file, as_version=4)

        # Prepare the new header content
        new_header = f"""---
title: "{title}"
subtitle: "{subtitle}"
author: "Kangheng Liu"
date: last-modified
date-format: long
format:
    html:
        theme:
            dark: 
                - cosmo
                - style/html-sta313.scss
                - style/html-dark.scss
                - style/my-adjustments.scss
            light: 
                - cosmo
                - style/html-sta313.scss
        toc: true
        code-copy: true
        code-overflow: wrap
        mainfont: "Atkinson Hyperlegible"
        code-annotations: hover
        self-contained: {str(self_contained).lower()}
execute:
    echo: true
    warning: false
    message: false
    freeze: auto
filters:
    - openlinksinnewpage
lightbox: auto
---"""

        # Check the first cell for existing header
        if notebook.cells:
            first_cell = notebook.cells[0]
            if first_cell.cell_type in ['markdown', 'raw'] and first_cell.source.startswith('---'):
                # Existing header found
                print("Existing header found:")
                print(first_cell.source)
                proceed = input("Overwrite? (yes/no(default)): ")
                if proceed.lower() == 'yes' or proceed.lower() == 'y':
                    # Replace the existing header
                    notebook.cells[0].source = new_header
                # If 'no', do nothing
            else:
                # No header found, insert new header as the first cell
                notebook.cells.insert(0, nbformat.v4.new_markdown_cell(new_header))
        else:
            # Notebook is empty, add new header as the first cell
            notebook.cells.append(nbformat.v4.new_markdown_cell(new_header))

        # Save the notebook
        with open(path, 'w', encoding='utf-8') as file:
            nbformat.write(notebook, file)


    elif path.endswith('.qmd'):
        # Read the QMD file
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # Prepare the new header content
        new_header = f"""---
title: "{title}"
subtitle: "{subtitle}"
author: "Kangheng Liu"
date: last-modified
date-format: long
format:
    html:
        theme:
            dark: 
                - cosmo
                - style/html-sta313.scss
                - style/html-dark.scss
                - style/my-adjustments.scss
            light: 
                - cosmo
                - style/html-sta313.scss
        toc: true
        code-copy: true
        code-overflow: wrap
        mainfont: "Atkinson Hyperlegible"
        code-annotations: hover
        self-contained: {str(self_contained).lower()}
execute:
    echo: true
    warning: false
    message: false
    freeze: auto
filters:
    - openlinksinnewpage
lightbox: auto
---\n"""
        # Check if the file starts with a header
        if lines and lines[0].startswith('---'):
            # Find the end of the header
            end_of_header_idx = lines.index('---\n', 1) if '---\n' in lines[1:] else None

            if end_of_header_idx:
                # Existing header found
                existing_header = ''.join(lines[:end_of_header_idx + 1])
                print("Existing header found:")
                print(existing_header)
                proceed = input("Overwrite? (yes/no(default)): ")
                
                if proceed.lower() != 'yes' or proceed.lower() == 'y':
                    return


                # Replace the existing header with the new header
                updated_content = new_header + ''.join(lines[end_of_header_idx + 1:])
            else:
                # No header end marker found, treat entire file as content
                updated_content = new_header + ''.join(lines)
        else:
            # No header found, prepend the new header
            updated_content = new_header + ''.join(lines)

        # Write the updated content back to the file
        with open(path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    
def process_files_in_directory(directory, title, subtitle, self_contained):
    for file in os.listdir(directory):
        if file.endswith('.ipynb') or file.endswith('.qmd'):
            file_path = os.path.join(directory, file)
            # Ask for confirmation before processing each file
            proceed = input(f"Do you want to process the file {file_path}? (yes(default)/no): ")
            if proceed.lower() in ['no', 'n']:
                print(f"Skipping {file_path}")
            elif proceed.lower() in ['yes', 'y', '']:
                print(f"Processing {file_path}")
                modify_file(file_path, title, subtitle, self_contained)
                copy_stylesheet(file_path)
                copy_extensions(file_path)
            else:
                raise ValueError(f"Invalid input: {proceed}")

def main(title, subtitle, self_contained, path):
    if os.path.isdir(path):
        process_files_in_directory(path, title, subtitle, self_contained)
    elif os.path.isfile(path) and (path.endswith('.ipynb') or path.endswith('.qmd')):
        # Ask for confirmation before processing the file
        proceed = input(f"Do you want to process the file {path}? (yes(default)/no): ")
        if proceed.lower() in ['no', 'n']:
            print(f"Skipping {path}")
        elif proceed.lower() in ['yes', 'y', '']:
            print(f"Processing {path}")
            modify_file(path, title, subtitle, self_contained)
            copy_stylesheet(path)
            copy_extensions(path)
        else:
            raise ValueError(f"Invalid input: {proceed}")
    else:
        print(f"The provided path is neither a directory nor a supported file type (.ipynb or .qmd): {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modify Jupyter Notebook or QMD file headers to my custom one, takes either a path to a directory or a supported file type (.ipynb or.qmd)")
    parser.add_argument("title", type=str, help="Title for the header")
    parser.add_argument("subtitle", type=str, help="Subtitle for the header")
    parser.add_argument("self_contained", type=str2bool, help="Self-contained boolean value")
    parser.add_argument("path", type=str, help="Path to the .ipynb or .qmd file or directory containing them")

    args = parser.parse_args()

    main(args.title, args.subtitle, args.self_contained, args.path)
