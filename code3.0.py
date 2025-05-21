import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

shape_start_x, shape_start_y = None, None
prev_x, prev_y = None, None
temp_shape_id = None
current_color = "black"
current_width = 2
canvas_bg_color = "white"
current_mode = "pencil"

tool_buttons = {}

def update_button_states():
    for mode, button in tool_buttons.items():
        if button:
            if mode == current_mode:
                button.config(relief=tk.SUNKEN)
            else:
                button.config(relief=tk.RAISED)

def activate_mode(mode):
    global current_mode
    current_mode = mode
    print(f"Mode: {current_mode}")
    if mode == "pencil":
        canvas.config(cursor="pencil")
    elif mode == "eraser":
        canvas.config(cursor="dotbox")
    elif mode in ["square", "circle"]:
        canvas.config(cursor="crosshair")
    else:
        canvas.config(cursor="")
    update_button_states()

def get_drawing_color():
    return canvas_bg_color if current_mode == "eraser" else current_color

def start_draw(event):
    global shape_start_x, shape_start_y, prev_x, prev_y, temp_shape_id
    temp_shape_id = None
    if current_mode in ["pencil", "eraser"]:
        prev_x, prev_y = event.x, event.y
        draw_color = get_drawing_color()
        canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                           event.x + current_width/2, event.y + current_width/2,
                           fill=draw_color, outline=draw_color, width=0)
    elif current_mode in ["square", "circle"]:
        shape_start_x, shape_start_y = event.x, event.y

def draw(event):
    global prev_x, prev_y, temp_shape_id
    if current_mode in ["pencil", "eraser"]:
        if prev_x is not None and prev_y is not None:
            draw_color = get_drawing_color()
            canvas.create_line(prev_x, prev_y, event.x, event.y,
                               fill=draw_color, width=current_width,
                               capstyle=tk.ROUND, smooth=tk.TRUE)
            prev_x, prev_y = event.x, event.y
    elif current_mode in ["square", "circle"] and shape_start_x is not None:
        if temp_shape_id:
            canvas.delete(temp_shape_id)
        x1, y1 = shape_start_x, shape_start_y
        x2, y2 = event.x, event.y
        if current_mode == "square":
            temp_shape_id = canvas.create_rectangle(x1, y1, x2, y2,
                                                    outline="gray",
                                                    dash=(2, 2))
        elif current_mode == "circle":
            temp_shape_id = canvas.create_oval(x1, y1, x2, y2,
                                               outline="gray",
                                               dash=(2, 2))

def stop_draw(event):
    global prev_x, prev_y, shape_start_x, shape_start_y, temp_shape_id
    if temp_shape_id:
        canvas.delete(temp_shape_id)
        temp_shape_id = None
    if current_mode in ["pencil", "eraser"]:
        prev_x, prev_y = None, None
    elif current_mode in ["square", "circle"] and shape_start_x is not None:
        x1, y1 = shape_start_x, shape_start_y
        x2, y2 = event.x, event.y
        draw_color = current_color
        effective_width = max(1, current_width)
        if current_mode == "square":
            canvas.create_rectangle(x1, y1, x2, y2,
                                   outline=draw_color,
                                   width=effective_width,
                                   tags='drawn_shape')
        elif current_mode == "circle":
            canvas.create_oval(x1, y1, x2, y2,
                              outline=draw_color,
                              width=effective_width,
                              tags='drawn_shape')
        shape_start_x, shape_start_y = None, None

def choose_color():
    global current_color
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint", initialcolor=current_color)
    if color_code[1]:
        current_color = color_code[1]
        if 'color' in tool_buttons and tool_buttons['color']:
            tool_buttons['color'].config(bg=current_color, activebackground=current_color)
            try:
                r, g, b = root.winfo_rgb(current_color)
                brightness = (r + g + b) / 3 / 65535
                fg_color = 'white' if brightness < 0.5 else 'black'
                tool_buttons['color'].config(fg=fg_color, activeforeground=fg_color)
            except:
                tool_buttons['color'].config(fg='black', activeforeground='black')

def set_width(size):
    global current_width
    new_width = size
    if isinstance(size, str) and size == 'custom':
        new_width = simpledialog.askinteger("Line/Outline Thickness",
                                           "Enter thickness (pixels):",
                                           parent=root, minvalue=1, maxvalue=100,
                                           initialvalue=current_width)
        if new_width is None:
            return
    current_width = new_width
    print(f"Thickness set to:
