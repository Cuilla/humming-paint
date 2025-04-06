import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

# --- Global Variables ---
last_x, last_y = None, None
current_color = "black"
current_width = 2
is_erasing = False  # New flag: True if eraser is active, False if pencil
canvas_bg_color = "white" # Canvas background color, used for eraser

# --- Variables for buttons (to change their appearance) ---
pencil_button = None
eraser_button = None
color_button = None

# --- Functions ---

def activate_pencil():
    """Activates the drawing (pencil) mode."""
    global is_erasing
    is_erasing = False
    # Update button appearance
    if pencil_button:
        pencil_button.config(relief=tk.SUNKEN) # "Sunken" button - active
    if eraser_button:
        eraser_button.config(relief=tk.RAISED) # "Raised" button - inactive
    # Restore pencil cursor if it was changed for the eraser
    canvas.config(cursor="pencil")
    print("Mode: Pencil") # Debugging

def activate_eraser():
    """Activates the eraser mode."""
    global is_erasing
    is_erasing = True
    # Update button appearance
    if pencil_button:
        pencil_button.config(relief=tk.RAISED)
    if eraser_button:
        eraser_button.config(relief=tk.SUNKEN)
    # Change cursor, e.g., to a dot or standard arrow
    canvas.config(cursor="dotbox") # Or "arrow", "circle", etc.
    print("Mode: Eraser") # Debugging


def get_drawing_color():
    """Returns the drawing color based on the current mode."""
    return canvas_bg_color if is_erasing else current_color

def start_draw(event):
    """Called when the mouse button is pressed."""
    global last_x, last_y
    last_x, last_y = event.x, event.y
    # Use the function to get the correct color
    draw_color = get_drawing_color()
    # Draw the starting point/oval
    canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                       event.x + current_width/2, event.y + current_width/2,
                       fill=draw_color, outline=draw_color, width=0)

def draw(event):
    """Called when the mouse moves with the button held down."""
    global last_x, last_y
    if last_x is not None and last_y is not None:
        # Use the function to get the correct color
        draw_color = get_drawing_color()
        # Draw the line
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=draw_color, width=current_width,
                           capstyle=tk.ROUND, smooth=tk.TRUE)
        last_x, last_y = event.x, event.y

def stop_draw(event):
    """Called when the mouse button is released."""
    global last_x, last_y
    last_x, last_y = None, None

def choose_color():
    """Opens the color chooser dialog and sets the selected color."""
    global current_color
    # askcolor returns ((R, G, B), '#rrggbb') or (None, None) if canceled
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint", initialcolor=current_color)
    if color_code[1]: # If a color was chosen (not None)
        current_color = color_code[1]
        if color_button: # Check if the button exists
            color_button.config(bg=current_color, activebackground=current_color)
            # Make button text visible on dark backgrounds
            try:
                # Simple check for color brightness
                r, g, b = root.winfo_rgb(current_color) # Returns values 0-65535
                brightness = (r + g + b) / 3 / 65535
                fg_color = 'white' if brightness < 0.5 else 'black'
                color_button.config(fg=fg_color, activeforeground=fg_color)
            except: # In case color determination fails (rare)
                 color_button.config(fg='black', activeforeground='black')
        # Automatically switch to pencil mode when a color is chosen
        activate_pencil()


def set_width(size):
    """Sets the line thickness (for pencil and eraser)."""
    global current_width
    new_width = size # Intermediate variable in case of input cancellation
    if isinstance(size, str) and size == 'custom': # Check if custom thickness is needed
        new_width = simpledialog.askinteger("Brush/Eraser Thickness",
                                           "Enter thickness (pixels):",
                                           parent=root, minvalue=1, maxvalue=100, # Increased max thickness
                                           initialvalue=current_width)
        if new_width is None: # If the user pressed "Cancel"
             return # Do not change thickness

    current_width = new_width
    print(f"Brush/Eraser thickness set to: {current_width}") # Debugging

def clear_canvas():
    """Clears the entire canvas."""
    canvas.delete("all") # Deletes all items tagged "all" (i.e., everything)

# --- GUI Setup ---
root = tk.Tk()
root.title("Humming Paint v2.0 (with Eraser!)")

controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# --- Add Tool Buttons ---
pencil_button = tk.Button(controls_frame, text="Pencil", width=8, command=activate_pencil, relief=tk.SUNKEN) # Start with the pencil active
pencil_button.pack(side=tk.LEFT, padx=(5, 2), pady=2)

eraser_button = tk.Button(controls_frame, text="Eraser", width=8, command=activate_eraser, relief=tk.RAISED)
eraser_button.pack(side=tk.LEFT, padx=2, pady=2)

# --- Color Button ---
# Determine the initial text color for the color button
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


# --- Buttons for Brush Thickness ---
width_btn_frame = tk.Frame(controls_frame)
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="2px", width=4, command=lambda: set_width(2)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="5px", width=4, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="10px", width=4, command=lambda: set_width(10)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="20px", width=4, command=lambda: set_width(20)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Custom", width=6, command=lambda: set_width('custom')).pack(side=tk.LEFT) # Pass the string 'custom'

# --- Clear Button ---
clear_button = tk.Button(controls_frame, text="Clear", width=10, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2) # Place on the right

# --- Canvas ---
canvas = tk.Canvas(root, bg=canvas_bg_color, cursor="pencil") # Use the variable for the background color
canvas.pack(fill=tk.BOTH, expand=True) # Make the canvas fill the window

# --- Bind Mouse Events ---
canvas.bind("<Button-1>", start_draw)       # Left mouse button press
canvas.bind("<B1-Motion>", draw)          # Left mouse button drag
canvas.bind("<ButtonRelease-1>", stop_draw) # Left mouse button release

# --- Run ---
# Ensure the initial state is pencil mode
activate_pencil()
root.mainloop() # Start the Tkinter event loop