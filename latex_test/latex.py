from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
from db import create_db, insert_entry, get_entries


# Function to update the listbox with database entries
def update_listbox():
    listbox.delete(0, END)
    for row in get_entries():
        listbox.insert(END, row[1])

# Function to save the input to the database and update the listbox
def save_entry():
    content = entry.get()
    insert_entry(content)
    update_listbox()

    

# Function to render the selected LaTeX from the listbox
def render_latex():
    selection = listbox.curselection()
    if not selection:
        return
    content = listbox.get(selection[0])
    content = """
      \\begin{align*}
      \\text{Let } f(x) &= x^2 \\text{, where } x \\text{ is a real number.} \\
      \\text{Then, } f'(x) &= 2x \\text{, which represents the derivative of } f(x).
      \end{align*}
   """

    fig.clear()
    fig.text(0.5, 0.5, f"${content}$", fontsize=20, ha='center', va='center', )
    #canvas.draw()
    
    canvas.draw()





win = Tk()
win.geometry("800x600")
win.title("LaTeX Database Viewer")

frame = Frame(win)
frame.pack(fill=BOTH, expand=True)

entry = Entry(frame, width=70)
entry.pack(side=TOP, fill=X, padx=5, pady=5)

save_button = Button(frame, text="Save", command=save_entry)
save_button.pack(side=TOP, fill=X, padx=5, pady=5)

listbox = Listbox(frame)
listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

scrollbar = Scrollbar(frame, command=listbox.yview)
scrollbar.pack(side=LEFT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)

render_button = Button(frame, text="Render LaTeX", command=render_latex)
render_button.pack(side=TOP, fill=X, padx=5, pady=5)

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=win)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

update_listbox()

win.mainloop()
