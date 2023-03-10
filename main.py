import asyncio
import ctypes
import logging

import tkinter

from ocrTranslate.assets import Assets as assets
from ocrTranslate.config_files import google_api, google_free, path_to_Capture2Text_CLI_exe, chatGpt, baidu_client, deepL, multi_translators
from ocrTranslate.gui.complex_tk_gui import ComplexTkGui, result_boxes

import os
import time
import subprocess

from win32api import GetSystemMetrics
from threading import Thread
from queue import Queue
import keyboard

from PIL import ImageEnhance
from PIL import ImageGrab
from mss import mss

root = ComplexTkGui()

myappid = 'Azornes.ocrTranslator'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# subprocess.call(["C:\Program Files\AutoHotkey\AutoHotkey.exe", "na wierzchu.ahk"])

class MyCapture:
    def __init__(self, png):
        # Variables X and Y are used to register the position of the left mouse button
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.X2 = tkinter.IntVar(value=0)
        self.Y2 = tkinter.IntVar(value=0)
        self.sel = False
        # screen size
        # self.screenWidth = root.winfo_screenwidth()+1920
        # self.screenHeight = root.winfo_screenheight()
        self.screen_width = GetSystemMetrics(78)
        self.screen_height = GetSystemMetrics(79)
        print("screen width and height: " + str(self.screen_width) + "x" + str(self.screen_height))
        # Create the highest level container
        self.top = tkinter.Toplevel(root, width=self.screen_width, height=self.screen_height)
        # The maximization and minimization buttons are not displayed
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=self.screen_width, height=self.screen_height)

        # Show a screenshot on the full screen, take a screenshot on the screenshot on the full screen
        self.image = tkinter.PhotoImage(file=assets.path_to_tmp4)
        self.canvas.create_image(self.screen_width // 2, self.screen_height // 2, image=self.image)
        self.canvas.pack()

        # A position in which the left mouse button is pressed
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            # start screenshot
            self.sel = True

        self.canvas.bind('<Button-1>', onLeftButtonDown)

        # Move the left mouse button to display the selected area
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                # Delete the newly drawn graphic, otherwise when the mouse is moved it will be a black rectangle.
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except:
                pass
            # Draw a crosshair when the left button is not clicked
            r = self.canvas.create_line(0, event.y, self.screen_width, event.y, fill='white')
            c = self.canvas.create_line(event.x, 0, event.x, self.screen_height, fill='white')
            if not self.sel:
                # print(event.x, event.y, self.screenWidth, self.screenHeight)
                pass
            else:
                lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='orange')  # print(event.x, event.y, self.screenWidth, self.screenWidth)

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        def onMouseMove(event):  # Mouse movement without clicking, drawing crosshair lines.
            global r, c
            try:
                # Delete the newly drawn graphic, otherwise when the mouse is moved it's a black rectangle.
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception:
                pass
            # Draw cross-hairs without clicking the left mouse button.
            r = self.canvas.create_line(0, event.y, self.screen_width, event.y, fill='white')
            c = self.canvas.create_line(event.x, 0, event.x, self.screen_height, fill='white')

        self.canvas.bind('<Motion>', onMouseMove)

        def onEscPressd(event):
            self.top.destroy()

        self.canvas.bind('<Cancel>', onEscPressd)

        # Get the position where the mouse left button is lifted, save the screenshot of the region.
        def onLeftButtonUp(event):
            self.sel = False
            self.X2.set(event.x)
            self.Y2.set(event.y)
            try:
                self.canvas.delete(lastDraw)
            except Exception:
                pass

            # Consider a screenshot taken with the mouse left button pressed down from the lower right and lifted
            # from the upper left.
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])

            # pic = ImageGrab.grab((left + 1, top + 1, right, bottom)) #one monitor
            pic = ImageGrab.grab((left + 1, top + 1, right, bottom), all_screens=True)

            self.top.destroy()  # Close the top-level container.
            # Pop up the save screenshot dialog.
            # fileName = tkinter.filedialog.asksaveasfilename(title='????????????',
            # filetypes=[('image','*.jpg *.png')])
            if pic:
                pic.save(assets.path_to_tmp)
                pic.save(assets.path_to_tmp2)  # Close the current window.  # self.top.destroy()

        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.top.attributes("-topmost", True)
        self.top.focus_force()

    def get_text_from_ocr(self):
        def OCRGoogle(test):
            with open(assets.path_to_tmp, 'rb') as img:
                img2 = ImageEnhance.Image.open(img)
                result = google_api.ocr_by_google_api(img2)
                # self.showtextwindow(ja_text)
                return result

        def OCRBaiduu(test):
            with open(assets.path_to_tmp2, 'rb') as img:
                img = img.read()
                result = baidu_client.basicGeneral(img)
                result = get_result_text(result)
                return result

        def OCRCapture2Text(test):
            EXE_PATH = path_to_Capture2Text_CLI_exe
            result = subprocess.check_output(EXE_PATH + ' --image {path_to_tmp} '.format(path_to_tmp=assets.path_to_tmp) + '--output-format ${capture}')
            print(result.decode('UTF-8'))
            return result.decode('UTF-8')

        def OCRGoogleFree(test):
            with open(assets.path_to_tmp, 'rb') as img:
                import base64
                b64_string = base64.b64encode(img.read())
                result = google_free.ocr_google_free(b64_string.decode('utf-8'))
                # self.showtextwindow(ja_text)
                return result

        list_functions = [OCRGoogle, OCRBaiduu, OCRCapture2Text, OCRGoogleFree]
        list_states_of_switches = [root.switch_google_api.get(), root.switch_baidu.get(), root.switch_capture.get(), root.switch_google_free.get()]
        string_results = {0: "-Google API:\n", 1: "-Baidu:\n", 2: "-Capture2Text:\n", 3: "-Google Free:\n"}

        queues = [Queue() for _ in range(len(list_functions))]
        threads = []

        for i, func in enumerate(list_functions):
            if list_states_of_switches[i] == 1:
                print(func.__name__)
                t = Thread(target=lambda q, func, arg1: q.put(func(arg1)), args=(queues[i], func, 'world!'))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()

        result = ""
        for i, queue in enumerate(queues):
            if list_states_of_switches[i] == 1:
                if list_states_of_switches.count(1) == 1 and root.switch_game_mode.get() == 1:
                    result = queue.get()
                else:
                    result += string_results[i] + queue.get() + "\n\n"


        root.scrollable_frame_textbox.insert("0.0", result)
        if root.switch_results_to_clipboard.get() == 1:
            root.clipboard_clear()
            root.clipboard_append(result)
        # root.scrollable_frame_textbox.get('1.0', 'end')
        # if root.switch_from_text.get() == 1:
        #    results = root.scrollable_frame_textbox.get('1.0', 'end')

        if root.option_menu_translation.get() != "Disabled":
            translated = translate(result)
            self.show_text_window(translated)
        else:
            #    translated = "    Google API:\n\n" + result1 + "\n    Baidu:\n\n" + get_result_text(
            #        result2) + "\n    Capture:\n\n" + result3 + "\n\n    GooglePoint:\n\n" + result4
            #    root.scrollable_frame_textbox.insert("0.0",translated)
            self.show_text_window(result)

        # self.showtextwindow("BaiduOCR: \n\n" + getresulttext(result2) + "\nGooglVisionOCR: \n\n" + result1)

    def show_text_window(self, text):
        result_toplevel = tkinter.Toplevel()
        result_toplevel.title('OCR window')
        result_toplevel.iconbitmap(assets.path_to_icon2)

        if root.switch_game_mode.get() == 1:
            result_toplevel.overrideredirect(1)  # will remove the top badge of window
            result_toplevel.attributes('-topmost', 'true')
            # w = result_toplevel.winfo_width()
            # h = result_toplevel.winfo_height()

            result_toplevel.geometry("%dx%d+%d+%d" % (abs(self.X2.get() - self.X.get()), abs(self.Y2.get() - self.Y.get()), min(self.X.get(), self.X2.get()), abs(min(self.Y.get(), self.Y2.get()) - abs(self.Y2.get() - self.Y.get()))))

            # def topclose():
            #     resultboxes.remove(self)
            # result_toplevel.protocol('WM_DELETE_WINDOW', topclose)

            # L1 = tkinter.Label(result_toplevel, text='OCR Tekst???')
            # L1.pack()
            result_text = tkinter.Text(result_toplevel, width=abs(self.X2.get() - self.X.get()), height=abs(self.Y2.get() - self.Y.get()))

            def click(event):
                result_toplevel.destroy()

            result_text.bind('<Button-2>', click)
            result_text.insert(tkinter.END, text)
            result_text.pack()
            self.resultbox = tkinter.Message(result_toplevel)
            self.resultbox.pack()
            result_boxes.append(result_toplevel)
            print(text)

            result_toplevel.after(10000, lambda: result_toplevel.destroy())  # Destroy the widget after 30 seconds
        else:
            def top_close():
                result_toplevel.destroy()

            result_toplevel.protocol('WM_DELETE_WINDOW', top_close)

            L1 = tkinter.Label(result_toplevel, text='OCR Text???')
            L1.pack()

            result_text = tkinter.Text(result_toplevel, width=100, height=50)
            result_text.insert(tkinter.END, text)
            result_text.pack()
            self.resultbox = tkinter.Message(result_toplevel)
            self.resultbox.pack()
            result_boxes.append(result_toplevel)


def translate(results):
    translated = ""
    if root.option_menu_translation.get() == "GoogleFree":
        translated = google_free.translate_by_special_point_google(results, root.combobox_to_language.get())
    elif root.option_menu_translation.get() == "Deepl":
        translated = deepL.translate_by_special_point_deepL(results, root.combobox_from_language.get(), root.combobox_to_language.get())
    elif root.option_menu_translation.get() == "ChatGPT":
        translated = asyncio.run(chatGpt.translate_by_chat_gpt(results, root.combobox_to_language.get()))
    elif root.option_menu_translation.get() in ['alibaba', 'argos', 'baidu', 'bing', 'caiyun', 'google', 'iciba', 'iflytek', 'iflyrec', 'itranslate', 'lingvanex', 'mglip', 'modernMt', 'myMemory', 'niutrans', 'papago', 'qqFanyi', 'qqTranSmart', 'reverso', 'sogou', 'translateCom', 'utibet', 'volcEngine', 'yandex', 'youdao']:
        translated = multi_translators.translate(results, root.combobox_from_language.get(), root.combobox_to_language.get(), root.option_menu_translation.get())
    if root.switch_results_to_clipboard.get() == 1:
        root.clipboard_clear()
        root.clipboard_append(translated)
    root.translation_frame_textbox.insert("0.0", translated + "\n\n")
    return translated


def buttonCaptureClick():
    with mss() as sct:
        sct.shot(mon=-1, output=assets.path_to_tmp4)
    if root.switch_from_text.get() != 1 and root.switch_from_clipboard.get() != 1:
        root.state('icon')
        for box in result_boxes:
            try:
                box.state('icon')
            except Exception:
                pass
        time.sleep(0.2)
        filename = assets.path_to_tmp3
        im = ImageGrab.grab()
        im = ImageEnhance.Brightness(im).enhance(0.8)
        im.save(filename)
        im.close()

        w = MyCapture(filename)
        # buttonCapture.wait_window(w.top)
        root.button_start.wait_window(w.top)
        # pdb.set_trace()
        # result = w.getText()
        w.get_text_from_ocr()
        # printresult(result)

        root.state('normal')
        for box in result_boxes:
            try:
                box.state('normal')
            except Exception:
                pass
        os.remove(filename)
    else:
        if root.switch_from_text.get() == 1:
            translate(root.scrollable_frame_textbox.get('1.0', 'end'))
        else:
            translate(root.clipboard_get())


def get_result_text(json):
    s = ''
    if json.__contains__('words_result_num') and json['words_result_num'] > 0:
        for i in range(0, json['words_result_num']):
            s += json['words_result'][i]['words']
            s += '\r\n'
    else:
        # s += '"text not found"???'
        s += ''
    return s


def key(event):
    buttonCaptureClick()


keyboard.add_hotkey('alt+win+t', key, args=('From global keystroke',))
# root.bind('<Control-Alt-f>', key)

root.button_start.configure(command=buttonCaptureClick)

# buttonCapture = tkinter.Button(root, text='Start', command=buttonCaptureClick)
# buttonCapture.place(x=160, y=10, width=80, height=30)

try:
    root.mainloop()
except Exception as e:
    logging.exception("An exception was thrown!")
    root.destroy()
