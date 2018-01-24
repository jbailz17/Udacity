import os

def rename_files():
    file_list = os.listdir(r"C:\Users\jbailz\Desktop\Web Development\Udacity\Programming Fundamentals and the web\prank")
    print(file_list)
    saved_path = os.getcwd()
    os.chdir(r"C:\Users\jbailz\Desktop\Web Development\Udacity\Programming Fundamentals and the web\prank")
    for file_name in file_list:
        os.replace(file_name,file_name.lstrip("0123456789"))
    os.chdir(saved_path)

rename_files()