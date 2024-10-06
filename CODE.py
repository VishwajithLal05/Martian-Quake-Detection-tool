import os
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar
from PIL import Image, ImageTk

# Function to process and detect the strongest quake (based on highest velocity)
def process_seismic_data(data_directory, output_catalog_file):
    detection_catalog = []

    for filename in os.listdir(data_directory):
        if filename.endswith('.mseed'):
            mseed_file = os.path.join(data_directory, filename)
            st = read(mseed_file)
            tr = st.traces[0].copy()
            tr_times = tr.times()
            tr_data = tr.data
            starttime = tr.stats.starttime.datetime

            # Find the index of the maximum velocity
            max_velocity_index = np.argmax(np.abs(tr_data))
            max_velocity_time = tr_times[max_velocity_index]
            max_velocity_value = tr_data[max_velocity_index]
            max_velocity_abs_time = starttime + timedelta(seconds=max_velocity_time)

            detection_catalog.append({
                'filename': filename,
                'time_abs(%Y-%m-%dT%H:%M:%S.%f)': max_velocity_abs_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                'time_rel(sec)': max_velocity_time,
                'max_velocity(m/s)': max_velocity_value  # Store maximum velocity
            })

            # Plotting
            fig, ax = plt.subplots(1, 1, figsize=(10, 3))
            ax.plot(tr_times, tr_data, label='Velocity (m/s)')
            ax.axvline(x=max_velocity_time, color='red', label='Max Velocity (Detection)')
            ax.set_xlim([min(tr_times), max(tr_times)])
            ax.set_ylabel('Velocity (m/s)')
            ax.set_xlabel('Time (s)')
            ax.set_title(f'{filename}', fontweight='bold')
            ax.legend(loc='upper left')
            # Uncomment below line to show the plot
            plt.show()

    # Create DataFrame and save to CSV
    detection_df = pd.DataFrame(detection_catalog)
    detection_df.to_csv(output_catalog_file, index=False)
    messagebox.showinfo("Process Complete", f"Detection catalog saved to {output_catalog_file}")

# Function to browse for data directory
def browse_data_directory():
    data_dir.set(filedialog.askdirectory())
    data_dir_entry.delete(0, 'end')
    data_dir_entry.insert(0, data_dir.get())

# Function to run seismic detection
def run_detection():
    data_directory = data_dir.get()
    output_catalog_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if not data_directory or not output_catalog_file:
        messagebox.showerror("Input Error", "Please make sure all inputs are provided.")
        return

    process_seismic_data(data_directory, output_catalog_file)

# Create GUI
root = Tk()
root.title("Seismic Detection GUI")

# Set background color
root.configure(bg='#f0f0f0')

# Variables for input fields
data_dir = StringVar()

# Title Label
title_label = Label(root, text="Martian Quake", bg='#f0f0f0', font=('Arial', 20, 'bold'))
title_label.grid(row=0, column=1, padx=10, pady=10)

# Data directory input
Label(root, text="Data Directory:", bg='#f0f0f0', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)
data_dir_entry = Entry(root, textvariable=data_dir, width=50, font=('Arial', 12))
data_dir_entry.grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Browse", command=browse_data_directory, height=1, bg='#4CAF50', fg='black', font=('Arial', 12, 'bold')).grid(row=1, column=2, padx=10, pady=10)

# Image display
image_path = "./images/MartianQuake.png"
img = Image.open(image_path)
img = img.resize((300, 250), Image.LANCZOS)
img = ImageTk.PhotoImage(img)

panel = Label(root, image=img, bg='#f0f0f0')
panel.grid(row=2, column=1, padx=10, pady=10)

# Start button
Button(root, text="Run Detection", command=run_detection, height=1, bg='#008CBA', fg='black', font=('Arial', 12, 'bold')).grid(row=3, column=1, padx=10, pady=10)

# Start GUI loop
root.mainloop()
