import tkinter as tk

def show_main_buttons():
    clear_frame()
    # Ensure the button frame is packed at the bottom and fills horizontally
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    # Pack buttons into the button frame
    tk.Button(button_frame, text="Add", command=show_add_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Study", command=show_study_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Browse", command=show_browse_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Stats", command=show_stats_page).pack(side=tk.LEFT, expand=True, fill=tk.X)

def show_add_page():
    clear_frame()
    tk.Label(main_frame, text="Add Page").pack()
    tk.Button(main_frame, text="Back", command=show_main_buttons).pack()

def show_study_page():
    clear_frame()
    tk.Label(main_frame, text="Study Page").pack()
    tk.Button(main_frame, text="Back", command=show_main_buttons).pack()

def show_browse_page():
    clear_frame()
    tk.Label(main_frame, text="Browse Page").pack()
    tk.Button(main_frame, text="Back", command=show_main_buttons).pack()

def show_stats_page():
    clear_frame()
    tk.Label(main_frame, text="Stats Page").pack()
    tk.Button(main_frame, text="Back", command=show_main_buttons).pack()

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()
    # Ensure the button frame is removed from the main frame when clearing
    button_frame.pack_forget()

root = tk.Tk()
root.title("Multi-Page Sample App")
root.geometry("400x300")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, side=tk.TOP)

# Create a separate frame for the buttons
button_frame = tk.Frame(root)

show_main_buttons()

root.mainloop()
