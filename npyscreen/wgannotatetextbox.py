from . import wgwidget
from .wgtextbox import Textfield



class AnnotateTextboxBase(wgwidget.Widget):
    """A base class intented for customization. Note in particular the annotationColor and annotationNoColor methods
    which you should override."""
    ANNOTATE_WIDTH = 5
    
    def __init__(self, screen, value = False, annotation_color='CONTROL', **keywords):
        self.value = value
        self.annotation_color = annotation_color
        super(AnnotateTextboxBase, self).__init__(screen, **keywords)
        
        self.text_area = Textfield(screen, rely=self.rely, relx=self.relx+self.ANNOTATE_WIDTH, 
                      width=self.width-self.ANNOTATE_WIDTH, value=self.name)
        if hasattr(self, 'display_value'):
            self.text_area.display_value = self.display_value
        self.show_bold = False
        self.highlight = False
        self.important = False
        self.hide      = False
    
    def getAnnotationAndColor(self):
        return ('xxx', 'CONTROL')
    
    def annotationColor(self):
        _annotation, _color = self.getAnnotationAndColor()
        self.parent.curses_pad.addstr(self.rely, self.relx, _annotation, self.parent.theme_manager.findPair(self, _color))

    def annotationNoColor(self):
        _annotation, _color = self.getAnnotationAndColor()
        self.parent.curses_pad.addstr(self.rely, self.relx, _annotation)

    def update(self, clear=True):
        if clear: 
            self.clear()
        if self.hidden:
            self.clear()
            return False
        if self.hide: 
            return True

        self.text_area.value = self.value

        if self.do_colors():    
            self.annotationColor()
        else:
            self.annotationNoColor()


        if self.editing:
            self.text_area.highlight = True
        else:
            self.text_area.highlight = False
        
        if self.show_bold: 
            self.text_area.show_bold = True
        else: 
            self.text_area.show_bold = False
            
        if self.important:
            self.text_area.important = True
        else:
            self.text_area.important = False

        if self.highlight: 
            self.text_area.highlight = True
        else: 
            self.text_area.highlight = False

        self.text_area.update(clear=clear)
        
    def calculate_area_needed(self):
        return 1,0
    



