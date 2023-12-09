import tkinter as tk
from tkinter import ttk, messagebox
import time
import winsound
import threading

class DigitalClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("🕰️ Floating Digital Clock - ❤️-From Thiarara V1.5")
        self.attributes('-topmost', 1)  # This line makes the window stay on top

        self.dark_theme = True
        self.alarm_times = []
        self.alarm_active = False  # Flag to track whether the alarm is currently active

        self.configure_ui()

        self.update_time()

        # Bind the function to handle window closure
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_ui(self):
        self.configure(background='black' if self.dark_theme else 'white')

        self.clock_label = tk.Label(self, font=('arial', 80, 'bold'), bg='black' if self.dark_theme else 'white', fg='white' if self.dark_theme else 'black')
        self.clock_label.grid(row=0, column=0, columnspan=5, pady=10)

        self.theme_button = tk.Button(self, text='Switch to Light Theme' if self.dark_theme else 'Switch to Dark Theme', command=self.toggle_theme)
        self.theme_button.grid(row=1, column=0, columnspan=5, pady=5)

        self.view_more_button = tk.Button(self, text='View More', command=self.toggle_view_more)
        self.view_more_button.grid(row=2, column=0, columnspan=5, pady=5, sticky='nsew')  # Use sticky to center and expand the button

        # Additional widgets initially hidden
        self.label_alarm = tk.Label(self, text='Alarm Time:', font=('arial', 12, 'bold'), bg='black' if self.dark_theme else 'white', fg='white' if self.dark_theme else 'black')
        self.alarm_entry_var = tk.StringVar()
        self.alarm_entry = tk.Entry(self, textvariable=self.alarm_entry_var)
        self.add_placeholder(self.alarm_entry, 'Enter alarm time...')
        self.add_alarm_button = tk.Button(self, text='Add Alarm', command=self.add_alarm)
        self.label_sound = tk.Label(self, text='Select Alarm Sound:', font=('arial', 12, 'bold'), bg='black' if self.dark_theme else 'white', fg='white' if self.dark_theme else 'black')
        self.sound_combobox = ttk.Combobox(self, values=['Default Beep', 'System Exclamation', 'System Hand', 'System Question'])
        self.sound_combobox.set('Default Beep')
        self.label_alarm_list = tk.Label(self, text='Alarm List:', font=('arial', 12, 'bold'), bg='black' if self.dark_theme else 'white', fg='white' if self.dark_theme else 'black')
        self.alarm_listbox = tk.Listbox(self)
        self.delete_alarm_button = tk.Button(self, text='Delete Alarm', command=self.delete_alarm)
        self.stop_button = tk.Button(self, text='Stop Alarm', command=self.stop_alarm, state=tk.DISABLED)

        for widget in [self.label_alarm, self.alarm_entry, self.add_alarm_button,
                       self.label_sound, self.sound_combobox, self.label_alarm_list,
                       self.alarm_listbox, self.delete_alarm_button, self.stop_button]:
            widget.grid_remove()

        # Set up column configuration to make the first column expandable
        self.columnconfigure(0, weight=1)  # Make the first column expandable

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda event, placeholder=placeholder: self.on_entry_focusin(event, entry, placeholder))
        entry.bind('<FocusOut>', lambda event, placeholder=placeholder: self.on_entry_focusout(event, entry, placeholder))

    def on_entry_focusin(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')  # Change text color when user is typing

    def on_entry_focusout(self, event, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')  # Change text color back to grey

    def toggle_view_more(self):
        # Toggle the visibility of additional widgets
        for widget in [self.label_alarm, self.alarm_entry, self.add_alarm_button,
                       self.label_sound, self.sound_combobox, self.label_alarm_list,
                       self.alarm_listbox, self.delete_alarm_button, self.stop_button]:
            if widget.winfo_ismapped():  # Check if the widget is currently visible
                widget.grid_remove()
            else:
                widget.grid(sticky='nsew', padx=10, pady=5)  # Use sticky and padx/pady for margin and padding

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.clock_label.after(1000, self.update_time)

        # Check if any alarm should sound
        for alarm_time in self.alarm_times:
            if time.strftime("%H:%M") == alarm_time and not self.alarm_active:
                threading.Thread(target=self.trigger_alarm).start()

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme  # Toggle the theme
        self.configure(background='black' if self.dark_theme else 'white')

        theme_text = 'Switch to Light Theme' if self.dark_theme else 'Switch to Dark Theme'
        self.theme_button.config(text=theme_text)

        for widget in [self.clock_label, self.theme_button, self.view_more_button]:
            widget.configure(bg='black' if self.dark_theme else 'white', fg='white' if self.dark_theme else 'black')

        # Update color of entry widgets based on the theme
        entry_widgets = [self.alarm_entry]
        for entry_widget in entry_widgets:
            current_text = entry_widget.get()
            if current_text != 'Enter alarm time...' and current_text != 'Select alarm sound...':
                entry_widget.config(fg='black' if self.dark_theme else 'grey')
            else:
                entry_widget.config(fg='grey' if self.dark_theme else 'black')

    def add_alarm(self):
        alarm_time = self.alarm_entry_var.get()
        if alarm_time and alarm_time != 'Enter alarm time...' and alarm_time not in self.alarm_times:
            self.alarm_times.append(alarm_time)
            self.alarm_listbox.insert(tk.END, alarm_time)
        else:
            messagebox.showwarning("Invalid Alarm", "Please enter a valid and unique alarm time.")

    def delete_alarm(self):
        selected_alarm = self.alarm_listbox.curselection()
        if selected_alarm:
            self.alarm_listbox.delete(selected_alarm)
            self.alarm_times.pop(selected_alarm[0])

    def trigger_alarm(self):
        selected_sound = self.sound_combobox.get()
        try:
            self.alarm_active = True  # Set the alarm active flag
            self.stop_button.config(state=tk.NORMAL)  # Enable the stop button
            winsound.PlaySound(selected_sound, winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            messagebox.showerror("Sound Error", f"Error playing selected sound: {str(e)}")
        finally:
            self.alarm_active = False  # Reset the alarm active flag
            self.stop_button.config(state=tk.DISABLED)  # Disable the stop button

    def stop_alarm(self):
        winsound.PlaySound(None, winsound.SND_ALIAS)  # Stop the alarm sound
        self.stop_button.config(state=tk.DISABLED)  # Disable the stop button

    def on_close(self):
        # Stop the alarm and perform any necessary cleanup when the window is closed
        if self.alarm_active:
            self.stop_alarm()
        self.destroy()

if __name__ == "__main__":
    app = DigitalClockApp()
    app.mainloop()
