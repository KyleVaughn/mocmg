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


# Initialize mocmg logger and gmsh.
def initialize(mocmgOption=None,gmshOption=None):
    # mocmg
    if mocmgOption == 'debug':
        mocmgVerbosity = logging.DEBUG
    elif mocmgOption == 'warning':
        mocmgVerbosity = logging.WARNING
    elif mocmgOption == 'silent':
        mocmgVerbosity = 50
    else:
        mocmgVerbosity = logging.INFO

    # Get the root logger
    logger = logging.getLogger()
    # Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-10s: %(name)s - %(message)s', datefmt='%H:%M:%S')

    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(logging.DEBUG)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    logging_handler_out.setFormatter(formatter)
    logger.addHandler(logging_handler_out)

    logging_handler_err = logging.StreamHandler(sys.stderr)
    logging_handler_err.setLevel(logging.WARNING)
    logging_handler_err.setFormatter(formatter)
    logger.addHandler(logging_handler_err)

    #demonstrate the logging levels
    log = logging.getLogger(__name__)
    log.debug('DEBUG')
    log.info('INFO')
    log.warning('WARNING')
    log.error('ERROR')
    log.critical('CRITICAL')

    # gmsh
    if gmshOption == 'debug':
        gmshVerbosity = 99
    elif gmshOption == 'warning':
        gmsh_verbosity = 2
    elif gmshOption == 'silent':
        gmsh_verbosity = 0
    else:
        gmsh_verbosity = 5 

    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmshVerbosity)
