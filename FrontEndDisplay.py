import tkinter as tk
from ufcRatings import *
from PIL import Image, ImageTk

# Retrieve fighter data
fighters_data = process_fights()

root = tk.Tk()
root.title("UFC Fighter Ratings")
root.geometry("600x800")
root.configure(bg="#2C3E50")  


FONT_LARGE = ("Arial", 20, "bold")
FONT_MEDIUM = ("Arial", 16)
FONT_SMALL = ("Arial", 12)
BUTTON_STYLE = {
    "font": ("Arial", 12, "bold"),
    "bg": "#1ABC9C",  
    "fg": "white",
    "activebackground": "#16A085",  
    "activeforeground": "white",
    "relief": tk.RAISED,
    "width": 15,
    "pady": 10
}

# Main frames
top_frame = tk.Frame(root, bg="#34495E")  # Slightly lighter dark blue-gray
top_frame.pack(side=tk.TOP, pady=20, fill="x")

content_frame = tk.Frame(root, bg="#2C3E50")  # Matches the root background
content_frame.pack(expand=True, fill="both", pady=20)

bottom_frame = tk.Frame(root, bg="#34495E")
bottom_frame.pack(side=tk.BOTTOM, pady=20, fill="x")

# Widgets for fighter details
image_label = tk.Label(content_frame, bg="#2C3E50")
label = tk.Label(content_frame, text="Name:", font=FONT_LARGE, bg="#2C3E50", fg="white")
label_2 = tk.Label(content_frame, text="Rating:", font=FONT_MEDIUM, bg="#2C3E50", fg="white")
label_3 = tk.Label(content_frame, text="Class:", font=FONT_MEDIUM, bg="#2C3E50", fg="white")
label_5 = tk.Label(content_frame, text="UFC Record:", font=FONT_MEDIUM, bg="#2C3E50", fg="white")

label.pack(pady=10)
label_2.pack(pady=10)
label_3.pack(pady=10)
label_5.pack(pady=10)

# Textbox for user input
label_4 = tk.Label(content_frame, text="Enter Fighter's Name:", font=FONT_MEDIUM, bg="#2C3E50", fg="white")
label_4.pack(pady=10)

textbox = tk.Text(content_frame, height=2, width=30, font=FONT_SMALL, wrap="word", bg="#ECF0F1", fg="#2C3E50")
textbox.pack(pady=10)

def get_textbox_content():
    global current_index
    content = textbox.get("1.0", tk.END).strip()
    index = None 
    for key, fighter in enumerate(fighters_data):
        if fighter["Name"] == content:
            index = key
            break
    if index is not None:
        current_index = index
        loop_fighters(0)
    else:
        print("Fighter not found!")

submit_button = tk.Button(content_frame, text="Submit", command=get_textbox_content, font=FONT_SMALL, bg="#1ABC9C", fg="white")
submit_button.pack(pady=10)


current_index = 0

# Label for displaying the image
label_image = tk.Label(content_frame, bg="#2C3E50")
label_image.pack(pady=20)

def loop_fighters(direction):
    global current_index, label_image
    current_index = (current_index + direction) % len(fighters_data)  # Wrap around list
    fighter = fighters_data[current_index]

    
    label.config(text=f"Name: {fighter['Name']}")
    label_2.config(text=f"Rating: {fighter['Rating']}")
    label_3.config(text=f"Class: {fighter['Class']}")
    label_5.config(text=f"UFC Record: {fighter['Record']}")

    
    image_path = fr"FILE_PATH\athlete_images\{fighter['Name'].replace(' ', '_')}.png"
    try:
        image = Image.open(image_path)
        image = image.resize((300, 300))
        tk_image = ImageTk.PhotoImage(image)
        label_image.config(image=tk_image)
        label_image.image = tk_image
    except FileNotFoundError:
        label_image.config(text="Image not found", image="")
        label_image.image = None

    
    class_colors = {
        "Gold": "#FFD700",  
        "Silver": "#C0C0C0", 
        "Bronze": "#CD7F32",  
        "Diamond": "#87CEFA",  
        "Platnium": "#DDA0DD"  
    }
    bg_color = class_colors.get(fighter["Class"], "#2C3E50") 
    content_frame.configure(bg=bg_color)

def sort_ratings():
    global fighters_data, current_index
    fighters_data.sort(key=lambda x: x["Rating"], reverse=True)
    current_index = 0
    loop_fighters(0)


sort_button = tk.Button(top_frame, text="Sort By Rating", command=sort_ratings, **BUTTON_STYLE)
forward_button = tk.Button(bottom_frame, text="Next", command=lambda: loop_fighters(1), **BUTTON_STYLE)
backward_button = tk.Button(bottom_frame, text="Previous", command=lambda: loop_fighters(-1), **BUTTON_STYLE)

sort_button.pack(pady=10)
backward_button.pack(side=tk.LEFT, padx=20)
forward_button.pack(side=tk.RIGHT, padx=20)


loop_fighters(0)

root.mainloop()
