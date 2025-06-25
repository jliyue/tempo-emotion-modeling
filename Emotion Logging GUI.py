import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import Button, TextBox
import pandas as pd
from datetime import datetime
import time
import numpy as np
import os

# Set the download path to your computer here
download_path = ""

# List to store emotions (time, valence, arousal)
emotions = []
start_time = None
logging_enabled = False
song_filename = "unknown_song"
scatters = [] 

def update_filename(text):
    """Update the song filename from the input box."""
    global song_filename
    song_filename = text
    print(f"Song filename updated to: {song_filename}")

def start_logging(event):
    """Start the timer and enable logging."""
    global start_time, logging_enabled
    if not logging_enabled:
        start_time = time.time()  # Record the start time
        logging_enabled = True
        print("Logging started! Timer is running...")
    else:
        print("Logging is already running.")

def end_logging(event):
    """Stop the timer and disable logging."""
    global start_time, logging_enabled
    if logging_enabled:
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        logging_enabled = False
        print(f"Logging ended. Total time elapsed: {elapsed_time:.2f} seconds.")
    else:
        print("Logging is not running.")
        
def determine_quadrant_color(x, y):
    """Determine the quadrant color based on valence (x) and arousal (y) values."""
    if x >= 0 and y >= 0:
        return "Green"
    elif x < 0 and y >= 0:
        return "Yellow"
    elif x < 0 and y < 0:
        return "Red"
    elif x >= 0 and y < 0:
        return "Blue"
    return "Unknown"  # Default case

def onclick(event):
    """Handles clicks to log valence/arousal only on user interaction inside the plot area."""
    global logging_enabled
    if event.inaxes != ax:  # Ignore clicks outside the main plot area
        return
    
    if logging_enabled and event.button == MouseButton.LEFT:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:  # Ensure valid data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            quadrant_color = determine_quadrant_color(x, y)
            
            if quadrant_color:  # Ensure quadrant_color is assigned
                emotions.append((timestamp, song_filename, x, y, quadrant_color))
                print(f'Logged Emotion: Time={timestamp}, Song={song_filename}, Valence={x:.2f}, Arousal={y:.2f}, Quadrant={quadrant_color}')
                
                # Plot the point on click
                scatter = ax.scatter(x, y, color='black', s=100)
                scatters.append(scatter)
                plt.draw()
            else:
                print("Error: Quadrant color not determined correctly.")
    elif not logging_enabled:
        print("Please click the 'Start' button to begin logging.")
        

def save_emotions(event):
    """Save emotions to a CSV file and the figure as an image in the Downloads folder."""
    if emotions:
        print("Saving emotions, verifying structure...")
        print(emotions)  # Debugging output
        
        filename = os.path.join(download_path, f'emotions_log_{song_filename}.csv') #Set desired name here
        image_filename = os.path.join(download_path, f'emotions_log_{song_filename}.png') #Set desired name here
        
        try:
            df = pd.DataFrame(emotions, columns=['Timestamp', 'Song', 'Valence', 'Arousal', 'Quadrant Color'])
            df.to_csv(filename, index=False)
            print(f"Emotions saved to '{filename}'.")
            
            # Save the figure as an image
            fig.savefig(image_filename, dpi=300, bbox_inches='tight')
            print(f"Figure saved as '{image_filename}'.")
        except ValueError as e:
            print("Error saving emotions: ", e)
            print("Check if all logged entries have the expected 5 columns.")
    else:
        print("No emotions logged to save.")

def clear_coordinates(event):
    """Clear only logged scatter points while preserving the rest of the graph."""
    global emotions, scatters
    emotions.clear()
    for scatter in scatters:
        scatter.remove()
    scatters.clear()
    plt.draw()
    print("Logged emotions cleared.")

  


# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_xlabel('Valence (-1 to 1)', fontsize=12, fontweight='bold')
ax.set_ylabel('Arousal (-1 to 1)', fontsize=12, fontweight='bold')
ax.grid(True)
ax.set_title('Click to Log Emotions on Arousal-Valence Model', fontsize=14, fontweight='bold')
ax.set_aspect('equal', adjustable='box')


# Add x-axis and y-axis lines with arrows
ax.annotate('', xy=(1, 0), xytext=(-1, 0),
            arrowprops=dict(arrowstyle='<|-|>', color='black', linewidth=2))
ax.annotate('', xy=(0, 1), xytext=(0, -1),
            arrowprops=dict(arrowstyle='<|-|>', color='black', linewidth=2))

# Emotion labels evenly spaced in a circle
emotion_labels = [
    ("Excited", 67),
    ("Delighted", 45),
    ("Happy", 22),
    ("Content", -22),
    ("Relaxed", -45),
    ("Calm", -67),
    ("Tired", -113),
    ("Bored", -135),
    ("Depressed", -158),
    ("Frustrated", 158),
    ("Angry", 135),
    ("Tense", 113)
]

# Convert angles to radians and calculate coordinates
radius = 0.9  # Adjust the radius of the circle if necessary
coordinates = {emotion: (radius * np.cos(np.radians(angle)), radius * np.sin(np.radians(angle))) for emotion, angle in emotion_labels}

# Plot the labels
for emotion, (x, y) in coordinates.items():
    ax.text(x, y, emotion, fontsize=10, ha='center', va='center')

# Add a circular boundary for visual reference
circle = plt.Circle((0, 0), 1, color='black', fill=False, linestyle='--', linewidth=0.8)
ax.add_artist(circle)

# Draw quadrants with colors
ax.fill_between([-1, 0], 0, 1, color='yellow', alpha=0.3)
ax.fill_between([0, 1], 0, 1, color='green', alpha=0.3)
ax.fill_between([-1, 0], -1, 0, color='red', alpha=0.3)
ax.fill_between([0, 1], -1, 0, color='blue', alpha=0.3)


# Add labels for axes
ax.text(.88, .5, 'Positive', fontsize=14, color='grey',verticalalignment='center', transform=ax.transAxes)
ax.text(.02, .5, 'Negative', fontsize=14,color='grey', verticalalignment='center', transform=ax.transAxes)
ax.text(0.5, .98, 'High', fontsize=14,color='grey', horizontalalignment='center', transform=ax.transAxes)
ax.text(0.5, .02, 'Low', fontsize=14, color='grey', horizontalalignment='center', transform=ax.transAxes)



# Connect click events
fig.canvas.mpl_connect('button_press_event', onclick)

# Add UI elements
ax_textbox = plt.axes([0.1, 0.01, 0.3, 0.05])
text_box = TextBox(ax_textbox, 'Song File:', initial=song_filename)
text_box.on_submit(update_filename)

ax_button_start = plt.axes([0.55, 0.01, 0.1, 0.05])
btn_start = Button(ax_button_start, 'Start')
btn_start.on_clicked(start_logging)

ax_button_end = plt.axes([0.67, 0.01, 0.1, 0.05])
btn_end = Button(ax_button_end, 'End')
btn_end.on_clicked(end_logging)

ax_button_save = plt.axes([0.79, 0.01, 0.1, 0.05])
btn_save = Button(ax_button_save, 'Save')
btn_save.on_clicked(save_emotions)

ax_button_clear = plt.axes([0.91, 0.01, 0.1, 0.05])
btn_clear = Button(ax_button_clear, 'Clear')
btn_clear.on_clicked(clear_coordinates)

plt.show()
