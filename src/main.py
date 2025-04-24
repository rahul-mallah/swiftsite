from textnode import *
from html_page_generator import *


def main():
    move_files("static", "public")
    generate_page_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
