import gmsh
import logging
import sys

# Filters messages of severity less than warning to stdout
class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        #non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


# Logging formatter to add colors using ANSI
class CustomFormatter(logging.Formatter):

    def __init__(self, option=None):
        self.option = option

        green = "\x1b[32;10m"
        default = "\x1b[39;10m"
        yellow = "\x1b[33;10m"
        red = "\x1b[31;10m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
                                                                                             
        fmt =      "%(asctime)s %(levelname)-10s: %(name)s - %(message)s'"
        debugFmt = "%(asctime)s %(levelname)-10s: %(name)s - (line: %(lineno)d) %(message)s"

        if option == 'debug':
            theFormat = debugFmt
        else:
            theFormat = fmt

        self.FORMATS = {
            logging.DEBUG:    green    + theFormat + reset,
            logging.INFO:     default  + theFormat + reset,
            logging.WARNING:  yellow   + theFormat + reset,
            logging.ERROR:    red      + theFormat + reset,
            logging.CRITICAL: bold_red + theFormat + reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


# Initialize mocmg logger and gmsh.
def initialize(mocmgOption=None,gmshOption=None, color=True):
    # mocmg
    if mocmgOption == 'debug':
        mocmgVerbosity = logging.DEBUG
    elif mocmgOption == 'warning':
        mocmgVerbosity = logging.WARNING
    elif mocmgOption == 'error':
        mocmgVerbosity = logging.ERROR
    else:
        mocmgVerbosity = logging.INFO

    # Get the root logger
    logger = logging.getLogger()
    # Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-10s: %(name)s - %(message)s', 
            datefmt='%H:%M:%S')
    debugFormatter = logging.Formatter(fmt='%(asctime)s %(levelname)-10s: %(name)s - (line: %(lineno)d) %(message)s', 
            datefmt='%H:%M:%S')

    # Stdout
    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(mocmgVerbosity)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    # If stdout is terminal, color if desired. Otherwise, don't color.
    if color and sys.stdout.isatty():
        if mocmgOption == 'debug':
            print(f'mocmgOption={mocmgOption}')
            logging_handler_out.setFormatter(CustomFormatter(option='debug'))
        else:
            logging_handler_out.setFormatter(CustomFormatter())
    else:
        if mocmgOption == 'debug':
            logging_handler_out.setFormatter(debugFormatter)
        else:
            logging_handler_out.setFormatter(formatter)
    logger.addHandler(logging_handler_out)

    # Stderr
    logging_handler_err = logging.StreamHandler(sys.stderr)
    lvl = max(logging.WARNING, mocmgVerbosity)
    logging_handler_err.setLevel(lvl)
    # If stderr is terminal, color if desired. Otherwise, don't color.
    if color and sys.stderr.isatty():
        if mocmgOption == 'debug':
            logging_handler_err.setFormatter(CustomFormatter('debug'))
        else:
            logging_handler_err.setFormatter(CustomFormatter())
    else:
        logging_handler_err.setFormatter(formatter)
    logger.addHandler(logging_handler_err)


    # gmsh
    if gmshOption == 'debug':
        gmshVerbosity = 99
    elif gmshOption == 'warning':
        gmshVerbosity = 2
    elif gmshOption == 'error':
        gmshVerbosity = 1
    elif gmshOption == 'silent':
        gmshVerbosity = 0
    else:
        gmshVerbosity = 5

    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
