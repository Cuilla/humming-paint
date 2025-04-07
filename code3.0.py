import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

# --- Global Variables ---
shape_start_x, shape_start_y = None, None # Start coordinates for shapes
prev_x, prev_y = None, None               # Previous coordinates for freehand
temp_shape_id = None                      # ID of the temporary shape being drawn
current_color = "black"
current_width = 2
canvas_bg_color = "white"
current_mode = "pencil"                   # Modes: "pencil", "eraser", "square", "circle"

# --- Variables for buttons (to change their appearance) ---
tool_buttons = {} # Dictionary to hold tool buttons for easy state management

# --- Functions ---

def update_button_states():
    """Updates the relief of all tool buttons based on current_mode."""
    for mode, button in tool_buttons.items():
        if button: # Check if button exists
            if mode == current_mode:
                button.config(relief=tk.SUNKEN) # Active tool
            else:
                button.config(relief=tk.RAISED)  # Inactive tool

def activate_mode(mode):
    """Activates the specified drawing mode."""
    global current_mode
    current_mode = mode
    print(f"Mode: {current_mode}") # Debugging

    # Set appropriate cursor
    if mode == "pencil":
        canvas.config(cursor="pencil")
    elif mode == "eraser":
        canvas.config(cursor="dotbox")
    elif mode in ["square", "circle"]:
        canvas.config(cursor="crosshair")
    else:
        canvas.config(cursor="") # Default cursor

    update_button_states()


def get_drawing_color():
    """Returns the drawing color based on the current mode (eraser uses bg color)."""
    return canvas_bg_color if current_mode == "eraser" else current_color

def start_draw(event):
    """Called when the mouse button is pressed."""
    global shape_start_x, shape_start_y, prev_x, prev_y, temp_shape_id
    temp_shape_id = None # Reset temporary shape ID

    if current_mode in ["pencil", "eraser"]:
        prev_x, prev_y = event.x, event.y
        # Draw initial dot for immediate feedback
        draw_color = get_drawing_color()
        canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                           event.x + current_width/2, event.y + current_width/2,
                           fill=draw_color, outline=draw_color, width=0)
    elif current_mode in ["square", "circle"]:
        shape_start_x, shape_start_y = event.x, event.y

def draw(event):
    """Called when the mouse moves with the button held down."""
    global prev_x, prev_y, temp_shape_id

    if current_mode in ["pencil", "eraser"]:
        if prev_x is not None and prev_y is not None:
            draw_color = get_drawing_color()
            canvas.create_line(prev_x, prev_y, event.x, event.y,
                               fill=draw_color, width=current_width,
                               capstyle=tk.ROUND, smooth=tk.TRUE)
            prev_x, prev_y = event.x, event.y
    elif current_mode in ["square", "circle"] and shape_start_x is not None:
        # Delete previous temporary shape if it exists
        if temp_shape_id:
            canvas.delete(temp_shape_id)

        # Draw new temporary shape (dashed outline)
        x1, y1 = shape_start_x, shape_start_y
        x2, y2 = event.x, event.y
        if current_mode == "square":
            temp_shape_id = canvas.create_rectangle(x1, y1, x2, y2,
                                                    outline="gray", # Use a neutral color for temp
                                                    dash=(2, 2))     # Dashed line
        elif current_mode == "circle":
             temp_shape_id = canvas.create_oval(x1, y1, x2, y2,
                                                outline="gray",
                                                dash=(2, 2))

def stop_draw(event):
    """Called when the mouse button is released."""
    global prev_x, prev_y, shape_start_x, shape_start_y, temp_shape_id

    # Delete the final temporary shape
    if temp_shape_id:
        canvas.delete(temp_shape_id)
        temp_shape_id = None

    if current_mode in ["pencil", "eraser"]:
        prev_x, prev_y = None, None # Reset for freehand
    elif current_mode in ["square", "circle"] and shape_start_x is not None:
        # Draw the final shape
        x1, y1 = shape_start_x, shape_start_y
        x2, y2 = event.x, event.y
        draw_color = current_color # Shapes always use the selected color, not eraser

        # Ensure width is at least 1 for visible outlines, even if current_width is small
        effective_width = max(1, current_width)

        if current_mode == "square":
            # Add tag 'drawn_shape' for potential future use (like selection/deletion)
             canvas.create_rectangle(x1, y1, x2, y2,
                                     outline=draw_color,
                                     width=effective_width,
                                     tags='drawn_shape')
        elif current_mode == "circle":
             canvas.create_oval(x1, y1, x2, y2,
                                outline=draw_color,
                                width=effective_width,
                                tags='drawn_shape')
        # Reset shape starting point
        shape_start_x, shape_start_y = None, None

def choose_color():
    """Opens the color chooser dialog and sets the selected color."""
    global current_color
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint", initialcolor=current_color)
    if color_code[1]:
        current_color = color_code[1]
        if 'color' in tool_buttons and tool_buttons['color']: # Check if color button exists
            tool_buttons['color'].config(bg=current_color, activebackground=current_color)
            try:
                r, g, b = root.winfo_rgb(current_color)
                brightness = (r + g + b) / 3 / 65535
                fg_color = 'white' if brightness < 0.5 else 'black'
                tool_buttons['color'].config(fg=fg_color, activeforeground=fg_color)
            except:
                 tool_buttons['color'].config(fg='black', activeforeground='black')
        # Don't automatically switch mode when color is chosen
        # activate_mode("pencil") # Removed this line


def set_width(size):
    """Sets the line/outline thickness."""
    global current_width
    new_width = size
    if isinstance(size, str) and size == 'custom':
        new_width = simpledialog.askinteger("Line/Outline Thickness",
                                           "Enter thickness (pixels):",
                                           parent=root, minvalue=1, maxvalue=100,
                                           initialvalue=current_width)
        if new_width is None:
             return # User cancelled

    current_width = new_width
    print(f"Thickness set to: {current_width}")

def clear_canvas():
    """Clears the entire canvas."""
    canvas.delete("all")

# --- GUI Setup ---
root = tk.Tk()
# Updated Title
root.title("Humming Paint 3.0 (With drawing figures!)")

controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# --- Tool Buttons ---
# Store buttons in the dictionary for easy access in activate_mode
tool_buttons["pencil"] = tk.Button(controls_frame, text="Pencil", width=7, command=lambda: activate_mode("pencil"))
tool_buttons["pencil"].pack(side=tk.LEFT, padx=(5, 2), pady=2)

tool_buttons["eraser"] = tk.Button(controls_frame, text="Eraser", width=7, command=lambda: activate_mode("eraser"))
tool_buttons["eraser"].pack(side=tk.LEFT, padx=2, pady=2)

tool_buttons["square"] = tk.Button(controls_frame, text="Square", width=7, command=lambda: activate_mode("square"))
tool_buttons["square"].pack(side=tk.LEFT, padx=2, pady=2)

tool_buttons["circle"] = tk.Button(controls_frame, text="Circle", width=7, command=lambda: activate_mode("circle"))
tool_buttons["circle"].pack(side=tk.LEFT, padx=2, pady=2)


# --- Color Button (also stored for text color changes) ---
try:
    r, g, b = root.winfo_rgb(current_color)
    brightness = (r + g + b) / 3 / 65535
    initial_fg = 'white' if brightness < 0.5 else 'black'
except:
    initial_fg = 'black'

# Use a distinct key like 'color' for the color button in the dictionary
tool_buttons['color'] = tk.Button(controls_frame, text="Color", width=7, command=choose_color,
                                  bg=current_color, fg=initial_fg,
                                  activebackground=current_color, activeforeground=initial_fg)
tool_buttons['color'].pack(side=tk.LEFT, padx=2, pady=2)


# --- Buttons for Width ---
width_btn_frame = tk.Frame(controls_frame)
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="1px", width=4, command=lambda: set_width(1)).pack(side=tk.LEFT) # Start with 1px
tk.Button(width_btn_frame, text="3px", width=4, command=lambda: set_width(3)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="5px", width=4, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="10px", width=4, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Custom", width=6, command=lambda: set_width('custom')).pack(side=tk.LEFT)

# --- Clear Button ---
clear_button = tk.Button(controls_frame, text="Clear All", width=8, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2)

# --- Canvas ---
canvas = tk.Canvas(root, bg=canvas_bg_color) # Default cursor set by activate_mode
canvas.pack(fill=tk.BOTH, expand=True)

# --- Bind Mouse Events ---
canvas.bind("<Button-1>", start_draw)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_draw)

# --- Run ---
# Set initial mode and update buttons accordingly
activate_mode("pencil")
set_width(1) # Set initial width to 1px to match button
root.mainloop()
