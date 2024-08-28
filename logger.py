import logging
import coloredlogs

level_styles = {
    'debug': {'color': 'cyan'},
    'info': {'color': 'blue'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True},
}


def configure_logging():
    coloredlogs.install(level='INFO', level_styles=level_styles)


def get_logger(name):
    return logging.getLogger(name)


# Call configure_logging to set up the colored logs
configure_logging()
