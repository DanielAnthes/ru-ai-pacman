
if __name__ == '__main__':

    """
    This script is used for combining the local assignment
    files with the central script files, and starting the
    pacman program.
    """

    import sys, os, re, importlib

    dir_local = os.getcwd()
    dir_central = os.path.join(dir_local, '..', 'scripts')
    sys.path.append(dir_central) # append the scripts dir to the path

    os.chdir(dir_central) # import pacman files from central scripts directory

    import pacman

    os.chdir(dir_local) # import asssignment files from local directory, overriding central files

    for file in os.listdir('.'):
        if file.endswith('.py') and file != os.path.basename(__file__):
            importlib.import_module(file[:-3])

    os.chdir(dir_central) # change back to central directory for script execution

    if len(sys.argv) == 1:
        args = re.split(r' *', input("Enter any command line arguments?"))
        sys.argv.extend([a for a in args if a != ''])
    args = pacman.readCommand(sys.argv[1:])  # Get game components based on input
    pacman.runGames(**args)
