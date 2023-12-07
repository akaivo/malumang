from gpiozero import Button

button_pins = [19, 26, 16, 20, 21]

class PhysicalButtons:
    def __init__(self):
        self.__buttons = []
        for i in range(0, len(button_pins)):
            self.__buttons.append(Button(button_pins[i], bounce_time=0.2))
        
    def set_all(self, callback):
        for button in self.__buttons:
            button.when_pressed = callback
            
    def set(self, i, callback):
        self.__buttons[i].when_pressed = callback
    