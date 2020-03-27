import os
import subprocess
import settings

cmd = subprocess.run(["git", "describe", "--abbrev=0"], stdout=subprocess.PIPE)
version: str = cmd.stdout.decode("utf-8")
version = version.strip()

with open("version.py", "w", encoding="utf8", errors="ignore") as f:
    f.write("version = \"{}\"".format(version))

print("::set-output name=version::{}".format(version))

properties_file_content = ""
with open("build_properties_template.txt", 'r', encoding='utf8', errors='ignore') as f:
    properties_file_content = f.read()
properties_file_content = properties_file_content.replace("x.x.x.x", version)
properties_file_content = properties_file_content.replace("company_name", settings.company_name)
properties_file_content = properties_file_content.replace("file_description", settings.file_description)
properties_file_content = properties_file_content.replace("legal_copyright", settings.legal_copyright)
properties_file_content = properties_file_content.replace("original_filename", settings.app_executable_name)
properties_file_content = properties_file_content.replace("product_name", settings.app_name)
with open("tmp_build_properties.txt", 'w', encoding='utf8') as f:
    f.write(properties_file_content)

os.system("pyinstaller --onefile main.py --version-file=\"tmp_build_properties.txt\"")
filename = f"./dist/{settings.app_executable_name}"
if os.path.isfile(filename):
    os.remove(filename)
os.rename("./dist/main.exe", filename)


os.system("pyinstaller --onefile updater.py --version-file=\"tmp_build_properties.txt\"")
filename = f"./dist/{settings.updater_executable_name}"
if os.path.isfile(filename):
    os.remove(filename)
os.rename("./dist/updater.exe", filename)

os.remove("tmp_build_properties.txt")

