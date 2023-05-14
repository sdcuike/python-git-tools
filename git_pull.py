import os
import signal
import subprocess
import sys


def main():
    dir = sys.argv[1]
    cwd = os.getcwd()

    os.chdir(dir)
    child_dir = os.listdir(dir)

    for child in child_dir:
        if not os.path.isdir(child):
            continue

        os.chdir(child)
        print(os.getcwd())
        # os.system('git checkout master & git pull ')
        process = subprocess.run('git checkout master & git pull', shell=True, capture_output=True, text=True)
        if process.stdout:
            print(process.stdout)

        if process.stderr:
            print(process.stderr)

        os.chdir(dir)

    os.chdir(cwd)


if __name__ == '__main__':
    main()
