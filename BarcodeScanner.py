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

current_barcode = None
last_barcode_time = None

def capture_image(barcode=None):
    global current_barcode, last_barcode_time

    # Capture current frame
    ret, frame = cap.read()
    if ret:
        if barcode:
            filename = f"{barcode}.png"
        else:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        filepath = os.path.join("Images", filename)
        cv2.imwrite(filepath, frame)
        messagebox.showinfo("Image Captured", f"Image saved as {filename}")

    current_barcode = None
    last_barcode_time = None

def update_frame():
    global current_barcode, last_barcode_time

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        decoded = decode(thresh)

        if decoded:
            barcode = decoded[0]
            x, y, w, h = barcode.rect.left, barcode.rect.top, barcode.rect.width, barcode.rect.height
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            current_barcode = barcode.data.decode("utf-8")
            last_barcode_time = datetime.now()
            editbox.delete(0, tk.END)
            editbox.insert(0, current_barcode)
        elif current_barcode and (datetime.now() - last_barcode_time).seconds >= 10:
            current_barcode = None
            editbox.delete(0, tk.END)
            editbox.insert(0, "No barcode found")

        frame2Display = Image.fromarray(frame)
        frame2Display = ImageTk.PhotoImage(frame2Display)
        label.config(image=frame2Display)
        label.image = frame2Display

    root.after(10, update_frame)


def on_keypress(event):
    if event.keysym == 'space' and current_barcode:
        capture_image(current_barcode)
    elif event.keysym == 'space':
        capture_image()
    elif event.keysym == 'Escape':  # Handling ESC key press
        cap.release()  # Release the webcam
        root.quit()    # Stop the Tkinter main loop


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
