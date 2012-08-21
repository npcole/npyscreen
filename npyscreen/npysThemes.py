from . import npysThemeManagers as ThemeManagers

class DefaultTheme(ThemeManagers.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'WHITE_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'YELLOW_BLACK',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
        'WARNING'     : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
    }

class ColorfulTheme(ThemeManagers.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'RED_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'YELLOW_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
        'WARNING'     : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_BLACK',
        'GOODHL'      : 'GREEN_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
        }

class BlackOnWhiteTheme(ThemeManagers.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'BLACK_WHITE',
        'FORMDEFAULT' : 'BLACK_WHITE',
        'NO_EDIT'     : 'BLUE_WHITE',
        'STANDOUT'    : 'CYAN_WHITE',
        'LABEL'       : 'BLUE_WHITE',
        'LABELBOLD'   : 'BLACK_WHITE',
        'CONTROL'     : 'GREEN_WHITE',
        'WARNING'     : 'RED_WHITE',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'GREEN_WHITE',
        'GOODHL'      : 'GREEN_WHITE',
        'VERYGOOD'    : 'WHITE_GREEN',
        'CAUTION'     : 'YELLOW_WHITE',
        'CAUTIONHL'   : 'BLACK_YELLOW',
    }

