import sys
from logging_settings.log_filters import DebugWarningLogFilter, CriticalLogFilter, ErrorLogFilter


logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '#%(levelname)-8s %(name)s:%(funcName)s - %(message)s'
        },
        'formatter_1': {
            'format': '[%(asctime)s] #%(levelname)-8s %(filename)s:'
                      '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
        },
        'formatter_2': {
            'format': '#%(levelname)-8s [%(asctime)s] - %(filename)s:'
                      '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
        },
        'formatter_3': {
            'format': '#%(levelname)-8s [%(asctime)s] - %(message)s'
        }
    },
    'filters': {
        'critical_filter': {
            '()': CriticalLogFilter,
        },
        'error_filter': {
            '()': ErrorLogFilter,
        },
        'debug_warning_filter': {
            '()': DebugWarningLogFilter,
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'stderr': {
            'class': 'logging.StreamHandler',
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'formatter_2',
            'filters': ['debug_warning_filter'],
            'stream': sys.stdout
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
            'mode': 'w',
            'level': 'DEBUG',
            'formatter': 'formatter_1',
            'filters': ['error_filter']
        },
        'critical_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/critical.log',
            'mode': 'w',
            'formatter': 'formatter_3',
            'filters': ['critical_filter']
        }
    },
    'loggers': {
        '__main__': {
            'level': 'INFO',
            'handlers': ['default']

        },
        'module_2': {
            'handlers': ['stdout']
        },
        'middlewares.middlewares': {
            'handlers': ['stderr', 'critical_file']
        }
    },
    'root': {
        'level': 'INFO',
        'formatter': 'default',
        'handlers': ['default']
    }
}