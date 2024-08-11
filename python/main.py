import sys
import os
from shutil import move
from getpass import getuser
from threading import Thread

def main():
    argv = sys.argv[1:]
    user_dir = f"/Users/{getuser()}/Documents/CodeSnippets"
    cmd_file = f"{user_dir}/cmd.code"
    cmd = argv[0]

    def ensure_cmd_file():
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        if not os.path.exists(cmd_file):
            open(cmd_file, 'w').close()

    ensure_cmd_file()

    commands = []
    with open(cmd_file, 'r') as f:
        for line in f:
            name, path, prefix = line.strip().split(',')
            commands.append((name, path, prefix))

    def add_command(name, path, prefix=None):
        if name in [c[0] for c in commands] or name in ['add', 'delete', 'conf', ',']:
            raise ValueError(f"Command '{name}' is already used or reserved.")
        filename = path.split('/')[-1].lower()
        move(path, f"{user_dir}/{filename}")
        os.chmod(f"{user_dir}/{filename}", 0o755) if not prefix else None
        with open(cmd_file, 'a') as f:
            f.write(f"{name},{filename},{prefix or ''}\n")

    def delete_command(name):
        for i, (cmd_name, path, _) in enumerate(commands):
            if cmd_name == name:
                os.remove(f"{user_dir}/{path}")
                del commands[i]
                break
        else:
            raise ValueError(f"Command '{name}' not found.")
        with open(cmd_file, 'w') as f:
            for name, path, prefix in commands:
                f.write(f"{name},{path},{prefix}\n")

    def configure_command(old_name, new_name):
        if new_name in [c[0] for c in commands] or new_name in ['add', 'delete', 'conf', ',']:
            raise ValueError(f"New command name '{new_name}' is already used or reserved.")
        for i, (cmd_name, path, prefix) in enumerate(commands):
            if cmd_name == old_name:
                commands[i] = (new_name, path, prefix)
                break
        else:
            raise ValueError(f"Command '{old_name}' not found.")
        with open(cmd_file, 'w') as f:
            for name, path, prefix in commands:
                f.write(f"{name},{path},{prefix}\n")

    def update_command(name, path):
        for i, (cmd_name, _, prefix) in enumerate(commands):
            if cmd_name == name:
                filename = path.split('/')[-1].lower()
                os.remove(f"{user_dir}/{commands[i][1]}")
                move(path, f"{user_dir}/{filename}")
                os.chmod(f"{user_dir}/{filename}", 0o755) if not prefix else None
                commands[i] = (name, filename, prefix)
                break
        else:
            raise ValueError(f"Command '{name}' not found.")
        with open(cmd_file, 'w') as f:
            for name, path, prefix in commands:
                f.write(f"{name},{path},{prefix}\n")

    def execute_command(name, args):
        for cmd_name, path, prefix in commands:
            if cmd_name == name:
                cmd = f"{prefix} {path} {' '.join(args)}" if prefix else f"./{path} {' '.join(args)}"
                os.system(cmd)
                break
        else:
            raise ValueError(f"Command '{name}' not found.")

    if cmd == 'add':
        name, path, prefix = argv[1], argv[2], argv[3] if len(argv) > 3 else None
        add_command(name, path, prefix)
    elif cmd == 'delete':
        delete_command(argv[1])
    elif cmd == 'conf':
        configure_command(argv[1], argv[2])
    elif cmd == 'update':
        update_command(argv[1], argv[2])
    elif cmd in [c[0] for c in commands]:
        execute_command(cmd, argv[1:])
    elif cmd == 'help':
        print('...')  # Add help message
    else:
        raise ValueError(f"Unknown command: {cmd}")
    
if __name__ == "__main__":
    s = Thread(target=main)
    s.start()
    s.join()