import tkinter as tk
from tkinter import *
import ctypes
import re
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from tkterminal import Terminal
import pygments.lexers
from chlorophyll import CodeView
import threading


# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Tkinter
root = Tk()
root.geometry('800x600')
root.title("IDE-A (BETA 0.00001)")
title = "IDE-A (Beta 0.00001)"
root.state('zoomed')
root.iconbitmap('IDE_Logo.ico')
file_path = ''


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    root.title(f'IDE-A (Beta 0.00001) {file_path}')
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editArea.delete('1.0', END)
        editArea.insert('1.0', code)
        set_file_path(path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')


def save_as(arg):
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')



def run(arg):
    
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    else:
        os.system(f'start cmd /K "python {file_path}"')
        threading.Thread(target=run).start(1)






# Register Changes made to the Editor Content
def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        return

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i+=1

    previousText = editArea.get('1.0', END) 

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches


def rgb(rgb):
    return "#%02x%02x%02x" % rgb


previousText = ''

# Define colors for the variouse types of tokens

normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))

font = 'Consolas 15'


# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
    ['abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__|', function]
]

controll_panel = Frame(root, width=300, height=50, background='purple')
controll_panel.pack(side='top', fill='x')
Run_bttn = PhotoImage(file='play.png')
img_label= Label(image=Run_bttn)

#checks file_path continuosly
def check_file_path():
    if file_path == '':
        Run_bttn.config(file='disk.png')
        button.config(command=save_as)
    else:
        Run_bttn.config(file='play.png')
        button.config(command=run,)
    root.after(100, check_file_path)


button= Button(controll_panel, image=Run_bttn, command=check_file_path,
borderwidth=0)


button.pack(side='top', pady=0.5)
editArea = CodeView(root, lexer=pygments.lexers.RustLexer, font=font)

'''editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    borderwidth=30,
    font=font,
)'''

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    expand=1
)
menu_bar = Menu(root)


notes_bar = Menu(menu_bar, tearoff=0)
notes_bar.add_command(label='PLZ NOTE THAT IF U CLICK "SAVE AS" THEN WRITE -|.py|- EXTENSION URSELF AT THE END')
menu_bar.add_cascade(label='!NOTE!', menu=notes_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
menu_bar.add_cascade(label='File', menu=file_menu)
"""
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)
"""
exit_bar = Menu(menu_bar, tearoff=0)
exit_bar.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='Exit', command=exit)

root.config(menu=menu_bar)

frame = Frame(root, width=800, height=50, background="yellow")
frame.pack(fill='x')

code_output = Terminal(frame, pady=5, padx=5, font='Consolas, 15')
code_output.pack(expand=True, fill='both')



# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """print("Hello To The IDE-A")
""")

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Bind Control + R to the exec function
editArea.bind('<Control-r>', run)
editArea.bind('<Control-s>', save_as)

#changes()
root.mainloop()