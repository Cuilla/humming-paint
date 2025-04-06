import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog

# --- Global Variables ---
last_x, last_y = None, None  # Coordinates of the last point
current_color = "black"      # Current drawing color
current_width = 2          # Current line width

# --- Functions ---

def start_draw(event):
    """Called when the mouse button is pressed. Stores the starting coordinates."""
    global last_x, last_y
    last_x, last_y = event.x, event.y
    # Start drawing a point immediately on click
    canvas.create_oval(event.x - current_width/2, event.y - current_width/2,
                       event.x + current_width/2, event.y + current_width/2,
                       fill=current_color, outline=current_color, width=0)


def draw(event):
    """Called when the mouse moves with the button held down. Draws a line."""
    global last_x, last_y
    if last_x is not None and last_y is not None:
        # Draw a line from the last point to the current point
        canvas.create_line(last_x, last_y, event.x, event.y,
                           fill=current_color, width=current_width,
                           capstyle=tk.ROUND, smooth=tk.TRUE)
        # Update the last point
        last_x, last_y = event.x, event.y

def stop_draw(event):
    """Called when the mouse button is released. Resets the coordinates."""
    global last_x, last_y
    last_x, last_y = None, None

def choose_color():
    """Opens the color chooser dialog and sets the selected color."""
    global current_color
    # askcolor returns a tuple ((R, G, B), '#rrggbb') or (None, None) if cancelled
    color_code = colorchooser.askcolor(title="Choose Color for Humming Paint")
    if color_code[1]: # If a color was chosen (not None)
        current_color = color_code[1]
        # Optional: Add a visual indicator for the current color
        color_button.config(bg=current_color, activebackground=current_color)
        # Make button text visible on dark backgrounds
        try:
            # Simple check for color brightness
            r, g, b = root.winfo_rgb(current_color) # Returns values 0-65535
            brightness = (r + g + b) / 3 / 65535
            if brightness < 0.5:
                color_button.config(fg='white', activeforeground='white')
            else:
                color_button.config(fg='black', activeforeground='black')
        except tk.TclError: # Handle potential errors if color name is invalid
             color_button.config(fg='black', activeforeground='black')


def set_width(size):
    """Sets the line width."""
    global current_width
    if size: # Ensure size is not None (e.g., if user cancels the dialog)
        current_width = size
        print(f"Brush width set to: {current_width}") # For debugging

def clear_canvas():
    """Clears the entire canvas."""
    canvas.delete("all") # Deletes all items tagged "all" (i.e., everything)

# --- GUI Setup ---

# 1. Create the main window
root = tk.Tk()
root.title("Humming Paint v0.1")

# 2. Create a frame for control buttons
controls_frame = tk.Frame(root, bd=2, relief=tk.RAISED)
controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# 3. Control Buttons
color_button = tk.Button(controls_frame, text="Color", width=10, command=choose_color, bg=current_color, fg='white', activebackground=current_color, activeforeground='white')
color_button.pack(side=tk.LEFT, padx=5, pady=2)

# Buttons for brush width
width_btn_frame = tk.Frame(controls_frame) # Nested frame for width buttons
width_btn_frame.pack(side=tk.LEFT, padx=5)

tk.Button(width_btn_frame, text="Thin", width=6, command=lambda: set_width(2)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Medium", width=6, command=lambda: set_width(5)).pack(side=tk.LEFT)
tk.Button(width_btn_frame, text="Thick", width=6, command=lambda: set_width(10)).pack(side=tk.LEFT)
# Button for custom width
tk.Button(width_btn_frame, text="Custom", width=6, command=lambda: set_width(simpledialog.askinteger("Brush Width", "Enter width (pixels):", parent=root, minvalue=1, maxvalue=50, initialvalue=current_width))).pack(side=tk.LEFT)

clear_button = tk.Button(controls_frame, text="Clear", width=10, command=clear_canvas)
clear_button.pack(side=tk.RIGHT, padx=5, pady=2) # Place on the right

# 4. Create the drawing canvas
canvas = tk.Canvas(root, bg="white", cursor="pencil") # Set white background and pencil cursor
canvas.pack(fill=tk.BOTH, expand=True) # Expand the canvas to fill available space

# 5. Bind mouse events to functions
canvas.bind("<Button-1>", start_draw)       # Left mouse button press
canvas.bind("<B1-Motion>", draw)          # Mouse movement with left button held
canvas.bind("<ButtonRelease-1>", stop_draw) # Left mouse button release

# --- Start the main application loop ---
root.mainloop()