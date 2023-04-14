import tkinter as tk
import subprocess
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import ctypes
import re
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename
import threading
import customtkinter


# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)
customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")



# Setup Tkinter
root = customtkinter.CTk()
root.geometry('800x600')
root.title("IDE-A (BETA 0.00001)")
title = "IDE-A (Beta 0.00001)"
root.state('zoomed')
root.iconbitmap('IDE_Logo.ico')
file_path = ''
folder_path = ''

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


def file_tree():
    if folder_path =='':
        folder_path = filedialog.askdirectory()
    else:
        print(folder_path)



def save(s=0):
    print(s, type(s))
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')

def save_as(s=0):
    print(s, type(s))
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')



def run(s=0):
    print(s, type(s))
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
background = rgb((40, 41, 35))
tree = rgb((42, 42, 48))

font = 'Consolas 15'


# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
    ['abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__|', function]
]



########################################
#TREE
########################################
#file_tree = Frame(root, width=300, background=tree)
#file_tree.pack(side='left', fill='y')




controll_panel = Frame(root, width=300, height=50, background='purple')
controll_panel.pack(side='top', fill='x')
Run_bttn = PhotoImage(file='play.png')
img_label= Label(image=Run_bttn)

#checks file_path continuosly
def check_file_path():
    if file_path == '':
        Run_bttn.config(file='disk.png')
        control_bttn.config(command=save_as)
    else:
        Run_bttn.config(file='play.png')
        control_bttn.config(command=run,)
    root.after(100, check_file_path)


control_bttn= Button(controll_panel, image=Run_bttn, command=check_file_path,
borderwidth=0)
control_bttn.pack(side='right', pady=0.5)

gapFrame = Frame(root, width=32)
gapFrame.pack(side='left', fill='y')

main_frame = Frame(root, relief=FLAT)
main_frame.pack(fill=BOTH)


editArea = Text(
    main_frame,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=FLAT,
    #borderwidth=30,
    pady=30,
    font=font,
)

editArea.pack(fill=BOTH, expand=1, side='right')


########################################
#GAP
########################################
gap = Text(gapFrame, width=2, background=background, foreground=normal, insertbackground=normal, relief=FLAT, pady=30, font=font)
gap.pack(side='left', fill='y', expand=NO)


menu_bar = Menu(root, background=background, fg=background)


notes_bar = Menu(menu_bar, tearoff=0, background=background)
notes_bar.add_command(label='PLZ NOTE THAT IF U CLICK "SAVE AS" THEN WRITE -|.py|- EXTENSION URSELF AT THE END')
menu_bar.add_cascade(label='!NOTE!', menu=notes_bar)

file_menu = Menu(menu_bar, tearoff=0, background=background)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As', command=save_as)
menu_bar.add_cascade(label='File', menu=file_menu)
"""
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)
"""
exit_bar = Menu(menu_bar, tearoff=0, )
exit_bar.add_command(label='Exit', command=exit, )
menu_bar.add_cascade(label='Exit', command=exit, )

root.config(menu=menu_bar)

#frame = Frame(root, width=800, background="yellow")
#frame.pack(fill='both')




# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """print("Hello To The IDE-A")
""")

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Bind Control + R to the exec function
editArea.bind('<Control-r>', run)
editArea.bind('<Control-s>', save)
editArea.bind('<Control-Alt-s>', save_as)

class Terminal:
    def __init__(self, master):
        self.master = master
        master.configure(bg='black')

        # create entry widget for user input
        self.entry = tk.Entry(root, width=80, fg='white', bg='black', insertbackground='white', bd=0, font=('Consolas', 13))
        self.entry.pack(fill="both", side='bottom')
        self.entry.focus_set()

        # create text widget for terminal output
        self.output = tk.Text(root, height=16, width=80, fg='white', bg='black', wrap='word', font=('Consolas', 13))
        self.output.pack(fill="both", side='bottom')

        # bind 'Return' key to execute command
        self.entry.bind("<Return>", self.execute_command)

        # set initial command prompt
        self.output.insert(tk.END, "C:\\>")

    def execute_command(self, event):
        # get user input from entry widget
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        # print user input to terminal output
        self.output.insert(tk.END, f"{command}\n")

        # execute command and print output to terminal output
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            self.output.insert(tk.END, output.decode())
        except subprocess.CalledProcessError as e:
            self.output.insert(tk.END, f"Error: {e}\n")

        # set command prompt to current working directory
        cwd = subprocess.check_output("cd", shell=True)
        self.output.insert(tk.END, f"{cwd.decode().strip()}\\>")




terminal = Terminal(root)
changes()
root.mainloop()
