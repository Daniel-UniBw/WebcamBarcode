import cv2
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os
from pyzbar.pyzbar import decode
import numpy as np

# Create the "Images" directory if it doesn't exist
os.makedirs("Images", exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(0)

def capture_image():
    # Capture current frame
    ret, frame = cap.read()
    if ret:
        # Save frame as an image
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        filepath = os.path.join("Images", filename)
        cv2.imwrite(filepath, frame)
        messagebox.showinfo("Image Captured", f"Image saved as {filename}")


def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame2Display = Image.fromarray(frame)
        frame2Display = ImageTk.PhotoImage(frame2Display)
        label.config(image=frame2Display)
        label.image = frame2Display

        # Read and display barcode if present
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        decoded = decode(thresh)
        if decoded:
            content = decoded[0].data.decode("utf-8")
            editbox.delete(0, tk.END)
            editbox.insert(0, content)
        else:
            editbox.delete(0, tk.END)
            editbox.insert(0, "No barcode found")



    root.after(10, update_frame)

def on_keypress(event):
    if event.keysym == 'space':
        capture_image()

root = tk.Tk()
root.title("Webcam Stream with Barcode Reader")
root.bind('<KeyPress>', on_keypress)

frame = tk.Frame(root)
frame.pack()

label = ttk.Label(frame)
label.pack()

editbox = ttk.Entry(root, width=50)
editbox.pack(pady=10)

update_frame()
root.mainloop()

# Release webcam
cap.release()
