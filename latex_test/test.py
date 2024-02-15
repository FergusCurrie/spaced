import tkinter as tk

def show_main_buttons():
    clear_frame()
    # Pack the button frame at the bottom for the main buttons
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Button(button_frame, text="Add", command=show_add_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Study", command=show_study_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Browse", command=show_browse_page).pack(side=tk.LEFT, expand=True, fill=tk.X)
    tk.Button(button_frame, text="Stats", command=show_stats_page).pack(side=tk.LEFT, expand=True, fill=tk.X)

def show_add_page():
    clear_frame()
    
    # Assuming the main window's size is set to 400x300 as before
    window_width = root.winfo_width()
    entry_width = int(window_width * 0.8)  # 80% of the window width
    
    # For Entry widgets, width is in characters, not pixels, so this is approximate
    char_width = int(entry_width / 7)  # Approximation based on average character width
    
    label1 = tk.Label(main_frame, text="Field 1:")
    label1.pack()
    entry1 = tk.Text(main_frame, width=char_width, height=4)
    entry1.pack()

    label2 = tk.Label(main_frame, text="Field 2:")
    label2.pack()
    # Use Text widget for multi-line where you can more directly control height
    entry2 = tk.Text(main_frame, width=char_width, height=4)  # Height in lines, approximating 20% of window height
    entry2.pack()

    def print_entry_contents():
        # Retrieve text from entry1 and entry2 and print it
        content1 = entry1.get("1.0", tk.END).strip()
        content2 = entry2.get("1.0", tk.END).strip()
        print("Field 1:", content1)
        print("Field 2:", content2)

    # Add Card button
    add_card_button = tk.Button(main_frame, text="Add Card", command=print_entry_contents)
    add_card_button.pack()
    
    # Adjusting back button
    back_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Button(back_button_frame, text="Back", command=show_main_buttons).pack(side=tk.BOTTOM)

def show_study_page():
    show_page("Study Page")

def show_browse_page():
    show_page("Browse Page")

def show_stats_page():
    show_page("Stats Page")

def show_page(page_title):
    clear_frame()
    tk.Label(main_frame, text=page_title).pack(expand=True)
    # Pack a back button frame at the bottom for the back button
    back_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Button(back_button_frame, text="Back", command=show_main_buttons).pack(side=tk.BOTTOM)

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()
    for widget in button_frame.winfo_children():
        widget.destroy()
    for widget in back_button_frame.winfo_children():
        widget.destroy()
    # Ensure the frames are removed from the main frame when clearing
    button_frame.pack_forget()
    back_button_frame.pack_forget()

root = tk.Tk()
root.title("Multi-Page Sample App")
root.geometry("400x300")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, side=tk.TOP)

# Create separate frames for the main buttons and the back button
button_frame = tk.Frame(root)
back_button_frame = tk.Frame(root)

show_main_buttons()

root.mainloop()