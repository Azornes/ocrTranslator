""" AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()

Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md

"""
import sys
import time
from ocrTranslate.assets import Assets as assets

try:
    import Tkinter as tk  # for Python2
except ImportError:
    import tkinter as tk  # for Python3

import customtkinter as ctk
from PIL import Image


class AnimatedGifButton(ctk.CTkButton):
    def __init__(self, root, gif_file, stop_icon, delay=0.04, size=(40, 40), hide=True):
        self.stop_icon = ctk.CTkImage(Image.open(stop_icon), size=size)
        ctk.CTkButton.__init__(self, root, text="", fg_color="transparent", border_width=0, anchor="left", command=self.start_button, image=self.stop_icon, width=size[0], height=size[1])
        self.root = root
        self.hide = hide
        self.gif_file = gif_file
        self.delay = delay  # Animation delay - try low floats, like 0.04 (depends on the gif in question)
        self.stop_animation = False  # Thread exit request flag
        self.started_animation = False  # Thread exit request flag
        self.size = size
        self.grid_saved = self.grid_info()
        self._num = 0

    def grid_save(self):
        self.grid_saved = self.grid_info()

    def grid_restore(self):
        self.grid(**self.grid_saved)

    def start_button(self, started_animation=None):
        if started_animation is not None:
            started_forced_animation = not started_animation
            if self.started_animation and started_forced_animation:
                self.started_animation = False
                self.stop()
            elif not self.started_animation and not started_forced_animation:
                self.started_animation = True
                self.start()
        else:
            if self.started_animation:
                self.started_animation = False
                self.stop()
            else:
                self.started_animation = True
                self.start()

    def start(self):
        """ Starts non-threaded version that we need to manually update() """
        self.start_time = time.time()  # Starting timer
        self.stop_animation = False
        if self.hide:
            self.grid_restore()
        self._animate()

    def stop(self):
        """ This stops the after loop that runs the animation, if we are using the after() approach """
        self.stop_animation = True
        if self.hide:
            self.grid_forget()

    def _animate(self):
        with Image.open(self.gif_file) as im:
            try:
                im.seek(self._num + 1)
                self.gif = ctk.CTkImage(light_image=im, dark_image=im, size=self.size)
                self.configure(image=self.gif)  # do something to im
                self._num += 1
            except EOFError:
                self._num = -1  # end of sequence
            if not self.stop_animation:  # If the stop flag is set, we don't repeat
                self.root.after(int(self.delay * 1000), self._animate)
            else:
                self.configure(image=self.stop_icon)

    def start_thread(self):
        """ This starts the thread that runs the animation, if we are using a threaded approach """
        from threading import Thread  # We only import the module if we need it
        self._animation_thread = Thread()
        self._animation_thread = Thread(target=self._animate_thread).start()  # Forks a thread for the animation

    def stop_thread(self):
        """ This stops the thread that runs the animation, if we are using a threaded approach """
        self.stop_animation = True

    def _animate_thread(self):
        """ Updates animation, if it is running as a separate thread """
        while self.stop_animation is False:  # Normally this would block mainloop(), but not here, as this runs in separate thread
            try:
                time.sleep(self.delay)
                self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # Looping through the frames
                self.configure(image=self.gif)
                self._num += 1
            except tk.TclError:  # When we try a frame that doesn't exist, we know we have to start over from zero
                self._num = 0
            except RuntimeError:
                sys.exit()
