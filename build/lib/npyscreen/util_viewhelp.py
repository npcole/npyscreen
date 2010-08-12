import textwrap


def view_help(message, title="Message", form_color="STANDOUT"):
    from . import fmForm
    from . import wgmultiline
    F = fmForm.Form(name=title, color=form_color)
    mlw = F.add(wgmultiline.Pager,)
    mlw_width = mlw.width-1
    message = textwrap.wrap(message, mlw_width)
    mlw.values = message
    F.edit()
    del wlw
    F.destroy()
    del F
    
