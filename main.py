import asyncio
import ctypes
import logging

import tkinter

import configparser
import win32gui
from BlurWindow.blurWindow import blur

from ocrTranslate.assets import Assets as assets
from ocrTranslate.config_files import google_api, google_free, chatGpt, deepL, multi_translators, capture2Text, tesseract, baidu, rapid_ocr, config
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

# get current path
path = os.path.dirname(os.path.abspath(__file__))


# subprocess.call(["C:\Program Files\AutoHotkey\AutoHotkey.exe", "na wierzchu.ahk"])


class MyCapture:
    def __init__(self):
        # Variables X and Y are used to register the position of the left mouse button
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.X2 = tkinter.IntVar(value=0)
        self.Y2 = tkinter.IntVar(value=0)
        if root.seg_button_last_ocr_area.get() == "Off" or root.seg_button_last_ocr_area.get() == "On":
            self.sel = False
            # screen size
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
                self.X.set(event.x)
                self.Y.set(event.y)
                # start screenshot
                self.sel = True

            self.canvas.bind('<Button-1>', onLeftButtonDown)

            # Move the left mouse button to display the selected area
            def onLeftButtonMove(event):
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

            def onEscPressed(event):
                self.top.destroy()

            self.canvas.bind('<Cancel>', onEscPressed)

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
                if pic:
                    pic.save(assets.path_to_tmp)
                    pic.save(assets.path_to_tmp2)  # Close the current window.  # self.top.destroy()

                if root.seg_button_last_ocr_area.get() == "On":
                    config.read(assets.path_settings_gui)
                    dict_settings = {"last_ocr_area_x": str(self.X.get()), "last_ocr_area_y": str(self.Y.get()), "last_ocr_area_x2": str(self.X2.get()), "last_ocr_area_y2": str(self.Y2.get())}
                    if not config.has_section("settings"):
                        config.add_section("settings")
                    for key, value in dict_settings.items():
                        config.set("settings", key, value)
                    with open(assets.path_settings_gui, "w") as config_file:
                        config.write(config_file)
                    root.seg_button_last_ocr_area.set("Saved")

            self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)

            self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
            self.top.attributes("-topmost", True)
            self.top.focus_force()
        else:
            config.read(assets.path_settings_gui)
            self.X = tkinter.IntVar(value=int(config.get("settings", "last_ocr_area_x")))
            self.Y = tkinter.IntVar(value=int(config.get("settings", "last_ocr_area_y")))
            self.X2 = tkinter.IntVar(value=int(config.get("settings", "last_ocr_area_x2")))
            self.Y2 = tkinter.IntVar(value=int(config.get("settings", "last_ocr_area_y2")))

            left, right = sorted([self.X.get(), self.X2.get()])
            top, bottom = sorted([self.Y.get(), self.Y2.get()])

            pic = ImageGrab.grab((left + 1, top + 1, right, bottom), all_screens=True)
            if pic:
                pic.save(assets.path_to_tmp)
                pic.save(assets.path_to_tmp2)  # Close the current window.  # self.top.destroy()

    def get_text_from_ocr(self):
        def OCRGoogle(test):
            with open(assets.path_to_tmp, 'rb') as img:
                ocr_result = google_api.ocr_by_google_api(ImageEnhance.Image.open(img))
                return ocr_result

        def OCRBaiduu(test):
            with open(assets.path_to_tmp2, 'rb') as img:
                ocr_result = baidu.ocr_by_baidu(img.read())
                return ocr_result

        def OCRCapture2Text(test):
            ocr_result = capture2Text.ocr_by_capture2text()
            return ocr_result.decode('UTF-8')

        def OCRGoogleFree(test):
            with open(assets.path_to_tmp, 'rb') as img:
                ocr_result = google_free.ocr_google_free(img)
                return ocr_result

        def OCRWindows(test):
            command = "{path_to_win_ocr} -Path '{path_to_tmp}' | Select-Object -ExpandProperty Text".format(path_to_tmp=assets.path_to_tmp2, path_to_win_ocr=assets.path_to_win_ocr)
            ocr_result = subprocess.check_output(["powershell.exe", command])
            try:
                result_text = ocr_result.decode("cp852").strip()
            except UnicodeDecodeError:
                result_text = "Error decoding"
            return result_text

        def OCRTesseract(test):
            ocr_result = tesseract.ocr_by_tesseract(assets.path_to_tmp2)
            return ocr_result

        def OCRRapid(test):
            ocr_result = rapid_ocr.ocr_by_rapid(assets.path_to_tmp2)
            return ocr_result

        list_functions = [OCRGoogle, OCRBaiduu, OCRCapture2Text, OCRGoogleFree, OCRWindows, OCRTesseract, OCRRapid]
        list_states_of_switches = [root.switch_ocr_google_api.get(), root.switch_ocr_baidu_api.get(), root.switch_ocr_capture2text.get(), root.switch_ocr_google_free.get(), root.switch_ocr_windows_local.get(), root.switch_ocr_tesseract.get(), root.switch_ocr_rapidocr.get()]
        string_results = {0: "-Google API:\n", 1: "-Baidu:\n", 2: "-Capture2Text:\n", 3: "-Google Free:\n", 4: "-Windows OCR:\n", 5: "-Tesseract:\n", 6: "-Rapid OCR:\n"}

        queues = [Queue() for _ in range(len(list_functions))]
        threads = []

        for i, func in enumerate(list_functions):
            if list_states_of_switches[i] == 1:
                # print(func.__name__)
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

        root.scrollable_frame_textbox.insert("0.0", result + "\n\n")
        if root.switch_results_to_clipboard.get() == 1:
            root.clipboard_clear()
            root.clipboard_append(result)

        def translate_from_ocr():
            if root.option_menu_translation.get() != "Disabled":
                translated = translate(result)
                self.show_text_window(translated)
            else:
                self.show_text_window(result)

        thread = Thread(target=translate_from_ocr)
        thread.start()

    def show_text_window(self, text):
        if root.switch_game_mode.get() == 1:
            def destroy_result(event):
                result_toplevel.destroy()

            def start_move(event):
                result_toplevel.x = event.x
                result_toplevel.y = event.y

            def stop_move(event):
                result_toplevel.x = None
                result_toplevel.y = None

            def do_move(event):
                deltax = event.x - result_toplevel.x
                deltay = event.y - result_toplevel.y
                x = result_toplevel.winfo_x() + deltax
                y = result_toplevel.winfo_y() + deltay
                result_toplevel.geometry(f"+{x}+{y}")

            # result_toplevel = customtkinter.CTkToplevel()
            result_toplevel = tkinter.Toplevel()
            result_toplevel.title('OCR window')
            result_toplevel.overrideredirect(1)  # will remove the top badge of window
            result_toplevel.attributes('-topmost', 'true')
            result_toplevel.wm_attributes('-transparentcolor', "#202020")

            width_geometry = abs(self.X2.get() - self.X.get())
            height_geometry = abs(self.Y2.get() - self.Y.get())
            coordinate_x_geometry = min(self.X.get(), self.X2.get())
            coordinate_y_geometry = abs(min(self.Y.get(), self.Y2.get()) - abs(self.Y2.get() - self.Y.get()))
            result_toplevel.geometry("%dx%d+%d+%d" % (width_geometry, height_geometry, coordinate_x_geometry, coordinate_y_geometry))
            result_toplevel.configure(bg="#202020")

            def stroke_text(text, textcolor, strokecolor, fontsize):
                xy = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                max_width = int(canvas.cget('width'))
                font_size = fontsize
                length_of_one_char = fontsize * 0.7
                font = ('Helvetica', font_size, 'bold')
                line = ""
                lines = []
                for i, char in enumerate(text):
                    line += char
                    text_width = canvas.create_text(0, 0, anchor="nw", text=line, font=font, tags=("text",))
                    width = canvas.bbox(text_width)[2] - canvas.bbox(text_width)[0]
                    canvas.delete(text_width)
                    if char == "\n" or width > max_width:
                        lines.append(line.replace("\n", ""))
                        line = ""
                    elif char == " ":
                        next_word = ""
                        for next_char in text[i + 1:]:
                            if next_char == " ":
                                break
                            next_word += next_char
                        text_width = canvas.create_text(0, 0, anchor="nw", text=next_word, font=font, tags=("text",))
                        next_width = canvas.bbox(text_width)[2] - canvas.bbox(text_width)[0]
                        canvas.delete(text_width)
                        if width + next_width > max_width:
                            lines.append(line[:-1])
                            line = char
                if line:
                    lines.append(line)
                text2 = "\n".join(lines)
                if '\n' in text2:
                    lines2 = text2.split('\n')
                    for i in range(len(lines2)):
                        for x, y in xy:
                            canvas.create_text((canvas.winfo_reqwidth() // 2) + x, length_of_one_char + y + i * 20, text=lines2[i], font=font, fill=strokecolor)
                        canvas.create_text(canvas.winfo_reqwidth() // 2, length_of_one_char + i * 20, text=lines2[i], font=font, fill=textcolor)
                else:
                    text_width = canvas.create_text(0, 0, anchor="nw", text=text2, font=font, tags=("text",))
                    width = canvas.bbox(text_width)[2] - canvas.bbox(text_width)[0]
                    height = canvas.bbox(text_width)[3] - canvas.bbox(text_width)[1]
                    canvas.delete(text_width)
                    canvas.config(width=width, height=height)
                    result_toplevel.geometry("%dx%d+%d+%d" % (width, height, (width_geometry - width) / 2 + coordinate_x_geometry, (height_geometry - height) + coordinate_y_geometry))
                    for x, y in xy:
                        canvas.create_text((canvas.winfo_reqwidth() // 2) + x, length_of_one_char + y, text=text2, font=font, fill=strokecolor)
                    canvas.create_text(canvas.winfo_reqwidth() // 2, length_of_one_char, text=text2, font=font, fill=textcolor)

            canvas = tkinter.Canvas(result_toplevel, bg='#202020', width=width_geometry, height=height_geometry)
            # determination of the font size based on the window size
            font_size = 1
            while True:
                font = ("Helvetica", font_size)
                text_width = canvas.create_text(0, 0, anchor="nw", text=text, font=font, tags=("text",))
                width = canvas.bbox(text_width)[2] - canvas.bbox(text_width)[0]
                height = canvas.bbox(text_width)[3] - canvas.bbox(text_width)[1]
                canvas.delete(text_width)
                if width > int(canvas.cget('width')) or height > int(canvas.cget('height')):
                    font_size -= 3
                    break
                font_size += 1
            if font_size < 10:
                font_size = 10
            stroke_text(text, 'white', 'black', font_size)
            canvas.configure(borderwidth=0, highlightthickness=0, relief="flat")
            canvas.bind('<Button-2>', destroy_result)
            canvas.bind("<ButtonPress-1>", start_move)
            canvas.bind("<ButtonRelease-1>", stop_move)
            canvas.bind("<B1-Motion>", do_move)
            canvas.pack()
            # print(canvas.cget('width'))
            # canvas.cget('height')

            # result_text = tkinter.Text(result_toplevel, width=abs(self.X2.get() - self.X.get()), height=abs(self.Y2.get() - self.Y.get()))
            # result_text.configure(font=("Arial", 13, "bold"), fg="white", bg="black", borderwidth=0, highlightthickness=0, relief="flat")

            # result_text = customtkinter.CTkTextbox(result_toplevel, width=abs(self.X2.get() - self.X.get()), height=abs(self.Y2.get() - self.Y.get()))
            # helv36 = customtkinter.CTkFont(family="Helvetica", size=13, weight="bold")
            # result_text.configure(font=helv36, text_color="white", fg_color="transparent", bg_color="#60b26c", border_spacing=0)

            # result_text.bind('<Button-2>', destroy_result)
            # result_text.bind("<ButtonPress-1>", start_move)
            # result_text.bind("<ButtonRelease-1>", stop_move)
            # result_text.bind("<B1-Motion>", do_move)
            # result_text.insert(tkinter.END, text)
            # result_text.pack(ipadx=0, ipady=0, padx=0, pady=0)
            self.resultbox = tkinter.Message(result_toplevel)
            self.resultbox.pack()
            result_boxes.append(result_toplevel)
            hWnd = win32gui.GetParent(result_toplevel.winfo_id())
            # blur(hWnd, hexColor='#12121240')
            blur(hWnd)
            result_toplevel.after(60000, lambda: result_toplevel.destroy())  # Destroy the widget after 60 seconds
        elif root.switch_window_mode.get() == 1:
            result_toplevel = tkinter.Toplevel()
            result_toplevel.title('OCR window')
            result_toplevel.iconbitmap(assets.path_to_icon2)

            def top_close():
                result_toplevel.destroy()

            result_toplevel.protocol('WM_DELETE_WINDOW', top_close)
            L1 = tkinter.Label(result_toplevel, text='OCR Text：')
            L1.pack()
            result_text = tkinter.Text(result_toplevel, width=100, height=50)
            result_text.insert(tkinter.END, text)
            result_text.pack()
            self.resultbox = tkinter.Message(result_toplevel)
            self.resultbox.pack()
            result_boxes.append(result_toplevel)


async def display_translations_ChatGPT(word, language_to="English"):
    root.translation_frame_textbox.insert("0.0", "\n\n")
    final_result = ""
    line_num = 0
    async for response in chatGpt.translate_by_chat_gpt_async(word, language_to):
        if "\n" in response:
            root.translation_frame_textbox.insert(f"{line_num}.0 lineend", response)
            line_num += 2
        else:
            root.translation_frame_textbox.insert(f"{line_num}.0 lineend", response)

        final_result += response
    return final_result


def translate(results):
    root.loading_icon.start()
    translated = ""
    if root.option_menu_translation.get() == "GoogleFree":
        translated = google_free.translate_by_special_point_google(results, root.combobox_to_language.get())
    elif root.option_menu_translation.get() == "DeepL":
        translated = deepL.translate_by_special_point_deepL(results, root.combobox_from_language.get(), root.combobox_to_language.get())
    elif root.option_menu_translation.get() == "ChatGPT":
        translated = asyncio.run(display_translations_ChatGPT(results, root.combobox_to_language.get()))
    elif root.option_menu_translation.get() in ['alibaba', 'argos', 'baidu', 'bing', 'caiyun', 'google', 'iciba', 'iflytek', 'iflyrec', 'itranslate', 'lingvanex', 'mglip', 'modernMt', 'myMemory', 'niutrans', 'papago', 'qqFanyi', 'qqTranSmart', 'reverso', 'sogou', 'translateCom', 'utibet', 'volcEngine', 'yandex', 'youdao']:
        translated = multi_translators.translate(results, root.combobox_from_language.get(), root.combobox_to_language.get(), root.option_menu_translation.get())
    if root.switch_results_to_clipboard.get() == 1:
        root.clipboard_clear()
        root.clipboard_append(translated)
    elif root.option_menu_translation.get() != "ChatGPT":
        root.translation_frame_textbox.insert("0.0", translated + "\n\n")
    root.loading_icon.stop()
    return translated


def translate_without_ocr():
    if root.switch_from_text.get() == 1:
        translate(root.scrollable_frame_textbox.get('1.0', 'end'))
    else:
        translate(root.clipboard_get())


def handle_app_windows(win_state):
    if win_state == 'normal' and root.state() == 'normal':
        root.state('icon')
        for box in result_boxes:
            try:
                box.state('icon')
            except Exception:
                pass
    elif win_state == 'normal':
        root.state('normal')
        for box in result_boxes:
            try:
                box.state('normal')
            except Exception:
                pass


def buttonCaptureClick():
    load_hotkey()
    win_state = root.state()
    if root.switch_from_text.get() != 1 and root.switch_from_clipboard.get() != 1:
        handle_app_windows(win_state)
        with mss() as sct:
            sct.shot(mon=-1, output=assets.path_to_tmp4)
        time.sleep(0.2)
        w = MyCapture()
        if root.seg_button_last_ocr_area.get() != "Saved":
            root.button_start.wait_window(w.top)
        w.get_text_from_ocr()
        handle_app_windows(win_state)
    else:
        thread = Thread(target=translate_without_ocr)
        thread.start()


def key(event):
    buttonCaptureClick()


def load_hotkey():
    config.read(assets.path_settings_gui)
    try:
        keyboard.clear_all_hotkeys()
    except AttributeError:
        pass
    try:
        if config.get("settings", "entry_binding_start_ocr") != "":
            keyboard.add_hotkey(config.get("settings", "entry_binding_start_ocr"), key, args=('From global keystroke',))
        else:
            keyboard.add_hotkey('alt+win+t', key, args=('From global keystroke',))
    except KeyError:
        keyboard.add_hotkey('alt+win+t', key, args=('From global keystroke',))


load_hotkey()
root.button_start.configure(command=buttonCaptureClick)

try:
    root.mainloop()
except Exception as e:
    logging.exception("An exception was thrown!")
    root.destroy()
