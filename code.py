import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import font

# --- Global Variables ---
shape_start_x, shape_start_y = None, None
prev_x, prev_y = None, None
temp_shape_id = None
current_color = "black"
current_width = 1
current_font_size = 12 # NEW: Variable for font size, default 12pt
canvas_bg_color = "white"
current_mode = "pencil" # Modes: "pencil", "eraser", "square", "circle", "text"

# --- Variables for buttons ---
tool_buttons = {}

# --- Functions ---

def update_button_states():
    """Updates the relief of all tool buttons based on current_mode."""
    for mode, button in tool_buttons.items():
        if button:
            relief = tk.SUNKEN if mode == current_mode else tk.RAISED
            if mode != 'color':
                 button.config(relief=relief)

def activate_mode(mode):
    """Activates the specified drawing mode."""
    global current_mode
    if current_mode == mode: return
    current_mode = mode
    print(f"Mode: {current_mode}")

    cursors = {
        "pencil": "pencil", "eraser": "dotbox", "square": "crosshair",
        "circle": "crosshair", "text": "xterm"
    }
    canvas.config(cursor=cursors.get(mode, "")) # Set cursor or default
    update_button_states()


def get_drawing_color():
    """Returns the drawing color (eraser uses bg color)."""
    return canvas_bg_color if current_mode == "eraser" else current_color

def start_draw(event):
    """Called when the mouse button is pressed."""
    global shape_start_x, shape_start_y, prev_x, prev_y, temp_shape_id
    temp_shape_id = None

    if current_mode in ["pencil", "eraser"]:
        prev_x, prev_y = event.x, event.y
        draw_color = get_drawing_color()
        # Use create_line for single pixel dot if width is 1, otherwise oval
        if current_width <= 1 and current_mode == "pencil":
             canvas.create_line(event.x, event.y, event.x+1, event.y, fill=draw_color, width=1)
        elif current_width <= 1 and current_mode == "eraser":
             canvas.create_line(event.x, event.y, event.x+1, event.y, fill=draw_color, width=1)
        else:
            radius = current_width / 2
            canvas.create_oval(event.x - radius, event.y - radius,
                               event.x + radius, event.y + radius,
                               fill=draw_color, outline=draw_color, width=0)
    elif current_mode in ["square", "circle"]:
        shape_start_x, shape_start_y = event.x, event.y
    elif current_mode == "text":
        # --- Text Drawing Logic ---
        user_text = simpledialog.askstring("Enter Text", "Text to draw:", parent=root)
        if user_text:
            # Use current_font_size here!
            canvas.create_text(event.x, event.y, text=user_text,
                               fill=current_color, anchor=tk.NW,
                               font=("Arial", current_font_size), # Use the variable
                               tags='drawn_text')


def draw(event):
    """Called when the mouse moves with the button held down."""
    global prev_x, prev_y, temp_shape_id

    if current_mode in ["pencil", "eraser"]:
        if prev_x is not None and prev_y is not None:
            draw_color = get_drawing_color()
            canvas.create_line(prev_x, prev_y, event.x, event.y,
                               fill=draw_color, width=current_width,
                               capstyle=tk.ROUND, smooth=tk.TRUE,
                               tags=('line' if current_mode == 'pencil' else 'erased_line'))
            prev_x, prev_y = event.x, event.y
    elif current_mode in ["square", "circle"] and shape_start_x is not None:
        if temp_shape_id:
            canvas.delete(temp_shape_id)
        x1, y1 = shape_start_x, shape_start_y
        x2, y2 = event.x, event.y
        creator = canvas.create_rectangle if current_mode == "square" else canvas.create_oval
        temp_shape_id = creator(x1, y1, x2, y2, outline="gray", dash=(2, 2))


def stop_draw(event):
    """Called when the mouse button is released."""
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
        creator = canvas.create_rectangle if current_mode == "square" else canvas.create_oval
        # Ensure start/end coordinates are valid if user just clicks
        if x1 == x2 and y1 == y2:
             x2 += effective_width # Make a small shape for a click
             y2 += effective_width
        creator(x1, y1, x2, y2, outline=draw_color, width=effective_width, tags='drawn_shape')
        shape_start_x, shape_start_y = None, None


def choose_color():
    """Opens the color chooser dialog and sets the selected color."""
    global current_color
    color_code = colorchooser.askcolor(title="Choose Color", initialcolor=current_color)
    if color_code and color_code[1]:
        current_color = color_code[1]
        if 'color' in tool_buttons and tool_buttons['color']:
            btn = tool_buttons['color']
            btn.config(bg=current_color, activebackground=current_color)
            try: # Set foreground for readability
                r, g, b = root.winfo_rgb(current_color)
                brightness = (r + g + b) / 3 / 65535
                fg_color = 'white' if brightness < 0.5 else 'black'
                btn.config(fg=fg_color, activeforeground=fg_color)
            except:
                 btn.config(fg='black', activeforeground='black')


def set_width(size):
    """Sets the line/outline thickness."""
    global current_width
    new_width = size
    if isinstance(size, str) and size == 'custom':
        new_width = simpledialog.askinteger("Line/Outline Thickness",
                                           "Enter thickness (pixels):",
                                           parent=root, minvalue=1, maxvalue=100,
                                           initialvalue=current_width)
        if new_width is None: return
    current_width = new_width
    print(f"Thickness set to: {current_width}px")

# --- NEW Function to set Font Size ---
def set_font_size():
    """Opens a dialog to set the font size for the text tool."""
    global current_font_size
    new_size = simpledialog.askinteger("Font Size",
                                       "Enter font size (points):",
                                       parent=root, minvalue=6, maxvalue=120, # Example range
                                       initialvalue=current_font_size)
    if new_size is not None: # Check if user provided a value
        current_font_size = new_size
        print(f"Font size set to: {current_font_size}pt")


def clear_canvas():
    """Clears the entire canvas."""
    canvas.delete("all")

# --- GUI Setup ---
root = tk.Tk()
root.title("Humming Paint 4.0 (With text drawing!)") # Title remains the same for now

controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# --- Tool Buttons ---
btn_width = 6
tool_buttons["pencil"] = tk.Button(controls_frame, text="Pencil", width=btn_width, command=lambda: activate_mode("pencil"))
tool_buttons["pencil"].pack(side=tk.LEFT, padx=(5, 2), pady=2)

tool_buttons["eraser"] = tk.Button(controls_frame, text="Eraser", width=btn_width, command=lambda: activate_mode("eraser"))
tool_buttons["eraser"].pack(side=tk.LEFT, padx=2, pady=2)

tool_buttons["square"] = tk.Button(controls_frame, text="Square", width=btn_width, command=lambda: activate_mode("square"))
tool_buttons["square"].pack(side=tk.LEFT, padx=2, pady=2)

tool_buttons["circle"] = tk.Button(controls_frame, text="Circle", width=btn_width, command=lambda: activate_mode("circle"))
tool_buttons["circle"].pack(side=tk.LEFT, padx=2, pady=2)

tool_buttons["text"] = tk.Button(controls_frame, text="Text", width=btn_width, command=lambda: activate_mode("text"))
tool_buttons["text"].pack(side=tk.LEFT, padx=2, pady=2)


# --- Color Button ---
try: r, g, b = root.winfo_rgb(current_color); initial_fg = 'white' if (r + g + b) / 3 / 65535 < 0.5 else 'black'
except: initial_fg = 'black'
tool_buttons['color'] = tk.Button(controls_frame, text="Color", width=btn_width, command=choose_color,
                                  bg=current_color, fg=initial_fg,
                                  activebackground=current_color, activeforeground=initial_fg)
tool_buttons['color'].pack(side=tk.LEFT, padx=(4, 2), pady=2)


# --- Buttons for Width ---
width_label = tk.Label(controls_frame, text=" Width:")
width_label.pack(side=tk.LEFT, padx=(5,0), pady=2)
width_btn_frame = tk.Frame(controls_frame)
width_btn_frame.pack(side=tk.LEFT, padx=(0,5))
tk.Button(width_btn_frame, text="1", width=2, command=lambda: set_width(1)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="3", width=2, command=lambda: set_width(3)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="5", width=2, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="10", width=2, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="...", width=2, command=lambda: set_width('custom')).pack(side=tk.LEFT) # Custom button smaller

# --- NEW Font Size Button ---
font_size_button = tk.Button(controls_frame, text="Font Size", width=7, command=set_font_size)
font_size_button.pack(side=tk.LEFT, padx=2, pady=2)

# --- Clear Button ---
clear_button = tk.Button(controls_frame, text="Clear All", width=8, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2)

# --- Canvas ---
canvas = tk.Canvas(root, bg=canvas_bg_color)
canvas.pack(fill=tk.BOTH, expand=True)

# --- Bind Mouse Events ---
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# --- Run ---
set_width(1)
# Font size is already defaulted to 12
activate_mode("pencil")
root.mainloop()
