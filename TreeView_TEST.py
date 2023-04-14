from tkinter import*
from tkinter import ttk
import os
from tkinter.filedialog import askdirectory
def Open():
    for i in tree.get_children():
        tree.delete(i)
    path = askdirectory()
    abspath = os.path.abspath(path)
    root_node = tree.insert('', 'end', text=abspath, open=True)
    process_directory(root_node,abspath)
def process_directory( parent, path):

        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                process_directory(oid, abspath)
def Open_file_from_list_box(value):
    global file
    item_id = tree.selection()
    file = tree.item(item_id, 'text') # get the filename from 'text' option
    filepath = os.path.join(value,file)
    root.title(filepath + "                                                                                                                                            Code Editor")
    editor.delete(1.0,END)
    with open(filepath,"r") as f:
        editor.insert(1.0,f.read())
root = Tk()
root.geometry("1550x850+0+0")
Button(root,text="Open",command=Open).pack()
frame = Frame(root)
tree = ttk.Treeview(frame)
tree.pack(expand=True,fill=Y)
path = "."
tree.heading('#0', text=path, anchor='w')
abspath = os.path.abspath(path)
root_node = tree.insert('', 'end', text=abspath, open=True)
process_directory(root_node, abspath)
frame.pack(side=LEFT,fill=Y)
frame = Frame(root)
frame.pack(side=LEFT,expand=True,fill=BOTH)
editor = Text(frame,font="Consolas 15")
editor.pack(expand=True,fill=BOTH)

tree.bind("<<TreeviewSelect>>",lambda event=None:Open_file_from_list_box(path))

root.mainloop()