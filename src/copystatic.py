import os
import shutil

def remove_dir_contents(dir_path: str) -> None:
    destination_contents: list[str] = os.listdir(dir_path)
    for path in destination_contents:
        path = os.path.join(dir_path, path)
        if os.path.isfile(path):
            print(f"deleting {path}")
            os.remove(path)
        else:
            print(f"recursively deleting {path}/")
            shutil.rmtree(path)

def copy_directory_recursive(source_dir_path: str, destination_dir_path: str) -> None:
    if not os.path.exists(destination_dir_path):
        os.mkdir(destination_dir_path)
    
    for filename in os.listdir(source_dir_path):
        from_source = os.path.join(source_dir_path, filename)
        to_destination = os.path.join(destination_dir_path, filename)
        if os.path.isfile(from_source):
            print(f"copying file {from_source} to {to_destination}")
            shutil.copy(from_source, to_destination)
        else:
            print(f"recursively copying directory {from_source}/ to {to_destination}/")
            copy_directory_recursive(from_source, to_destination)