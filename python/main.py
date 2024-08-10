from sys import argv
from os.path import isfile,isdir
from os import mkdir,chdir,getcwd,system,access,X_OK,remove
from shutil import copy
from getpass import getuser
argv = argv[1:]

cwd = getcwd()
chdir(f"/Users/{getuser()}/Documents/CodeSnippets")

#defining and setting variables
folder = f"/Users/{getuser()}/Documents/CodeSnippets"
file = f"{folder}/cmd.code"
cmd = argv[0]
KEEP = ["add","delete","conf",","]
CMDLIST:list[str] = []
CMDRAW:list[str] = []
#check system used files and folder exists
def check():
    if not isdir(folder):
        mkdir(folder)
        open(file,"x").close()
    elif not isfile(file):
        open(file,"x").close()
check()
with open(file) as read:
    CMDRAW = read.readlines()
for i in range(0,len(CMDRAW)):
    CMDLIST.append(CMDRAW[i].split(",")[0])

#reset the folder path
def reset(cwd:str) -> None:
    chdir(cwd)
#adding new command
if cmd == "add":
    name = argv[1:][0]
    path = argv[1:][1]
    filename = path.split("/")[-1].lower()
    if name in KEEP or name in CMDLIST:
        raise ValueError(f"The command can't be these {KEEP} and {CMDLIST}")
    prefix = argv[3] if len(argv) == 4 else None
    copy(path,f"{folder}/{filename}")
    if access(f"{folder}/{filename}",X_OK):
        system(f"chmod +x {folder}/{filename}")
    else:
        prefix = argv[3]
    if name.lower() in CMDLIST and name.lower() in KEEP:
        raise ValueError("The command exists or reserved words")
    else:
        pass
    with open(file,"a") as write:
        write.write(f"{name.lower()},{filename},{prefix}\n")
    
#delete exists command
elif cmd == "delete":
    target = argv[1].lower()
    if target not in CMDLIST:
        raise ValueError("The command not exists")
    else:
        remove(f"{folder}/{CMDRAW[CMDLIST.index(target)].split(",")[1]}")
        CMDRAW.remove(CMDRAW[CMDLIST.index(target)])
        with open(file,"w") as write:
            write.writelines(CMDRAW)

#configure command (only name changing supported)
elif cmd == "conf":
    old, new = argv[1:]
    if old not in CMDLIST and new not in KEEP and new not in CMDLIST:
        pass
    else:
        raise ValueError("The command is not avaliable or used")

    cache:list[str] = []
    for cmdraw in CMDRAW:
        cache.append(cmdraw.replace(old,new,1))
    with open(file,"w") as write:
        write.writelines(cache)

#use noremal commands
elif cmd in CMDLIST:
    chdir(folder)
    cmd = cmd.lower()
    execute:str = ""
    items:list[set[str,str,str]] = []
    for a in CMDRAW:
        items.append((a.split(",")[0],a.split(",")[1],a.split(",")[2]))
    for i in items:
        if cmd in i:
            name,path,prefix = i
            prefix = prefix[:-1]
            if prefix != "None":
                execute += f"{prefix} {path} "
            else:
                execute += f"./{path}"
            for a in argv[2:]:
                execute += a+" "
        else:
            pass
    system(execute)
    chdir(cwd)

elif cmd == "help":
    print("Inputs must in lower case")
    print("This is a command manager\n and here's the command list")
    print("add [command name] [original file path (1)] {prefix}")
    print("delete [commands]")
    print("config [old name] [new name]")
    print("(other command) name {args} (2)")
    print("(1) if the origin file is executable, you don't need to enter the prefix command")
    print("(2) the args is not required,depends on the original file accepts args")
else:
    raise ValueError("Command not supported")