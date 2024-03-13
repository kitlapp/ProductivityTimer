from tkinter import *
from PIL import ImageTk
from datetime import datetime

# Set the constants.
YELLOW = "#f7f5dd"
FONT_NAME = "Calibri"
WORK_MIN = 25 * 60

# Initialize variables.
is_paused = False
is_reset = False
is_running = False
should_start = True
daily_sessions = 0

# Create the application window.
window = Tk()
window.title("Productivity Timer")
window.config(width=1000, height=600)


def is_pause_status():
    """
Pauses the timer when pause button is pressed.
    """
    global is_paused, should_start
    if is_running:  # Prevents bugs from multiple and consecutive pause presses.
        is_paused = True
    should_start = True  # If timer paused, this should be true.


def reset_status():
    """
Resets the timer when reset button is pressed.
    """
    global is_reset, WORK_MIN, should_start
    if is_running:  # Prevents bugs from multiple and consecutive reset presses
        # Prevents timer from a delay on start press when reset is pressed after a pause.
        is_reset = True
    WORK_MIN = 25 * 60  # Reset variable.
    canvas.itemconfig(timer, text="25:00")  # Reset timer.
    should_start = True  # If timer reset, this should be true.


def should_start_status():
    """
Starts countdown ONLY if not already running.
    """
    if should_start:
        start_countdown()


def start_countdown():
    """
Manages the countdown timer and updates the display.
    """
    global WORK_MIN, is_paused, daily_sessions, is_reset, is_running, should_start
    if WORK_MIN >= 0 and not is_paused and not is_reset:
        minutes, seconds = divmod(WORK_MIN, 60)
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        canvas.itemconfig(timer, text=formatted_time)
        is_running = True
        WORK_MIN -= 1
        window.after(1000, start_countdown)  # Updates every second.
        should_start = False
        if WORK_MIN < 0:
            daily_sessions += 1
            reset_status()
    else:
        is_paused = False
        is_running = False
        is_reset = False


def show_history():
    """
Displays the daily study history for 3 seconds when the history button is pressed.
    """
    global daily_sessions
    total_hours, total_minutes = divmod(daily_sessions * 25, 60)
    daily_study_time = f"Study Today: {total_hours:02d} hours {total_minutes:02d} minutes"
    canvas.itemconfig(history_text, text=daily_study_time)
    window.after(3000, delete_history_text)  # Deletes after 3 seconds.


def delete_history_text():
    """
Deletes the displayed study history text.
    """
    canvas.itemconfig(history_text, text="")


def hover_over_button(event):
    """
Highlights a button when the mouse pointer hovers over it.
    :param event:
    """
    event.widget.config(bg=YELLOW)


def on_leave(event):
    """
Resets the background color of the button when the mouse pointer leaves it.
    """
    event.widget.config(bg="white")


def update_clock():
    """
Updates clock and date on screen every second
    """
    clock = datetime.now()
    formatted_time = clock.strftime("%I:%M %p")
    formatted_date = clock.strftime("%d %B")
    canvas.itemconfig(clock_displayed_text, text=formatted_time)
    canvas.itemconfig(date_displayed_text, text=formatted_date)
    window.after(1000, update_clock)  # Updates every second.


for_image = ImageTk.PhotoImage(file="forest.jpg")  # Creates a background forest image.

canvas = Canvas(width=1000, height=600, highlightthickness=0)  # Creates the canvas.

# Creates canvas widgets:
canvas.create_image(500, 300, image=for_image)
timer = canvas.create_text(500, 300, text="25:00", fill="white", font=(FONT_NAME, 35, "bold"))
timer_text = canvas.create_text(500, 250, text="Timer", fill="white", font=(FONT_NAME, 35, "bold"))
history_text = canvas.create_text(500, 490, text="", fill="white", font=(FONT_NAME, 20, "bold"))
clock_displayed_text = canvas.create_text(900, 550, text="", fill="white", font=(FONT_NAME, 20, "bold"))
date_displayed_text = canvas.create_text(880, 575, text="", fill="white", font=(FONT_NAME, 12, "bold"))

update_clock()

canvas.pack(fill="both", expand=True)

#  Creates the start button.
start_button = Button(text="Start", font=(FONT_NAME, 12, "bold"), command=should_start_status, bg="white", fg="green",
                      highlightthickness=0)
start_button_window = canvas.create_window(500, 400, window=start_button)
start_button.bind("<Enter>", hover_over_button)
start_button.bind("<Leave>", on_leave)

# Creates the pause button.
pause_button = Button(text="Pause", font=(FONT_NAME, 12, "bold"), command=is_pause_status, bg="white", fg="green",
                      highlightthickness=0)
pause_button_window = canvas.create_window(400, 400, window=pause_button)
pause_button.bind("<Enter>", hover_over_button)
pause_button.bind("<Leave>", on_leave)

# Creates the reset button.
reset_button = Button(text="Reset", font=(FONT_NAME, 12, "bold"), command=reset_status, bg="white", fg="green",
                      highlightthickness=0)
reset_button_window = canvas.create_window(600, 400, window=reset_button)
reset_button.bind("<Enter>", hover_over_button)
reset_button.bind("<Leave>", on_leave)

# Creates the history button.
history_button = Button(text="History", font=(FONT_NAME, 12, "bold"), command=show_history, bg="white", fg="green",
                        highlightthickness=0)
history_button_window = canvas.create_window(500, 460, window=history_button)
history_button.bind("<Enter>", hover_over_button)
history_button.bind("<Leave>", on_leave)

window.mainloop()
