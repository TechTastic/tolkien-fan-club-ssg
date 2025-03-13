from block import markdown_to_html_node
import os

def extract_title(markdown):
    headers = list(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    if not headers:
        raise Exception("invalid markdown, no title header")
    return headers[0].replace("#", "").strip()

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r").read()
    template_file = open(template_path, "r").read()

    content = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    
    final_html = template_file.replace(r"{{ Title }}", title).replace(r"{{ Content }}", content).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}").replace("<blockquote> \"". "<blockquote>\"")
    print(final_html)

    dir_paths = dest_path.split("/")
    dir_paths = dir_paths[:len(dir_paths) -1]
    dir_path = "/".join(dir_paths)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    f = open(dest_path, "x")
    f.write(final_html)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    directories = os.listdir(dir_path_content)
    for directory in directories:
        if os.path.isfile(f"{dir_path_content}/{directory}"):
            generate_page(f"{dir_path_content}/{directory}", "template.html", f"{dest_dir_path}/{directory}".replace(".md", ".html"), basepath)
        else:
            generate_pages_recursive(f"{dir_path_content}/{directory}", template_path, f"{dest_dir_path}/{directory}", basepath)
