import customtkinter as ctk

class ModifiedMixin:
    def _init(self):
        self.clearModifiedFlag()
        self.bind('<<Modified>>', self._beenModified)

    def _beenModified(self, event=None):
        if self._resetting_modified_flag: return
        self.clearModifiedFlag()
        self.beenModified(event)

    def beenModified(self, event=None):
        pass

    def clearModifiedFlag(self):
        self._resetting_modified_flag = True

        try:
            self._textbox.tk.call(self._textbox._w, 'edit', 'modified', 0)

        finally:
            self._resetting_modified_flag = False


class AutoResizeTextBox(ModifiedMixin, ctk.CTkTextbox):
    def __init__(self, root, button = None):
        ctk.CTkTextbox.__init__(self, root, height=50, undo=True, autoseparators=True, border_width=2)
        # Initialize the ModifiedMixin.
        self._init()
        self.root = root
        self.button = button
        self.bind("<Shift-Return>", self.shift_enter)
        self.bind("<KeyRelease-Return>", self.shift_enter)
        self.bind("<Return>", lambda e: "break")

    def beenModified(self, event=None):
        self.change_size_textbox(event)

    def change_size_textbox(self, event):
        cursor_index = self._textbox.count('1.0', 'end', 'displaylines')[0]
        new_height = (cursor_index * 15) + 15
        # print(cursor_index)
        # print(self.textbox_chat_frame.cget('height'))
        if new_height != self.cget('height') and self.cget('height') <= 105:
            if new_height >= 105:
                self.configure(height=105)
            else:
                self.configure(height=new_height)

    def shift_enter(self, event=None):
        if event is not None and event.keysym == 'Return' and event.state == 9:
            #self.change_size_textbox(event)
            pass
        elif event is not None and event.keysym == 'Return' and event.state == 8:
            if self.get("0.0", "end").strip():
                self.button.invoke()
