import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def create_event(service, title, desc, start_time):
    event = {
        'summary': title,
        'description': desc,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (start_time + timedelta(hours=1)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def submit_event():
    title = entry_title.get()
    desc = entry_desc.get()
    selected_date = cal.get_date()
    selected_hour = hour_var.get()
    selected_minute = minute_var.get()

    try:
        start_time_str = f"{selected_date} {selected_hour}:{selected_minute}"
        start_time = datetime.strptime(start_time_str, "%m/%d/%y %H:%M")
        link = create_event(service, title, desc, start_time)
        messagebox.showinfo("Success", f"Event created!\n\nView it here:\n{link}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Authenticate once at start
service = authenticate_google()

# GUI Section
root = tk.Tk()
root.title("Google Calendar Appointment Scheduler")

tk.Label(root, text="Event Title:").grid(row=0, column=0)
entry_title = tk.Entry(root, width=40)
entry_title.grid(row=0, column=1)

tk.Label(root, text="Description:").grid(row=1, column=0)
entry_desc = tk.Entry(root, width=40)
entry_desc.grid(row=1, column=1)

tk.Label(root, text="Select Date:").grid(row=2, column=0)
cal = Calendar(root, selectmode='day', date_pattern='mm/dd/yy')
cal.grid(row=2, column=1, pady=5)

tk.Label(root, text="Select Hour (0–23):").grid(row=3, column=0)
hour_var = tk.StringVar(value="12")
hour_spinbox = tk.Spinbox(root, from_=0, to=23, width=5, textvariable=hour_var, format="%02.0f")
hour_spinbox.grid(row=3, column=1, sticky='w')

tk.Label(root, text="Select Minute (0–59):").grid(row=4, column=0)
minute_var = tk.StringVar(value="00")
minute_spinbox = tk.Spinbox(root, from_=0, to=59, width=5, textvariable=minute_var, format="%02.0f")
minute_spinbox.grid(row=4, column=1, sticky='w')

submit_btn = tk.Button(root, text="Create Calendar Event", command=submit_event)
submit_btn.grid(row=5, columnspan=2, pady=10)

root.mainloop()
