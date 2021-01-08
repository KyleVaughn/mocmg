"""Used to initialize both mocmg and gmsh and to set log message settings.

"""


import logging
import sys
import warnings


class LessThanFilter(logging.Filter):
    """Filters messages of level value less than exclusive_maximum.

    Args:
        exclusive_maximum (int): Numeric value of minimum message level to be logged.

    Example:
        LessThanFilter(logging.WARNING)

    Note:
        See `Python logging library <https://docs.python.org/3/library/logging.html>`_ documentation
        for logging level numeric values, or simply use 'logging.INFO', 'logging.WARNING', etc.

    """

    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


class CustomFormatter(logging.Formatter):
    """Specifies the format of log messages, including date, time, and colors using ANSI color codes.

    Args:
        debug (bool, optional): Enable printing of line numbers within the code where the message
            was written.

    Attributes:
        debug (bool): Enable printing of line numbers within the code where the message
            was written.

    """

    # Omitted from coverage due to no way to retrieve contents on screen.
    def __init__(self, debug=False):  # pragma no cover
        self.debug = debug

        purple = "\x1b[35;10m"
        green = "\x1b[32;10m"
        default = "\x1b[39;10m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        fmt = "%(asctime)s %(levelname)-10s: %(name)s - %(message)s"
        debugFmt = "%(asctime)s %(levelname)-10s: %(name)s - (line: %(lineno)d) %(message)s"

        if debug:
            theFormat = debugFmt
        else:
            theFormat = fmt

        self.FORMATS = {
            logging.DEBUG: green + theFormat + reset,
            logging.INFO: default + theFormat + reset,
            logging.WARNING: purple + theFormat + reset,
            logging.ERROR: bold_red + theFormat + reset,
            logging.CRITICAL: bold_red + theFormat + reset,
        }

    # Omitted from coverage due to no way to retrieve contents on screen.
    def format(self, record):  # pragma no cover
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


def initialize(verbosity="info", color=True):
    """Initializes the mocmg logger with the desired output options.

    Args:
        verbosity (str): Verbosity level for mocmg. All messages below this level will not be
            displayed. The levels are as follows:

            +-----------+----------------------------------------------------+
            |   Level   |   Description                                      |
            +===========+====================================================+
            |   silent  |   Don't output anything                            |
            +-----------+----------------------------------------------------+
            |   error   |   Display error messages only                      |
            +-----------+----------------------------------------------------+
            |   warning |   Display error and warning messages               |
            +-----------+----------------------------------------------------+
            |   info    |   Display error, warning, and info messages        |
            +-----------+----------------------------------------------------+
            |   debug   |   Display error, warning, info, and debug messages |
            +-----------+----------------------------------------------------+

        color (bool, optional): Display log messages with color coded levels.

    """
    if verbosity == "info":
        mocmgVerbosity = logging.INFO
    elif verbosity == "debug":
        mocmgVerbosity = logging.DEBUG
    elif verbosity == "warning":
        mocmgVerbosity = logging.WARNING
    elif verbosity == "error":
        mocmgVerbosity = logging.ERROR
    elif verbosity == "silent":
        mocmgVerbosity = 99
    else:
        warnings.warn(
            f"No verbosity option for '{verbosity}'. Defaulting to 'info'."
            + "Next time please choose from one of: "
            + "'silent', 'error', 'warning', 'info', or 'debug'"
        )
        mocmgVerbosity = logging.INFO

    # Get the root logger
    logger = logging.getLogger()
    # Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)
    # Format stdout and stderr based upon color and debug mode
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-10s: %(name)s - %(message)s", datefmt="%H:%M:%S"
    )
    debugFormatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-10s: %(name)s" + " - (line: %(lineno)d) %(message)s",
        datefmt="%H:%M:%S",
    )

    # Stdout
    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(mocmgVerbosity)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))

    # If stdout is terminal, color if desired. Otherwise, don't color.
    # Omitted from coverage due to no way to retrieve contents on screen.
    if color and sys.stdout.isatty():  # pragma no cover
        if verbosity == "debug":
            logging_handler_out.setFormatter(CustomFormatter(debug=True))
        else:
            logging_handler_out.setFormatter(CustomFormatter())
    else:
        if verbosity == "debug":
            logging_handler_out.setFormatter(debugFormatter)
        else:
            logging_handler_out.setFormatter(formatter)
    logger.addHandler(logging_handler_out)

    # Stderr
    logging_handler_err = logging.StreamHandler(sys.stderr)
    lvl = max(logging.WARNING, mocmgVerbosity)
    logging_handler_err.setLevel(lvl)

    # If stderr is terminal, color if desired. Otherwise, don't color.
    # Omitted from coverage due to no way to retrieve contents on screen.
    if color and sys.stderr.isatty():  # pragma no cover
        if verbosity == "debug":
            logging_handler_err.setFormatter(CustomFormatter(debug=True))
        else:
            logging_handler_err.setFormatter(CustomFormatter())
    else:
        if verbosity == "debug":
            logging_handler_err.setFormatter(debugFormatter)
        else:
            logging_handler_err.setFormatter(formatter)
    logger.addHandler(logging_handler_err)
