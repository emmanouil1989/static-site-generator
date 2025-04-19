import os
import shutil
from markdown_utils import markdown_to_html_node, extract_title
import sys

def main():
    basepath = sys.path[0] or '/'
    src = "./static"
    dst = "./public"
    if(os.path.exists(dst)):
        shutil.rmtree(dst)
    copy_files(src, dst)
    generate_pages_recursive(basepath,"content", "./template.html", "./public")
    

def copy_files(src, dst):
    list_of_directories = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    

    for i in range(len(list_of_directories)):
        if(os.path.isfile(f"{src}/{list_of_directories[i]}")):
            shutil.copy(f"{src}/{list_of_directories[i]}", f"{dst}/{list_of_directories[i]}")
        else:
            sub_directory_src = f"{src}/{list_of_directories[i]}"
            sub_directory_dst = f"{dst}/{list_of_directories[i]}"
            copy_files(sub_directory_src,sub_directory_dst)

def generate_page(basepath,from_path,template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    markdown_file = open(from_path,"r")
    template_file = open(template_path,"r")
    markdown = markdown_file.read()
    template = template_file.read()
    markdown_file.close()
    template_file.close()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    destination_file = open(dest_path,"w")
    destination_file.write(html)
    destination_file.close()

def generate_pages_recursive(basepath,dir_path_content, template_path, dest_dir_path):
    list_of_directories = os.listdir(dir_path_content)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    if len(list_of_directories) == 0:
        return
    
    for i in range(len(list_of_directories)):
        source = os.path.join(dir_path_content, list_of_directories[i])
        destination = os.path.join(dest_dir_path, list_of_directories[i])
        if(os.path.isfile(source)):
            if source.endswith(".md"):
                generate_page(basepath, source, template_path, destination.replace(".md", ".html"))
        else:
            sub_directory_src = os.path.join(dir_path_content, list_of_directories[i])
            sub_directory_dst = os.path.join(dest_dir_path, list_of_directories[i])
            generate_pages_recursive(basepath,sub_directory_src, template_path, sub_directory_dst)
main()
    