import tkinter as tk
import subprocess
import tkinter.ttk as ttk
from tkinter import *
from tkinter.messagebox import showinfo
import re
import os
import idlelib.colorizer as ic
import idlelib.percolator as ip
from tkinter.filedialog import asksaveasfilename, askopenfilename, askdirectory
import threading
import customtkinter



print("lmao")

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.deactivate_automatic_dpi_awareness()



        # configure window
app = customtkinter.CTk()
app.title("IDE-A (New UI)")
app.geometry(f"{1100}x{800}")

def open_input_dialog_event():
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

def sidebar_button_event():
        print("sidebar_button click")
file_path = ''
path = '.'

def set_file_path(f_path):
    global file_path
    file_path = f_path


def open_file():
    global file_path # add this line to access the global variable
    app.title(f'IDE-A {file_path}')
    f_path = askopenfilename(filetypes=[('Python Files', '*.py')])
    try:
        with open(f_path, 'r') as file: # use f_path instead of path
            code = file.read()
            editArea.delete('1.0', END)
            editArea.insert('1.0', code)
            set_file_path(f_path)
            app.title(f'IDE-A (Beta 0.00001) {file_path}')
    except Exception as e:
        error_popup= customtkinter.CTk()
        error_popup.title("Error")
        error_popup.geometry(f"{200}x{200}")
        popup = customtkinter.CTkLabel("Error Could not open file")
        popup.grid(sticky="nsew")



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
        app.title(f'IDE-A (Beta 0.00001) {file_path}')

def save_as(s=0):
    print(s, type(s))
    f_path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    with open(f_path, 'w') as file:
        code = editArea.get('1.0', END)
        file.write(code)
        set_file_path(f_path)
        app.title(f'IDE-A (Beta 0.00001) {file_path}')



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
        
        #for linux
        #os.system(f"gnome-terminal -e 'bash -c \"python3 {file_path}; bash\" '")
        t = threading.Thread(target=run)
        t.start(1)

        # configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0), weight=1)
app.grid_rowconfigure((1, 2, 3), weight=1)

navbar = customtkinter.CTkFrame(app, width=60, corner_radius=9)
navbar.grid(row=0, column=2, columnspan=2, sticky="ne")
navbar_run = customtkinter.CTkButton(navbar, text="Run", command=run, width=65, font=("Arial", 13))
navbar_run.grid(row=0, column=0, sticky="n", padx=20, pady=(20, 2))
navbar_run = customtkinter.CTkButton(navbar, text="Save", command=save, width=65, font=("Arial", 13))
navbar_run.grid(row=1, column=0, sticky="n", padx=20, pady=(20, 2))
navbar_run = customtkinter.CTkButton(navbar, text="Save as", command=save_as, width=65, font=("Arial", 13))
navbar_run.grid(row=2, column=0, sticky="n", padx=20, pady=(20, 2))
navbar_run = customtkinter.CTkButton(navbar, text="Open File", command=open_file, width=65, font=("Arial", 13))
navbar_run.grid(row=3, column=0, sticky="n", padx=20, pady=(20, 20))


# create sidebar frame with widgets
sidebar_frame = customtkinter.CTkFrame(app, width=300, corner_radius=0)
sidebar_frame.grid(row=0, rowspan=3, column=0, sticky="nsew")
sidebar_frame.grid_rowconfigure((1, 2, 3, 4), weight=1)

file_tree = Frame(sidebar_frame)
file_tree.grid(row=1, sticky="nsew")
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
        app.title(f"IDE-A (BETA 0.00001) {file_path}")
        editArea.delete(1.0,END)
        with open(file_path,"r") as f:
            editArea.insert(1.0,f.read())
    except Exception as ex:
        print(ex.__class__.__name__, ex)



tree = ttk.Treeview(file_tree)
tree.grid(row=1, sticky="nsew", rowspan=3)
path = '.'
tree.heading('#0', text=path, anchor='w')
abspath = os.path.abspath(path)
root_node = tree.insert('', 'end', text=abspath, open=True)
process_directory(root_node, abspath)

tree.bind("<<TreeviewSelect>>",lambda event=None:Open_file_from_list_box(path))




appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
scaling_label = customtkinter.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=change_scaling_event)
scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))



tabview = customtkinter.CTkTabview(app, width=700, height=400)
tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
tabview.add("MainFile").grid_columnconfigure(0, weight=1)
tabview.tab("MainFile").grid_columnconfigure(0, weight=1)
tabview.tab("MainFile").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
editArea = customtkinter.CTkTextbox(master=tabview.tab("MainFile"), width=700, height=400, font=("./images/Hack-Regular.ttf", 15))
editArea.grid(row=0, column=0, padx=(10, 10), pady=(10, 20), sticky='nsew')


'''cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = r"(?<!class)\s+(\w+)"

background = '#282923'

cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#282923'}

# These five lines are optional. If omitted, default colours are used.
cdg.tagdefs['COMMENT'] = {'foreground': '#007F00 ', 'background': '#282923'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#27b1dd', 'background': '#282923'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#dddd22', 'background': '#282923'}
cdg.tagdefs['STRING'] = {'foreground': '#8b9b40', 'background': '#282923'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#27b9b9', 'background': '#282923'}


ip.Percolator(editArea).insertfilter(cdg)'''


terminal_frame = customtkinter.CTkFrame(app, width=200)
terminal_frame.grid(row=1, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
terminal_frame.grid_columnconfigure(0, weight=1)
terminal_frame.grid_rowconfigure((0, 1), weight=1)

class Terminal:
    def __init__(self, master):
        self.master = master


        # create text widget for terminal output
        self.output = customtkinter.CTkTextbox(terminal_frame, wrap='word', font=('Consolas', 13))
        self.output.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky='nsew')
        
        # create entry widget for user input
        self.entry = customtkinter.CTkEntry(terminal_frame, placeholder_text="Command")
        self.entry.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky='nsew')
        self.entry.focus_set()

        # bind 'Return' key to execute command
        self.entry.bind("<Return>", self.execute_command)

        # set initial command prompt
        self.output.configure(state="normal")
        self.output.insert(tk.END, "$ ")
        self.output.configure(state="disabled")

    def execute_command(self, event):
        # get user input from entry widget
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        # print user input to terminal output
        self.output.insert(tk.END, f"{command}\n")

        # execute command and print output to terminal output
        self.output.configure(state="normal")
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            self.output.insert(tk.END, output.decode())
        except subprocess.CalledProcessError as e:
            self.output.insert(tk.END, f"Error: {e}\n")

        # set command prompt to current working directory
        cwd = subprocess.check_output("cd", shell=True)
        self.output.insert(tk.END, f"{cwd.decode().strip()}\\>")
        self.output.configure(state="disabled")

        th = threading.Thread(target=run)
        th.start(1)
terminal = Terminal(terminal_frame)



        

        # set default values
appearance_mode_optionemenu.set("Dark")
scaling_optionemenu.set("100%")
        
editArea.insert("0.0", "print('Welcome To The IDE-A')")
editArea.bind('<Control-r>', run)
editArea.bind('<Control-s>', save)
editArea.bind('<Control-Alt-s>', save_as)


app.mainloop()
