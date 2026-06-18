from copystatic import remove_dir_contents, copy_directory_recursive
from generate_content import generate_pages_recursively

static_path = "./static"
public_path = "./public"
content_path = "./content"
markdown_paths = [
    "./content/index.md",
    "./content/blog/glorfindel/index.md",
    "./content/blog/tom/index.md",
    "./content/blog/majesty/index.md",
    "./content/contact/index.md",
]

def main() -> None:
    print("Deleting public directory...")
    remove_dir_contents(public_path)
    print()

    print("Copying static files to public directory...")
    copy_directory_recursive(static_path, public_path)
    print()

    print("Generating content...")
    generate_pages_recursively(content_path, "template.html", public_path)


if __name__ == "__main__":
    main()