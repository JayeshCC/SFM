import os
import tkinter as tk
from tkinter import ttk, filedialog, Menu

def populate_tree(tree, node):
    if tree.set(node, "type") != 'directory':
        return

    path = tree.set(node, "fullpath")
    tree.delete(*tree.get_children(node))

    parent = tree.parent(node)
    special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

    for p in special_dirs + os.listdir(path):
        ptype = None
        p = os.path.join(path, p).replace('\\', '/')
        if os.path.isdir(p): ptype = "directory"
        elif os.path.isfile(p): ptype = "file"

        fname = os.path.split(p)[1]
        id = tree.insert(node, "end", text=fname, values=[p, ptype])

        if ptype == 'directory':
            if fname not in ('.', '..'):
                tree.insert(id, 0, text="dummy")
                tree.item(id, text=fname)
        elif ptype == 'file':
            tree.item(id, text=fname)

def populate_roots(tree):
    dir = os.path.abspath(os.sep)
    node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
    populate_tree(tree, node)

def update_tree(event):
    tree = event.widget
    populate_tree(tree, tree.focus())

def change_dir(event):
    tree = event.widget
    node = tree.focus()
    if tree.parent(node):
        path = os.path.abspath(tree.set(node, "fullpath"))
        if os.path.isdir(path):
            os.chdir(path)
            tree.delete(*tree.get_children(''))
            populate_roots(tree)

root = tk.Tk()
root.title("File Explorer")

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open...")
file_menu.add_command(label="Save As...")
file_menu.add_command(label="Exit", command=root.quit)

vsb = ttk.Scrollbar(orient="vertical")
hsb = ttk.Scrollbar(orient="horizontal")

tree = ttk.Treeview(columns=("fullpath", "type"), displaycolumns="",
                    yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
                    xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

vsb['command'] = tree.yview
hsb['command'] = tree.xview

tree.heading("#0", text="Directory Structure", anchor='w')
tree.heading("type", text="Type")
tree.column("type", stretch=0, width=100)

populate_roots(tree)
tree.bind('<<TreeviewOpen>>', update_tree)
tree.bind('<Double-Button-1>', change_dir)

# Arrange the tree and its scrollbars in a toplevel
tree.grid(column=0, row=0, sticky='nswe')
vsb.grid(column=1, row=0, sticky='ns')
hsb.grid(column=0, row=1, sticky='ew')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()