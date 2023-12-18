from pypdf import PdfReader, PdfMerger, PdfWriter
from tkinterdnd2 import *
from tkinter import Listbox, Frame, Button, Scrollbar, Checkbutton, VERTICAL, SINGLE, X, Y, LEFT, RIGHT, filedialog
from tkinter import *
import tkinter as tk
import os


# define action when file is dropped
def add_listbox(event):
    if event.data.endswith(".pdf"):
        listbox.insert("end", event.data)


# define button actions
def pdf_concat():
    if listbox.size() <= 0:
        return
    
    filename = filedialog.asksaveasfilename(
        title = 'write down output file name',
        filetypes = [("pdf", ".pdf")],
        initialdir = "./",
        defaultextension = "pdf"
    )
    if filename == '':
        return 

    # merge all pdf files in listbox
    merger = PdfMerger(strict=False)
    if has_title_page_status.get():
        # add title page first
        merger.append(listbox.get(0))
        if read_direction_status.get():
            for i in range(2, listbox.size(), 2):
                merger.append(listbox.get(i))
                merger.append(listbox.get(i-1))
        else:
            # merge all pdf files in listbox
            for i in range(1, listbox.size()):
                merger.append(listbox.get(i))
    else:
        if read_direction_status.get():
            for i in range(1, listbox.size(), 2):
                merger.append(listbox.get(i))
                merger.append(listbox.get(i-1))
        else:
            # merge all pdf files in listbox
            for i in range(listbox.size()):
                merger.append(listbox.get(i))
    merger.write(filename)
    merger.close()
def pdf_split():
    if listbox.size() <= 0:
        return

    cut_dir = filedialog.askdirectory(
        title="select where to preserve", 
        initialdir='./'
    )
    if cut_dir == '':
        return

    for i in range(listbox.size()):
        reader = PdfReader(listbox.get(i))
        cut_file = cut_dir + "/" + os.path.splitext(os.path.basename(listbox.get(i)))[0]
        for j in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[j])
            writer.write(cut_file + '_' + str(j) + '.pdf')
            writer.close()
            
def pdf_eliminate():
    indices = listbox.curselection()
    if len(indices) == 1:
        listbox.delete(indices)

def pdf_all_clear():
    listbox.delete(0, listbox.size())

def scroll_up():
    indices = listbox.curselection()
    if len(indices) > 1:
        return 
    if indices[0] > 0:
        listbox.insert(indices[0]-1, listbox.get(indices))
        listbox.delete(indices[0]+1)
        listbox.select_set(indices[0]-1)

def scroll_down():
    indices = listbox.curselection()
    if len(indices) > 1:
        return
    if indices[0] < listbox.size()-1:
        listbox.insert(indices[0]+2, listbox.get(indices))
        listbox.delete(indices)
        listbox.select_set(indices[0]+1)

if __name__=="__main__":
    # create main window
    root = TkinterDnD.Tk()
    root.title("pdf editor")
    root.geometry("500x500")
    root.config(bg="#eeeeee")


    # create Frame widget
    frame = Frame(root)


    # create Listbox widget
    listbox = Listbox(frame, width=50, height=15, selectmode=SINGLE)
    listbox.drop_target_register(DND_FILES)
    listbox.dnd_bind("<<Drop>>", add_listbox)


    # create scrollbar
    scroll = Scrollbar(frame, orient=VERTICAL)
    listbox.configure(yscrollcommand=scroll.set)
    scroll.config(command=listbox.yview)


    # set up widgets
    frame.place(x=20, y=20)
    listbox.pack(fill=X, side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)


    # define button actions
    concat_btn = tk.Button(root, text='concat', command=pdf_concat)
    split_btn = tk.Button(root, text='split', command=pdf_split)
    eliminate_btn = tk.Button(root, text='eliminate', command=pdf_eliminate)
    all_clear_btn = tk.Button(root, text='clear all', command=pdf_all_clear)
    scroll_up_btn = tk.Button(root, text='↑', command=scroll_up)
    scroll_down_btn = tk.Button(root, text='↓', command=scroll_down)


    # define checkboxes
    has_title_page_status = tk.BooleanVar()
    has_title_page_status.set(False)
    has_title_page_cbx = tk.Checkbutton(root, variable=has_title_page_status, text='has title page')
    # True; read from right page to left page
    read_direction_status = tk.BooleanVar()
    read_direction_status.set(False)
    read_direction_cbx = tk.Checkbutton(root, variable=read_direction_status, text='from right to left')


    # set up buttons
    concat_btn.place(x=40, y=300, width=60)
    split_btn.place(x=120, y=300, width=60)
    eliminate_btn.place(x=200, y=300, width=60)
    all_clear_btn.place(x=280, y=300, width=60)
    scroll_up_btn.place(x=350, y=100, width=40)
    scroll_down_btn.place(x=350, y=150, width=40)

    has_title_page_cbx.place(x=40, y=350)
    read_direction_cbx.place(x=40, y=380)


    # start window
    root.mainloop()
