import npyscreen
import curses

def sliderTest(screen):
    F = npyscreen.Form()
    F.add(npyscreen.TitleSlider, name="Slider 1")
    F.add(npyscreen.TitleSlider, color='STANDOUT', name="Slider 2")
    F.add(npyscreen.Slider, name="Slider 3")
    F.edit()



if __name__ == "__main__":
	curses.wrapper(sliderTest)