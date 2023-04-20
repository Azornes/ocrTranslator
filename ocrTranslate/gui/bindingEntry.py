import customtkinter as ctk
import keyboard


class BindingEntry(ctk.CTkEntry):
    def __init__(self, root, focus_on=None, hotkey_function=None):
        ctk.CTkEntry.__init__(self, root, placeholder_text="")
        # Initialize the ModifiedMixin.
        self.root = root
        self.focus_on = focus_on
        self.hotkey_function = hotkey_function
        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<ButtonPress>", self.on_mouse_press)

        self.key_combination = []

    def on_key_press(self, event):
        separator = "_"
        if separator in event.keysym:
            first_part, second_part = event.keysym.split(separator, 1)
            new_string = separator.join([first_part])
        else:
            new_string = event.keysym
        if new_string not in self.key_combination:
            self.key_combination.append(new_string)

        self.configure(state="normal", border_color="orange")
        self.delete(0, 'end')
        self.insert(0, "+".join(self.key_combination))
        self.configure(state="readonly")

    def on_key_release(self, event):
        self.configure(border_color="grey")
        self.focus_on.focus_set()
        self.key_combination = []
        try:
            keyboard.clear_all_hotkeys()
            keyboard.add_hotkey(self.get(), self.hotkey_function, args=('From global keystroke',))
        except AttributeError:
            pass

    def on_mouse_press(self, event):
        self.configure(state="readonly", border_color="orange")
