import shutil
import os
from markdown_to_html import *
from htmlnode import *
from pathlib import Path

def move_files(src, dest):
    # Delete dest and create main dest
    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.mkdir(dest)
    else:
        print(f"creating directory {dest}")
        os.mkdir(dest)

    # loop names of items in folder
    for name in os.listdir(src):
        # concat name to path
        src_item = os.path.join(src, name)
        dest_item = os.path.join(dest, name)
        # copy if it is a file else recursive call inside sub folder
        if os.path.isfile(src_item):
            print(f"Copying file from {src_item} to {dest_item}")
            shutil.copy(src_item, dest_item)
        else:
            move_files(src_item, dest_item)


def extract_title(markdown):
    # extract line starting from single #
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        line = line.strip()
        if line[:2] == "# ":
            title = line[2:]
            break
    
    if title:
        return title
    else:
        raise Exception("No title found")


def get_file_contents(file_path):
    with open(file_path) as f:
        return f.read()


def write_contents(file_path, contents):
    with open(file_path, "w") as f:
        f.write(contents)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read md and template files
    markdown_contents = get_file_contents(from_path)
    template_contents = get_file_contents(template_path)
    # convert md to html
    html_contents = markdown_to_html_node(markdown_contents).to_html()
    # extract h1 title
    title = extract_title(markdown_contents)
    # replace title and content to template contents
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_contents)
    # replace basepath in hyperlinks and images
    template_contents = template_contents.replace("href=\"/", f"href=\"{basepath}")
    template_contents = template_contents.replace("src=\"/", f"src=\"{basepath}")
    # create file and write contents
    write_contents(dest_path, template_contents)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for name in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, name)
        # check if it is md file then generate html page
        if os.path.isfile(src_path):
            if name.endswith(".md"):
                dest_path = os.path.join(dest_dir_path, name.replace(".md", ".html"))
                generate_page(src_path, template_path, dest_path, basepath) 
        else:
            # else create directory in dest
            dest_path = os.path.join(dest_dir_path, name)
            os.mkdir(dest_path)
            generate_page_recursive(src_path, template_path, dest_path, basepath)