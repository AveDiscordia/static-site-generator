from copystatic import remove_dir_contents, copy_directory_recursive

static_path = "./static"
public_path = "./public"

def main() -> None:
    remove_dir_contents(public_path)
    print()
    copy_directory_recursive(static_path, public_path)

if __name__ == "__main__":
    main()