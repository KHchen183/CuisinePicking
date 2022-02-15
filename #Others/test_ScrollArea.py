#兩種做法
#------------------------------------------------------------------------
from tkinter import *
def on_mousewheel(event):    # 函式：使用滾輪
  Canv.yview_scroll(int(-1*(event.delta//120)), "units")
def update_Scrollregion():
	Canv.update_idletasks()
	Canv.config(scrollregion = frm_assist.bbox("all"))
def origin_button():
  global i
  for i in range(4):
    Button(frm_assist, text = f"Button {i}").grid(row = i, column = 1)
    i+=1
  update_Scrollregion()

def add_button():
  global i
  Button(frm_assist, text = f"Button {i}").grid(row = i, column = 1)
  i+=1
  update_Scrollregion()

root = Tk()
root.geometry("400x200")

main_frame = Frame(root)
main_frame.pack(fill = "both", expand = 1)

Canv = Canvas(main_frame)
Canv.pack(side = "left", fill = "both", expand = 1)                                              

my_scrollbar = Scrollbar(main_frame, orient = "vertical", command = Canv.yview)                 
my_scrollbar.pack(side = "right", fill = "y")

Canv.configure(yscrollcommand = my_scrollbar.set)
Canv.bind("<Configure>", lambda e: Canv.configure(scrollregion = Canv.bbox("all")))    

frm_assist = Frame(Canv)                                                                      
Canv.create_window((0, 0), window = frm_assist, anchor = "nw") 
                               

i = 0
origin_button()
Button(frm_assist, text = "Add", command = add_button).grid(row = 0, column = 0)
Canv.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()


#------------------------------------------------------------------------

from tkinter import *
def on_mousewheel(event):    # 函式：使用滾輪
  Canv.yview_scroll(int(-1*(event.delta//120)), "units")
def update_Scrollregion():
	Canv.update_idletasks()
	Canv.config(scrollregion = frm_assist.bbox("all"))
def origin_button():
  global i
  for i in range(4):
    Button(frm_assist, text = f"Button {i}").grid(row = i, column = 1)
    i+=1
  update_Scrollregion()

def add_button():
  global i
  Button(frm_assist, text = f"Button {i}").grid(row = i, column = 1)
  i+=1
  update_Scrollregion()

root = Tk()
root.geometry("400x200")

main_frame = Frame(root)
main_frame.pack(fill = "both", expand = 1)

Canv = Canvas(main_frame)
Canv.pack(side = "left", fill = "both", expand = 1)                                              

my_scrollbar = Scrollbar(main_frame, orient = "vertical", command = Canv.yview)                 
my_scrollbar.pack(side = "right", fill = "y")

Canv.configure(yscrollcommand = my_scrollbar.set)
Canv.bind("<Configure>", lambda e: Canv.configure(scrollregion = Canv.bbox("all")))    

frm_assist = Frame(Canv)                                                                      
Canv.create_window((0, 0), window = frm_assist, anchor = "nw") 
                               

i = 0
origin_button()
Button(frm_assist, text = "Add", command = add_button).grid(row = 0, column = 0)
Canv.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()