from . import npysThemeManagers as ThemeManagers

class DefaultTheme(ThemeManagers.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'WHITE_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
        'WARNING'     : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
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
    }
