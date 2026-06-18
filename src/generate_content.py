import os
from pathlib import Path
from markdown_to_html import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise ValueError("markdown file missing h1 header")

def generate_page(from_path: str, template_path: str, dest_path: str | Path):
    print(f"Generating webpage from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    with open(template_path, "r") as temp_file:
        template = temp_file.read()

    title: str = extract_title(markdown)
    content: str = markdown_to_html_node(markdown).to_html()
    with_title = template.replace("{{ Title }}", title)
    full_html = with_title.replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as webpage:
        webpage.write(full_html)

def generate_pages_recursively(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursively(from_path, template_path, dest_path)