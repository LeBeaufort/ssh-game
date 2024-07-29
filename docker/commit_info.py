import gitinfo
from json import dumps
from sys import argv

output_file = argv[1]
infos = gitinfo.gitinfo.get_git_info()

with open(output_file, "w") as file:
    file.write(dumps(infos))
