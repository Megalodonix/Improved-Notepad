from configparser import ConfigParser
import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *
conf = ConfigParser()
conf.read('settings.ini')


def change_fg_color():
    change_fg_color = colorchooser.askcolor(title="Pick a text color.")
    if change_fg_color == None:
        change_fg_color = conf.get('change_color', 'fg')

    else:
        change_fg_color = change_fg_color[1] # Your HEX is in index 1
        conf.set('change_color', 'fg', str(change_fg_color))
        if change_fg_color is None:
            change_fg_color = change_fg_color
        else:
            with open('settings.ini', 'w') as f:
                conf.write(f)
            text_area.config(fg=str(change_fg_color))


def change_bg_color():
    change_bg_color = colorchooser.askcolor(title="Pick a background color.")
    if change_bg_color == None:
        change_bg_color = conf.get('change_color', 'bg')

    else:
        change_bg_color = change_bg_color[1]
        conf.set('change_color', 'bg', str(change_bg_color))
        if change_bg_color is None:
            change_bg_color = change_bg_color
        else:
            with open('settings.ini', 'w') as f:
                conf.write(f)
            text_area.config(bg=str(change_bg_color))


def change_font(*args):
    conf.set('change_font', 'font_type', font_type.get())
    conf.set('change_font', 'font_size', font_size.get())
    with open('settings.ini', 'w') as f:
        conf.write(f)
    text_area.config(font=(font_type.get(), font_size.get()))

def reset_default_all():
    text_area.config(fg="#000000", bg="#FFFFFF")
    conf.set('change_color', 'fg', '#000000')
    conf.set('change_color', 'bg', '#FFFFFF')
    conf.set('change_font', 'font_type', 'Arial')
    conf.set('change_font', 'font_size', str(20))
    font_type.set("Arial"), font_size.set(str(20))
    text_area.config(font=(font_type.get(), font_size.get()))
    with open('settings.ini', 'w') as f:
        conf.write(f)

def new_file():
    confirm = askokcancel(title="Save before making a new file!",
                       message="You might have unsaved data, do you wish to continue?", icon="warning")
    if confirm is True:
        win.title("Untitled")
        text_area.delete(1.0, END)


def open_file():
    file = file2 = askopenfilename(defaultextension=".txt",
                           filetypes=[("All files", "*"),
                                      ("Text document", "*.txt")])
    try:
        file = open(file, "r")
        text_area.insert(1.0, file.read())
        file = file2
    except UnicodeError:
        showerror("Error", "This is not a valid file!")
    else:
        text_area.delete(1.0, END)
        win.title(os.path.basename(file))
        file = open(file, 'r')
        text_area.insert(1.0, file.read())
    finally:
        file.close()


def save_file():
    file = filedialog.asksaveasfilename(initialfile="Untitled.txt",
                                        defaultextension="*.txt",
                                        filetypes=[("All files", "*"),
                                                   ("Text document", "*.txt")])
    if file is None:
        return

    else:
        try:
            win.title(os.path.basename(file))
            file = open(file, "w")

            file.write(text_area.get(1.0, END))

        except AttributeError:
            showerror("Error", "Something went wrong.")

        finally:
            file.close()


def copy():
    text_area.event_generate("<<Copy>>")


def cut():
    text_area.event_generate("<<Cut>>")


def paste():
    text_area.event_generate("<<Paste>>")


def about():
    showinfo("About this program", "This is a -slightly- improved version of the notepad.\nMade by MK_Megalodonix (a silly little oomfie)\n\nCreation date: 2023/4/26")

def quit():
    win.destroy()
win = Tk()
win.title("Improved notepad")


file = None

win_width = 1000
win_height = 700
scr_width = win.winfo_screenwidth()
scr_height = win.winfo_screenheight()

x = int((scr_width / 2) - (win_width / 2))
y = int((scr_height / 2) - (win_height / 2))

win.geometry(f"{win_width}x{win_height}+{x}+{y}")

font_type = StringVar(win)
font_type.set(conf.get('change_font','font_type'))

font_size = StringVar(win)
font_size.set(conf.get('change_font','font_size'))

text_area = Text(win, font=(font_type.get(), font_size.get()))
text_area.config(fg=conf.get('change_color', 'fg'), bg=conf.get('change_color', 'bg'))


scrollbar = Scrollbar(text_area)

win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)

text_area.grid(sticky=N+E+S+W)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scrollbar.set)

frame = Frame(win)
frame.grid()

fg_change_button = Button(frame, text="Font color", command=change_fg_color)
fg_change_button.grid(row=1, column=0)

bg_change_button = Button(frame, text="Background color", command=change_bg_color)
bg_change_button.grid(row=1, column=1)

reset_button = Button(frame, text="Reset to default", command=reset_default_all)
reset_button.grid(row=1, column=2)

font_box = OptionMenu(frame, font_type, *font.families(), command=change_font)
font_box.grid(row=0, column=0, columnspan=1)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)
size_box.grid(row=0, column=1)


menubar = Menu(win)
win.config(menu=menubar)

file_menu = Menu(menubar, tearoff=FALSE)

menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

file_menu.add_separator()

file_menu.add_command(label="Exit", command=quit)

edit_menu = Menu(menubar, tearoff=FALSE)

menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

help_menu = Menu(menubar, tearoff=FALSE)

menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

win.mainloop()