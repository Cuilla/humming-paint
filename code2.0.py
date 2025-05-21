import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

last_x, last_y = None, None
current_color = "black"
current_width = 2
is_erasing = False
canvas_bg_color = "white"

pencil_button = None
eraser_button = None
color_button = None

def activate_pencil():
    global is_erasing
    is_erasing = False
    if pencil_button:
        pencil_button.config(relief=tk.SUNKEN)
    if eraser_button:
        eraser_button.config(relief=tk.RAISED)
    canvas.config(cursor="pencil")
    print("Mode: Pencil")

def activate_eraser():
    global is_erasing
    is_erasing = True
    if pencil_button:
        pencil_button.config(relief=tk.RAISED)
    if eraser_button:
        eraser_button.config(relief=tk.SUNKEN)
    canvas.config(cursor="dotbox")
    print("Mode: Eraser")

def get_drawing_color():
    return canvas_bg_color if is_erasing else current_color

def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
    draw_color = get_drawing_color()
    canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                       event.x + current_width/2, event.y + current_width/2,
                       fill=draw_color, outline=draw_color, width=0)

def draw(event):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        draw_color = get_drawing_color()
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=draw_color, width=current_width,
                           capstyle=tk.ROUND, smooth=tk.TRUE)
        last_x, last_y = event.x, event.y

def stop_draw(event):
    global last_x, last_y
    last_x, last_y = None, None

def choose_color():
    global current_color
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint", initialcolor=current_color)
    if color_code[1]:
        current_color = color_code[1]
        if color_button:
            color_button.config(bg=current_color, activebackground=current_color)
            try:
                r, g, b = root.winfo_rgb(current_color)
                brightness = (r + g + b) / 3 / 65535
                fg_color = 'white' if brightness < 0.5 else 'black'
                color_button.config(fg=fg_color, activeforeground=fg_color)
            except:
                color_button.config(fg='black', activeforeground='black')
        activate_pencil()

def set_width(size):
    global current_width
    new_width = size
    if isinstance(size, str) and size == 'custom':
        new_width = simpledialog.askinteger("Brush/Eraser Thickness",
                                           "Enter thickness (pixels):",
                                           parent=root, minvalue=1, maxvalue=100,
                                           initialvalue=current_width)
        if new_width is None:
             return
    current_width = new_width
    print(f"Brush/Eraser thickness set to: {current_width}")

def clear_canvas():
    canvas.delete("all")

root = tk.Tk()
root.title("Humming Paint v2.0 (with Eraser!)")

controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

pencil_button = tk.Button(controls_frame, text="Pencil", width=8, command=activate_pencil, relief=tk.SUNKEN)
pencil_button.pack(side=tk.LEFT, padx=(5, 2), pady=2)

eraser_button = tk.Button(controls_frame, text="Eraser", width=8, command=activate_eraser, relief=tk.RAISED)
eraser_button.pack(side=tk.LEFT, padx=2, pady=2)

try:
    r, g, b = root.winfo_rgb(current_color)
    brightness = (r + g + b) / 3 / 65535
    initial_fg = 'white' if brightness < 0.5 else 'black'
except:
    initial_fg = 'black'

color_button = tk.Button(controls_frame, text="Color", width=8, command=choose_color,
                         bg=current_color, fg=initial_fg,
                         activebackground=current_color, activeforeground=initial_fg)
color_button.pack(side=tk.LEFT, padx=2, pady=2)

width_btn_frame = tk.Frame(controls_frame)
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="2px", width=4, command=lambda: set_width(2)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="5px", width=4, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="10px", width=4, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="20px", width=4, command=lambda: set_width(20)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Custom", width=6, command=lambda: set_width('custom')).pack(side=tk.LEFT)

clear_button = tk.Button(controls_frame, text="Clear", width=10, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2)

canvas = tk.Canvas(root, bg=canvas_bg_color, cursor="pencil")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

activate_pencil()
root.mainloop()
