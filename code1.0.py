import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

last_x, last_y = None, None
current_color = "black"
current_width = 2

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                       event.x + current_width/2, event.y + current_width/2,
                       fill=current_color, outline=current_color, width=0)

def draw(event):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=current_color, width=current_width,
                           capstyle=tk.ROUND, smooth=tk.TRUE)
        last_x, last_y = event.x, event.y

def stop_draw(event):
    global last_x, last_y
    last_x, last_y = None, None

def choose_color():
    global current_color
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint")
    if color_code[1]:
        current_color = color_code[1]
        color_button.config(bg=current_color, activebackground=current_color)
        try:
            r, g, b = root.winfo_rgb(current_color)
            brightness = (r + g + b) / 3 / 65535
            if brightness < 0.5:
                color_button.config(fg='white', activeforeground='white')
            else:
                color_button.config(fg='black', activeforeground='black')
        except tk.TclError:
             color_button.config(fg='black', activeforeground='black')

def set_width(size):
    global current_width
    if size:
        current_width = size
        print(f"Brush width set to: {current_width}")

def clear_canvas():
    canvas.delete("all")

root = tk.Tk()
root.title("Humming Paint v1.0")

controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

color_button = tk.Button(controls_frame, text="Color", width=10, command=choose_color, bg=current_color, fg='white', activebackground=current_color, activeforeground='white')
color_button.pack(side=tk.LEFT, padx=5, pady=2)

width_btn_frame = tk.Frame(controls_frame)
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="Thin", width=6, command=lambda: set_width(2)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Medium", width=6, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Thick", width=6, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Custom", width=6, command=lambda: set_width(simpledialog.askinteger("Brush Width", "Enter width (pixels):", parent=root, minvalue=1, maxvalue=50, initialvalue=current_width))).pack(side=tk.LEFT)

clear_button = tk.Button(controls_frame, text="Clear", width=10, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2)

canvas = tk.Canvas(root, bg="white", cursor="pencil")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

root.mainloop()
