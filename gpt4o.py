# Code needs to be executed within the virtual environment !! (make your own one)
# Need to install 'requests' and 'pillow' module !!

import base64
import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # Import Pillow library for image processing
import json

# OpenAI API Key
api_key = ""

# Max Tokens : Default = 150
max_tokens = 150

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to open file dialog and get image path
def get_image_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename()  # Open file dialog
    return file_path

# Function to handle "Send" button click event
def send_message(event=None):  # Event parameter added
    user_input = entry.get("1.0", tk.END).strip()  # Get user input from Text widget
    entry.delete("1.0", tk.END)  # Clear the input Text widget

    messages = [{"role": "user", "content": [{"type": "text", "text": user_input}]}]

    if image_path_label['text'] != "":
        image_path = image_path_label['text']
        base64_image = encode_image(image_path)  # Encode image
        messages[0]['content'].append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
        image_path_label['text'] = ""  # Clear the image path label

        # Clear the image preview
        preview_label.config(image=None)  # Clear the image preview
        preview_label.image = None  # Clear the reference to the image

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    response_data = response.json()  # Save response data to variable
    print(response_data)  # Print response data to debug

    # Decode AI response from UTF-8
    ai_response = response.json()['choices'][0]['message']['content']

    # Display AI response in the text widget
    ai_response = response.json().get('choices')[0].get('message').get('content')
    conversation_text.config(state=tk.NORMAL)  # Enable text widget for editing
    conversation_text.insert(tk.END, f"User:\n", "user")  # Insert "User:" with tag "user"
    conversation_text.insert(tk.END, f" {user_input}\n\n")  # Add extra newline
    conversation_text.insert(tk.END, f"AI:\n", "ai")  # Insert "AI:" with tag "ai"
    conversation_text.insert(tk.END, f" {ai_response}\n\n\n")  # Add two extra newlines
    conversation_text.config(state=tk.DISABLED)  # Disable text widget after editing

    # Scroll to the bottom of the text widget
    conversation_text.see(tk.END)

    # Resize the Entry widget based on the content
    update_entry_height()

# Function to handle "Select Image" button click event
def select_image():
    image_path = get_image_path()
    image_path_label['text'] = image_path

    # Display the selected image in a preview widget
    if image_path:
        img = Image.open(image_path)
        img.thumbnail((100, 100))  # Resize image to fit preview area
        img = ImageTk.PhotoImage(img)
        preview_label.config(image=img)
        preview_label.image = img  # Keep a reference to the image to prevent garbage collection

# Function to update the height of the Entry widget based on the content
def update_entry_height():
    entry_height = (len(entry.get("1.0", tk.END)) // 40) + 1  # Calculate the height based on the number of characters
    entry.config(height=entry_height)

# Create main window
root = tk.Tk()
root.title("Chat with AI")

# Create text widget to display conversation
conversation_text = tk.Text(root, wrap="word", state=tk.DISABLED)
conversation_text.pack(expand=True, fill="both")

# Create scrollbar for the text widget
scrollbar = tk.Scrollbar(root, orient="vertical", command=conversation_text.yview)
scrollbar.pack(side="right", fill="y")
conversation_text.configure(yscrollcommand=scrollbar.set)

# Define text tags for styling
conversation_text.tag_configure("user", foreground="blue", font=("Helvetica", 12, "bold"))  # Blue color and bold font for "User:"
conversation_text.tag_configure("ai", foreground="green", font=("Helvetica", 12, "bold"))  # Green color and bold font for "AI:"

# Create "Select Image" button
select_image_button = tk.Button(root, text="Select Image", command=select_image)
select_image_button.pack()

# Label to display selected image path
image_path_label = tk.Label(root, text="")
image_path_label.pack()

# Create a label for image preview
preview_label = tk.Label(root)
preview_label.pack()

# Create Text widget to get user input
entry_frame = tk.Frame(root)
entry_scrollbar = tk.Scrollbar(entry_frame, orient="vertical")
entry = tk.Text(entry_frame, height=8, yscrollcommand=entry_scrollbar.set)  # Text widget for user input with initial height of 8 lines
entry_scrollbar.config(command=entry.yview)
entry_scrollbar.pack(side="right", fill="y")
entry.pack(side="left", fill="both", expand=True)
entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
entry.bind("<Return>", send_message)  # Bind Return key to send_message function

# Run the GUI main loop
root.mainloop()
