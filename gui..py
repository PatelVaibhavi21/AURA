import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk  # For image loading (microphone icon)
import threading
import time
import math  # For creating wave-like coordinates

# Dummy backend functions (as before)
def dummy_get_command():
    print("Simulating voice command...")
    time.sleep(2)
    return "what's the weather in Mumbai"

def dummy_speak(text):
    print(f"Assistant says: {text}")
    output_text.insert(tk.END, f"Assistant: {text}\n")
    output_text.see(tk.END)

def dummy_get_weather(city):
    dummy_speak(f"Simulating weather in {city}...")
    dummy_speak("Temperature: 30 degrees Celsius, Sunny.")

def run_assistant():
    command = dummy_get_command()
    if command:
        output_text.insert(tk.END, f"You said: {command}\n")
        output_text.see(tk.END)
        if "weather in" in command:
            city = command.replace("weather in", "").strip()
            dummy_get_weather(city)
        else:
            dummy_speak("Sorry, I can't process that yet in the visual GUI.")

def start_assistant():
    threading.Thread(target=run_assistant).start()

# --- GUI Setup with Canvas ---
window = tk.Tk()
window.title("Visual Voice Assistant")

canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="#222831") # Dark background
canvas.pack(pady=10)

# Load Microphone Icon (replace with your actual path)
try:
    mic_img = Image.open("microphone_icon.png").resize((50, 70))
    mic_icon = ImageTk.PhotoImage(mic_img)
    mic_x = canvas_width // 2 - 25
    mic_y = canvas_height // 2 - 35
    canvas.create_image(mic_x, mic_y, anchor=tk.NW, image=mic_icon)
except FileNotFoundError:
    canvas.create_oval(canvas_width // 2 - 20, canvas_height // 2 - 30,
                       canvas_width // 2 + 20, canvas_height // 2 + 10, fill="cyan") # Placeholder circle

# Draw radiating circles (static)
center_x = canvas_width // 2
center_y = canvas_height // 2
for i in range(3):
    radius = 30 + i * 20
    color = f"#44{50+i*30:02x}{88+i*30:02x}" # Fading blue-purple
    canvas.create_oval(center_x - radius, center_y - radius,
                       center_x + radius, center_y + radius,
                       outline=color, width=2)

# Draw simple wave-like lines (static)
wave_amplitude = 30
wave_frequency = 0.05
for i in range(2):
    points = []
    start_y = canvas_height // 2 + (i - 0.5) * 80
    color = "#66CCFF" if i == 0 else "#FF66CC"
    for x in range(canvas_width):
        y = int(start_y + wave_amplitude * math.sin(wave_frequency * x + i * math.pi))
        points.append((x, y))
    canvas.create_line(points, fill=color, width=2, smooth=True)

# Output Text Area
output_label = tk.Label(window, text="Assistant Responses:")
output_label.pack(pady=5)
output_text = scrolledtext.ScrolledText(window, height=5, width=50)
output_text.pack(pady=5)

# Invisible Button Overlay (to trigger action on the central area)
button_area_size = 80
button_x1 = canvas_width // 2 - button_area_size // 2
button_y1 = canvas_height // 2 - button_area_size // 2
button_x2 = canvas_width // 2 + button_area_size // 2
button_y2 = canvas_height // 2 + button_area_size // 2

invisible_button = tk.Button(window, text="", command=start_assistant, relief=tk.FLAT, bg="#222831", activebackground="#222831", bd=0, highlightthickness=0)
invisible_button.place(x=button_x1, y=button_y1, width=button_area_size, height=button_area_size)

window.mainloop()