import tkinter as tk
import subprocess
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import ctypes
import re
import os
import idlelib.colorizer as ic
import idlelib.percolator as ip
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory
import threading



# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)



# Setup Tkinter
root = Tk()
root.geometry('800x600')
root.title("IDE-A (BETA 0.00001)")
title = "IDE-A (Beta 0.00001)"
root.state('normal')
#img = PhotoImage(file='IDE.png')
root.iconbitmap("./IDE.ico")
#root.tk.call('wm', 'iconphoto', root._w, img)
file_path = ''
folder_path = ''

def set_file_path(f_path):
    global file_path
    file_path = f_path


def open_file():
    root.title(f'IDE-A (Beta 0.00001) {file_path}')
    f_path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editArea.delete('1.0', END)
        editArea.insert('1.0', code)
        set_file_path(f_path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')


def save(s=0):
    print(s, type(s))
    if file_path == '':
        f_path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        f_path = file_path
    with open(f_path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(f_path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')

def save_as(s=0):
    print(s, type(s))
    f_path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(f_path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(f_path)
        root.title(f'IDE-A (Beta 0.00001) {file_path}')



def run(s=0):
    print(s, type(s))
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        save()
        return
    else:
        #Windows one
        os.system(f'start cmd /K "python {file_path}"')
        #terminal.entry.insert("end", f"python3 {file_path}")

        #for linux
        #os.system(f"gnome-terminal -e 'bash -c \"python3 {file_path}; bash\" '")
        t = threading.Thread(target=run)
        t.start(1)




# Register Changes made to the Editor Content
'''def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        #return

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
'''
'''def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches
'''

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
variables = rgb((148, 215, 71))
font = 'Consolas 15'


# Define a list of Regex Pattern that should be colored in a certain way
'''repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
    ['print|input|', function],
    #['str|int|byte|float', variables]
]
'''


########################################
#TREE
########################################
file_tree = Frame(root)
file_tree.pack(side='left', fill=Y, expand="yes")
def open_dir():
    global abspath
    for i in tree.get_children():
        tree.delete(i)
    path = askdirectory()
    abspath = os.path.abspath(path)
    root_node = tree.insert('', 'end', text=abspath, open=True)
    process_directory(root_node,abspath)


filepaths = {}
def process_directory(parent, path):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        isdir = os.path.isdir(abspath)
        oid = tree.insert(parent, 'end', text=p, open=False)
        filepaths[oid] = abspath  # save the full pathname
        if isdir:
            process_directory(oid, abspath)

def Open_file_from_list_box(value):
    global file_path
    file_path = ''
    try:
        item_id = tree.selection()[0]
        file_path = filepaths[item_id] # get the full pathname
        root.title(f"IDE-A (BETA 0.00001) {file_path}")
        editArea.delete(1.0,END)
        with open(file_path,"r") as f:
            editArea.insert(1.0,f.read())
    except Exception as ex:
        print(ex.__class__.__name__, ex)



tree = ttk.Treeview(file_tree)
tree.pack(expand=YES, fill=BOTH)
path = '.'
tree.heading('#0', text=path, anchor='w')
abspath = os.path.abspath(path)
root_node = tree.insert('', 'end', text=abspath, open=True)
process_directory(root_node, abspath)

tree.bind("<<TreeviewSelect>>",lambda event=None:Open_file_from_list_box(path))



terminal_frame = Frame(root, height=10, background='pink')
terminal_frame.pack(side='bottom', fill='both')


controll_panel = Frame(root, width=300, height=50, background='purple')
controll_panel.pack(side='top', fill='x')
Run_bttn = PhotoImage(file='play.png')
img_label= Label(image=Run_bttn)

#checks file_path continuosly
def check_file_path():
    if file_path == '':
        Run_bttn.config(file='./disk.png')
        control_bttn.config(command=save_as)
    else:
        Run_bttn.config(file='./play.png')
        control_bttn.config(command=run,)
    root.after(100, check_file_path)


control_bttn= Button(controll_panel, image=Run_bttn, command=check_file_path,
borderwidth=0)
control_bttn.pack(side='right', pady=0.5)

open_dir_bttn = Button(controll_panel,text="Open Directory",command=open_dir)
open_dir_bttn.pack(side='left', fill='y')

gapFrame = Frame(root, width=1)
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


cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = r"(?<!class)\s+(\w+)"

cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': background}

# These five lines are optional. If omitted, default colours are used.
cdg.tagdefs['COMMENT'] = {'foreground': '#007F00 ', 'background': background}
cdg.tagdefs['KEYWORD'] = {'foreground': '#27b1dd', 'background': background}
cdg.tagdefs['BUILTIN'] = {'foreground': '#dddd22', 'background': background}
cdg.tagdefs['STRING'] = {'foreground': '#8b9b40', 'background': background}
cdg.tagdefs['DEFINITION'] = {'foreground': '#27b9b9', 'background': background}


ip.Percolator(editArea).insertfilter(cdg)


'''
CHARBLUE = '#007F00 '
CLOUD = '#4aded9 '
CLOUD2 = '#47c2be '
LEMON = '#e1ec34 '
OVERCAST = '#dddd22 '
PUMPKIN = '#ea9f13'
STORMY = '#307ab4 '
FIRE = '#ed7110 '
DK_SEAFOAM = '#27b1dd '
PURPLE = '#8623c2 '
#test
IDPROG = r"(?<!class)\s+(\w+)"

TAGDEFS   = {   'COMMENT'    : {'foreground': CHARBLUE  , 'background': background},
                'TYPES'      : {'foreground': CLOUD2    , 'background': background},
                'NUMBER'     : {'foreground': LEMON     , 'background': background},
                'BUILTIN'    : {'foreground': OVERCAST  , 'background': background},
                'STRING'     : {'foreground': PUMPKIN   , 'background': background},
                'DOCSTRING'  : {'foreground': STORMY    , 'background': background},
                'EXCEPTION'  : {'foreground': CLOUD2    , 'background': background, 'font':'bold'},
                'DEFINITION' : {'foreground': FIRE    , 'background': background, 'font':'bold'},
                'DECORATOR'  : {'foreground': CLOUD2    , 'background': background, 'font':'italic'},
                'INSTANCE'   : {'foreground': CLOUD     , 'background': background, 'font':'italic'},
                'KEYWORD'    : {'foreground': DK_SEAFOAM, 'background': background, 'font':'bold'},
                'CLASSDEF'   : {'foreground': PURPLE    , 'background': background, 'font':'bold'},
            }

cd         = ic.ColorDelegator()
cd.idprog  = re.compile(IDPROG, re.S)
cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
ip.Percolator(editArea).insertfilter(cd)'''





class Terminal:
    def __init__(self, master):
        self.master = master
        master.configure(bg='black')

        # create entry widget for user input
        self.entry = tk.Entry(terminal_frame, width=80, fg='white', bg='black', insertbackground='white', bd=0, font=('Consolas', 13))
        self.entry.pack(fill="both", side='bottom')
        self.entry.focus_set()

        # create text widget for terminal output
        self.output = tk.Text(terminal_frame, height=10, width=80, fg='white', bg='black', wrap='word', font=('Consolas', 13))
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

terminal = Terminal(main_frame)


def open_settings():
    settings_window = Tk()
    settings_window.title("IDE-A (Options)")
    settings_window.geometry('600x400')
    settings_window.state('normal')

    string_label = Label(settings_window, text='Nothing is here dude :) \nYet...', pady=100, font=('Consolas', 15))
    string_label.pack()
    #string_label = ctk.CTkLabel(settings_window, text='Choose String color: ')
    #string_label.pack()

    #option_box = ctk.CTkOptionMenu(settings_window, values=["yellow", 'green', 'blue', 'red'])
    #option_box.pack()
    #option_box.set('yellow')


    

########################################
#GAP
########################################
gap = Label(gapFrame, width=1, background=background, foreground=normal, relief=FLAT, pady=30, font=font)
gap.pack(side='left', fill='y', expand=NO)



menu_bar = Menu(root)


notes_bar = Menu(menu_bar, tearoff=0)
notes_bar.add_command(label='PLZ NOTE THAT IF U CLICK "SAVE AS" THEN WRITE -|.py|- EXTENSION URSELF AT THE END')
menu_bar.add_cascade(label='!NOTE!', menu=notes_bar)

settings = Menu(menu_bar, tearoff=0)
settings.add_command(label='Settings', command=open_settings)
menu_bar.add_cascade(label='Settings', menu=settings)


file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As', command=save_as)
menu_bar.add_cascade(label='File', menu=file_menu)
exit_bar = Menu(menu_bar, tearoff=0, )
exit_bar.add_command(label='Exit', command=exit, )
menu_bar.add_cascade(label='Exit', command=exit, )

root.config(menu=menu_bar)







# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """print("Welcome To The IDE-A")
""")

# Bind the KeyRelase to the Changes Function
#editArea.bind('<KeyRelease>', changes)
editArea.bind('<Control-r>', run)
editArea.bind('<Control-s>', save)
editArea.bind('<Control-Alt-s>', save_as)



#hanges()
root.mainloop()


