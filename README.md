*Npyscreen is a python widget library and application framework for programming terminal or console applications.  It is built on top of ncurses, which is part of the standard library.*

# Information

I just copied the repo from [npcole/npyscreen](https://github.com/npcole/npyscreen) to tweak the framework just a tiny bit.


# Additions

## TitleDateCombo can now have an individual date format:

```python
Form.add(npyscreen.TitleDateCombo, name="Date:", dateFmt='%Y-%m-%d')
```