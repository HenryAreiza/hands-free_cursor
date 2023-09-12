"""
Cursor class and mouse actions function

Author: HenryAreiza
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

def mouse_action(cursor_obj, position_obj, action, state, verbose=True):
    """
    Handle mouse actions based on voice commands.

    Args:
        cursor_obj (Cursor): An instance of the Cursor class for cursor control.
        position_obj (FacePosition): An instance of the FacePosition class for face detection and cursor positioning.
        action (str): The recognized voice command for mouse actions.
        state (bool): The current state of cursor movement.
        verbose (bool, optional): Controls whether action execution messages are printed. Default is True.

    Returns:
        bool: The updated state of cursor movement.
    """
    if action == "left":
        cursor_obj.left_click()
        if verbose:
            print("Left mouse click executed.")
    elif action == "right":
        cursor_obj.right_click()
        if verbose:
            print("Right mouse click executed.")
    elif action in ["up", "down"]:
        cursor_obj.scroll(position_obj.speed, action)
        if verbose:
            print(f"Mouse scroll ({action}) executed.")
    elif action == "go":
        cursor_obj.double_left_click()
        if verbose:
            print("Double left click executed.")
    elif action == "follow":
        cursor_obj.sustained_left_click()
        if verbose:
            if cursor_obj.sustained_state:
                print("Sustained left mouse click initiated.")
            else:
                print("Sustained left mouse click finished.")
    elif action == "on":
        if verbose:
            print("Cursor movement enabled.")
        return True
    elif action == "off":
        if verbose:
            print("Cursor movement disabled.")
        return False
    elif action == "one":
        position_obj.speed = 1
        if verbose:
            print("Cursor speed set to 'slow'.")
    elif action == "two":
        position_obj.speed = 2
        if verbose:
            print("Cursor speed set to 'medium'.")
    elif action == "three":
        position_obj.speed = 3
        if verbose:
            print("Cursor speed set to 'fast'.")
    elif action == "stop":
        if verbose:
            print('\nProgram finished.\n')
    else:
        if verbose:
            print('Unknown command.')
    return state