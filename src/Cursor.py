import pyautogui
import time

class Cursor:
    def __init__(self):
        self.screen_width = pyautogui.size().width
        self.screen_height = pyautogui.size().height
        
    def move(self, x_normalized, y_normalized):
        x_pixel = int(x_normalized * self.screen_width)
        y_pixel = int(y_normalized * self.screen_height)
        pyautogui.moveTo(x_pixel, y_pixel)
        
    def left_click(self):
        pyautogui.click(button='left')
        
    def right_click(self):
        pyautogui.click(button='right')
        
    def sustained_left_click(self, duration):
        pyautogui.mouseDown(button='left')
        time.sleep(duration)
        pyautogui.mouseUp(button='left')
        
    def scroll_up(self, amount):
        pyautogui.scroll(amount)
        
    def scroll_down(self, amount):
        pyautogui.scroll(-amount)
        
    def double_left_click(self):
        pyautogui.doubleClick(button='left')
