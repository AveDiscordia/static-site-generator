import sys
from copystatic import remove_dir_contents, copy_directory_recursive
from generate_content import generate_pages_recursively

static_path = "./static"
dest_dir_path = "./docs"
dir_path_content = "./content"
template_path = "template.html"

def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    remove_dir_contents(dest_dir_path)
    print()

    print("Copying static files to public directory...")
    copy_directory_recursive(static_path, dest_dir_path)
    print()

    print("Generating content...")
    generate_pages_recursively(basepath, dir_path_content, template_path, dest_dir_path)


if __name__ == "__main__":
    main()