import os
import shutil
import generation

def delete_old_site():
    print("Deleting old site...")
    if os.path.exists("public"):
        shutil.rmtree("public")
    

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
    delete_old_site()
    print("Copying over static assets...")
    copy_over_static("static", "public")
    generation.generate_page("content/index.md", "template.html", "public/index.html")

main()