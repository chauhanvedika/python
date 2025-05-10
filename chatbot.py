#chatbot 
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import smtplib
from email.mime.text import MIMEText

# Predefined time slots
time_slots = ['10:00 AM', '2:00 PM', '3:30 PM']

# Function to send email
def send_email(recipient, date, time, subject, message_body, student_email):
    sender_email = "vedika20chauhan@gmail.com"          # Your Gmail
    sender_password = "kxyqbddobsueisji"                # App password

    # Complete message including student's email
    full_body = f"You have a new appointment request.\n\nFrom: {student_email}\nDate: {date}\nTime: {time}\n\nMessage:\n{message_body}"

    message = MIMEText(full_body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        result_label.config(text="✅ Email sent successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"❌ Email failed: {e}", fg="red")

# On Submit
def on_submit():
    selected_date = cal.get_date()
    selected_time = time_cb.get()
    student_email = email_entry.get().strip()
    subject = subject_entry.get().strip()
    body = body_text.get("1.0", tk.END).strip()

    if not student_email or not selected_time or not subject or not body:
        result_label.config(text="❗ Please fill all fields.", fg="orange")
        return

    # You are the recipient (Vedika)
    send_email("vedika20chauhan@gmail.com", selected_date, selected_time, subject, body, student_email)

# --- GUI Layout ---
root = tk.Tk()
root.title("Appointment Scheduler")
root.geometry("400x600")

tk.Label(root, text="📅 Select Appointment Date:").pack(pady=5)
cal = Calendar(root, date_pattern="yyyy-mm-dd")
cal.pack(pady=5)

tk.Label(root, text="⏰ Select Time Slot:").pack(pady=5)
time_cb = ttk.Combobox(root, values=time_slots, state="readonly")
time_cb.pack(pady=5)

tk.Label(root, text="📧 Your Email Address:").pack(pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

tk.Label(root, text="📝 Email Subject:").pack(pady=5)
subject_entry = tk.Entry(root, width=40)
subject_entry.pack(pady=5)

tk.Label(root, text="✉️ Message:").pack(pady=5)
body_text = tk.Text(root, height=8, width=40)
body_text.pack(pady=5)

tk.Button(root, text="📨 Submit Appointment Request", command=on_submit).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 10))
result_label.pack()

root.mainloop()
