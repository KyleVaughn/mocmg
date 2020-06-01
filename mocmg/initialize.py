import gmsh
import logging 

# Initialize logger and gmsh.
def initialize(option=None):
    if option == 'debug':
        log_level = logging.DEBUG
        gmsh_verbosity = 99
    elif option == 'warning':
        log_level = logging.WARNING
        gmsh_verbosity = 2
    elif option == 'silent':
        log_level = 60 # CRITICAL = 50
        gmsh_verbosity = 0
    else:
        log_level = logging.INFO
        gmsh_verbosity = 5 

    # logger
    #
    # create logger
    mocmgLogger = logging.getLogger('mocmg')
    mocmgLogger.setLevel(log_level)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('mocmg.log')
    fh.setLevel(log_level)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-10s: %(name)s - %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    mocmgLogger.addHandler(fh)
    mocmgLogger.addHandler(ch)

    # gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.option.setNumber("General.Verbosity", gmsh_verbosity)
