import os
from selenium import webdriver
from sys import stdin, stdout

from browser import login, browse_to_document, browse_to_folder, logout
from command_line import CommandLineException, authenticate, cd_command, find_command, ls_command, more_command, pwd_command, rm_command, upload_command
from utils.nav_utils import get_cur_dir_id, getFile

command_to_func = {
    'cd': cd_command,
    'find': find_command,
    'ls': ls_command,
    'more': more_command,
    'pwd': pwd_command,
    'rm': rm_command,
    'upload': upload_command,
}

def open_file(driver, service, folder_name):
    f = getFile(service, folder_name)
    file_id = f['id']
    browse_to_document(driver, file_id)

def main():
    service = authenticate()
    driver = webdriver.Chrome()
    login(driver)
    stdout.write('Welcome to the Command-Drive terminal!' + os.linesep)

    while True:
        stdout.write('$ ')
        argv = stdin.readline().split()
        if len(argv) == 0:
            continue
        command = argv[0]
        if command == 'exit':
            break
        elif command == 'open':
            open_file(driver, service, argv[1])
        elif command in command_to_func:
            func = command_to_func[command]
            try:
                func(service, argv[1:])
            except CommandLineException as e:
                stdout.write('Error: {0}'.format(e) + os.linesep)
            if command in ('cd', 'rm', 'upload'):
                browse_to_folder(driver, get_cur_dir_id())
        else:
            stdout.write('Error: Unrecognized command: {0}'.format(' '.join(argv)) + os.linesep)

    stdout.write('Bye' + os.linesep)
    logout(driver)

if __name__ == '__main__':
    main()
