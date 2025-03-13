from block import markdown_to_html_node
import os

def extract_title(markdown):
    headers = list(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    if not headers:
        raise Exception("invalid markdown, no title header")
    return headers[0].replace("#", "").strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r").read()
    template_file = open(template_path, "r").read()

    content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    
    final_html = template_file.replace(r"{{ Title }}", title).replace(r"{{ Content }}", content)

    #if not os.path.lexists(dest_path):
    #    os.makedirs("/".join(dest_path.split("/")[:1]))
    f = open(dest_path, "x")
    f.write(final_html)
    f.close()
