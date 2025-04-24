import sys
from textnode import *
from html_page_generator import *


def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    elif len(sys.argv) > 2:
        print(f"Usage: ./build.sh <basepath>")
        sys.exit(1)
    
    move_files("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
