import os
import shutil
import generation
import sys

def delete_old_site():
    print("Deleting old site...")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    

def copy_over_static(source, destination):
    files = os.listdir(source)
    print(f"Creating new {destination} directory...")
    os.mkdir(destination)
    for file in files:
        if os.path.isfile(f"{source}/{file}"):
            print(f"Copying over {source}/{file}")
            shutil.copy(f"{source}/{file}", f"{destination}/{file}")
        else:
            copy_over_static(os.path.join(source, file), os.path.join(destination, file))

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"

    delete_old_site()
    print("Copying over static assets...")
    copy_over_static("static", "docs")
    generation.generate_pages_recursive("content", "template.html", "docs", basepath)

main()