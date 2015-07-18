import os
from sys import stdin, stdout

from command_line import CommandLineException, authenticate, cd_command, find_command, ls_command, more_command, pwd_command, rm_command

command_to_func = {
    'cd': cd_command,
    'find': find_command,
    'ls': ls_command,
    'more': more_command,
    'pwd': pwd_command,
    'rm': rm_command,
}

service = authenticate()
stdout.write('Welcome to the Command-Drive terminal!' + os.linesep)

while True:
    stdout.write('$ ')
    argv = stdin.readline().split()
    if len(argv) == 0:
        continue
    command = argv[0]
    if command == 'exit':
        break
    elif command in command_to_func:
        func = command_to_func[command]
        try:
            func(service, argv[1:])
        except CommandLineException as e:
            stdout.write('Error: {0}'.format(e) + os.linesep)
    else:
        stdout.write('Error: Unrecognized command: {0}'.format(' '.join(argv)) + os.linesep)

stdout.write('Bye' + os.linesep)
