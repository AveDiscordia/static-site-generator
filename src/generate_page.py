import os
from markdown_to_html import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    raise ValueError("markdown file missing h1 header")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating webpage from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    with open(template_path, "r") as temp_file:
        template = temp_file.read()

    title: str = extract_title(markdown)
    content: str = markdown_to_html_node(markdown).to_html()
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as webpage:
        webpage.write(full_html)