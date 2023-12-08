import platform

if platform.system() != "Darwin":
  from gpiozero import Button

button_pins = [19, 26, 16, 20, 21]

class PhysicalButtons:
    def __init__(self):
        if platform.system() == "Darwin":
            return
        
        self.__buttons = []
        for i in range(0, len(button_pins)):
            self.__buttons.append(Button(button_pins[i], bounce_time=0.2))
        
    def set_all(self, callback):
        if platform.system() == "Darwin":
            return
        
        for button in self.__buttons:
            button.when_pressed = callback
            
    def set(self, i, callback):
        if platform.system() == "Darwin":
            return
        
        self.__buttons[i].when_pressed = callback
    