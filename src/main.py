from textnode import *
from leafnode import *
from blocknode import *
from parentnode import *
from server_util import *
import sys


def main():
    base_path = sys.argv[1]
    if not base_path:
        base_path = "/"
    print(base_path)
    migrate_files("static","docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)

main()
