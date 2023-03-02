import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import threading
import pyperclip

def reset_statusbar_callback():
    status_var.set("")

def set_timer(time):
    threading.Timer(time, reset_statusbar_callback).start()

def display_images(directory):
    image_filenames = []
    for filename in os.listdir(directory):
        if os.path.splitext(filename)[1].lower() in {".jpg", ".jpeg", ".png"}:
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            if not os.path.exists(os.path.join(directory, txt_filename)):
                image_filenames.append(filename)

    if not image_filenames:
        print("No images found in directory")
        return

    next_button = tk.Button(root, text="Next Image", command=lambda: next_image(image_filenames, directory, next_button))
    next_button.bind("<Right>", lambda event: next_button.invoke())
    next_button.pack(side=tk.LEFT)

    filename = os.path.join(directory, image_filenames[0])
    display_image(filename, next_button)

    current_filename.set(filename)

def next_image(image_filenames, directory, next_button):
    current_index = image_filenames.index(os.path.basename(current_filename.get()))

    if current_index < len(image_filenames) - 1:
        filename = os.path.join(directory, image_filenames[current_index + 1])
        display_image(filename, next_button)

def double_invoke(submit_button, next_button):
    submit_button.invoke()
    next_button.invoke()

def display_image(filename, next_button):
    global image_obj
    print(f"Displaying image {filename}")
    if os.path.exists(os.path.splitext(filename)[0] + ".txt"):
        return
    else:
        with Image.open(filename) as img:
            
            img.thumbnail((800, 600))
            image_obj = ImageTk.PhotoImage(img)
            image_label.configure(image=image_obj)

            text_box.focus()
            text.set("")
            text_box.config(state=tk.NORMAL)
            text_box.bind("<Return>", lambda event: double_invoke(submit_button, next_button))

            submit_button.config(state=tk.NORMAL)
            current_filename.set(filename)
def save_text():
    text_str = text.get()
    filename = current_filename.get()

    with open(os.path.splitext(filename)[0] + ".txt", "w") as text_file:
        text_file.write(text_str)

    print(f"Writing prompt : {text_str}")
    pyperclip.copy(text_str)
    status_var.set(f"{filename} saved successfully.")
    root.after(2000, lambda: status_bar.config(text="Everything's fine :)"))

    # Clear the status bar after 5 secondes
    set_timer(5.0)

def quit_application():
    root.quit()

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", quit_application)

window_width = 512+50
window_height = 512+50
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.S)
status_bar.pack(side=tk.TOP, fill=tk.X)

image_label = tk.Label(root)
image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

text = tk.StringVar()
text_box = tk.Entry(root, textvariable=text, state=tk.DISABLED)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

submit_button = tk.Button(root, text="Save", command=save_text, state=tk.DISABLED)
submit_button.pack(side=tk.LEFT)

select_button = tk.Button(root, text="Select Directory", command=lambda: display_images(filedialog.askdirectory()))
select_button.pack(side=tk.LEFT)

current_filename = tk.StringVar()

root.mainloop()

