from copystatic import remove_dir_contents, copy_directory_recursive
from generate_page import generate_page

static_path = "./static"
public_path = "./public"

def main() -> None:
    remove_dir_contents(public_path)
    print()
    copy_directory_recursive(static_path, public_path)
    print()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()