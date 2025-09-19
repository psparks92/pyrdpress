from textnode import *
from leafnode import *
from blocknode import *
from parentnode import *
from server_util import *


def main():
    migrate_files("static","public")
    generate_pages_recursive("content", "template.html", "public")

main()
