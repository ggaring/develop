import os

def write_env(version_file, f):
    version_file.append(f)
    content = open(f, 'r')
    readme.write("#### {0}".format(f.rpartition("_")[0]))
    readme.write("\n")
    readme.write("``` {0} ```".format(content.readline().split("\n")[0]))
    readme.write("\n\n")
    content.close()


files = os.listdir(".")
version_file = []
readme = open("README.md", 'w')
readme.write("## Versions deployed by environment")
readme.write("\n\n")
for f in files:
    if f.endswith("_version"):
        write_env(version_file, f)
readme.write("\n")
readme.write("---")
readme.write("\n")
readme.write("_Captain Deployment says:_")
readme.write("\n")
readme.write("> This file is generated with the readme.py")

readme.close()
