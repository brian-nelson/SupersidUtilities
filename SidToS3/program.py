from workers.fileprocessor import FileProcessor
from configuration.config import Config

def getopts(argv):
    #Credit for function - https://gist.github.com/dideler/2395703
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

if __name__ == '__main__':
    from sys import argv

    #Get the args
    myargs = getopts(argv)

    configFilename = ""
    if '-c' in myargs:
        configFilename = myargs['-c']

    config = Config(configFilename)

    loader = FileProcessor(config)
    processed_files = loader.process()

