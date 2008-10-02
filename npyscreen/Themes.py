import ThemeManager

class DefaultTheme(ThemeManager.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'WHITE_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
    }

class ColorfulTheme(ThemeManager.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'RED_BLACK',
        'FORMDEFAULT' : 'YELLOW_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'LABEL'       : 'BLUE_BLACK',
        'LABELBOLD'   : 'YELLOW_BLACK',
        'CONTROL'     : 'GREEN_BLACK',
    }
