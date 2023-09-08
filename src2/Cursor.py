"""
Cursor class

Author: HenRick69
Date: 08/09/2023
"""

import pyautogui

class Cursor:
    """
    A class for controlling the cursor and performing mouse actions.
    
    This class provides functionality for controlling the cursor's position
    and performing mouse actions such as clicking, scrolling, and more.

    Attributes:
        screen_width (int): The width of the screen in pixels.
        screen_height (int): The height of the screen in pixels.
        sustained_state (boolean): State of the sustained click
    """

    def __init__(self):
        """
        Initializes the Cursor class.
        """
        self.screen_width = pyautogui.size().width
        self.screen_height = pyautogui.size().height
        self.sustained_state = False

    def move(self, x_normalized, y_normalized):
        """
        Move the cursor to a specified normalized position.

        Args:
            x_normalized (float): Normalized x-coordinate (0.0 to 1.0).
            y_normalized (float): Normalized y-coordinate (0.0 to 1.0).
        """
        x_pixel = int(x_normalized * self.screen_width)
        y_pixel = int(y_normalized * self.screen_height)
        pyautogui.moveTo(x_pixel, y_pixel)

    def left_click(self):
        """
        Perform a left mouse click.
        """
        pyautogui.click(button='left')

    def right_click(self):
        """
        Perform a right mouse click.
        """
        pyautogui.click(button='right')

    def sustained_left_click(self):
        """
        Perform a sustained left mouse click.
        """
        if not self.sustained_state:
            pyautogui.mouseDown(button='left')
            self.sustained_state = True
        else:
            pyautogui.mouseUp(button='left')
            self.sustained_state = False

    def scroll(self, amount, direction):
        """
        Scroll the mouse wheel by a specified amount.

        Args:
            amount (int): The number of steps to scroll.
            direction (str): The direction to scroll ('up' or 'down')
        """
        if direction == 'up':
            pyautogui.scroll(amount)
        elif direction == 'down':
            pyautogui.scroll(-amount)      

    def double_left_click(self):
        """
        Perform a double left mouse click.
        """
        pyautogui.doubleClick(button='left')
