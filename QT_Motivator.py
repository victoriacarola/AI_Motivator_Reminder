# QT_Motivador.py
import os
import time
import schedule
import threading
from plyer import notification
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QComboBox, QWidget
)
from PyQt5.QtCore import Qt

from ai_quote_generator import generate_motivational_quote

# 🔔 Send task reminder
def task_reminder(task):
    notification.notify(
        title="📌 Task Reminder",
        message=task,
        timeout=10
    )
    print(f"[Reminder] {task} - {datetime.now().strftime('%H:%M:%S')}")

# 🌞 Daily motivational quote
def daily_quote_job():
    quote = generate_motivational_quote()

    # Write to file
    with open("daily_quote.txt", "w", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d')}\n{quote}")

    # Notification
    notification.notify(
        title="🌞 Daily Motivation",
        message=quote,
        timeout=10
    )

    print(f"[AI Quote] {quote}")

# 🕑 Schedule tasks
def schedule_task(task, time_str, repeat="Daily"):
    try:
        if repeat == "Daily":
            schedule.every().day.at(time_str).do(task_reminder, task)
        elif repeat == "Weekly":
            schedule.every().monday.at(time_str).do(task_reminder, task)
        elif repeat == "Hourly":
            schedule.every().hour.at(":00").do(task_reminder, task)
        QMessageBox.information(None, "Task Scheduled", f"✔ '{task}' at {time_str} ({repeat})")
    except schedule.ScheduleValueError:
        QMessageBox.critical(None, "Invalid Time", "Use 24h format HH:MM")

# 🧵 Background scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🌟 Main GUI
class TaskReminderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔮 Neo Task Reminder")
        self.setGeometry(200, 150, 540, 400)
        self.setStyleSheet("""
            QWidget { background-color: #1a1a1a; color: #e0e0e0; font-family: 'Segoe UI'; font-size: 15px; }
            QLabel { font-weight: 500; }
            QLineEdit, QComboBox {
                background-color: #2a2a2a; border: 1px solid #444; border-radius: 8px;
                padding: 8px; color: #fff;
            }
            QPushButton {
                background-color: #3a3aff; color: white; border-radius: 8px;
                padding: 10px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5c5cff; }
            QPushButton:pressed { background-color: #2a2aff; }
        """)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        title_label = QLabel("🚀 Task Reminder Dashboard")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; color: #7df9ff; font-weight: 600;")
        main_layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        task_label = QLabel("📝 Task Description")
        self.task_entry = QLineEdit()
        self.task_entry.setPlaceholderText("e.g., Water the plants")
        form_layout.addWidget(task_label)
        form_layout.addWidget(self.task_entry)

        time_label = QLabel("⏰ Time (HH:MM)")
        self.time_entry = QLineEdit()
        self.time_entry.setPlaceholderText("e.g., 14:30")
        form_layout.addWidget(time_label)
        form_layout.addWidget(self.time_entry)

        repeat_label = QLabel("🔁 Repeat")
        self.repeat_box = QComboBox()
        self.repeat_box.addItems(["Daily", "Weekly", "Hourly"])
        form_layout.addWidget(repeat_label)
        form_layout.addWidget(self.repeat_box)

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        schedule_button = QPushButton("➕ Schedule Task")
        schedule_button.clicked.connect(self.add_task)

        view_button = QPushButton("📋 View Tasks")
        view_button.clicked.connect(self.view_tasks)

        quote_button = QPushButton("🌟 Get Your Daily Quote")
        quote_button.clicked.connect(self.show_daily_quote)

        button_layout.addWidget(schedule_button)
        button_layout.addWidget(view_button)
        button_layout.addWidget(quote_button)

        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_daily_quote(self):
        try:
            quote = generate_motivational_quote()
            QMessageBox.information(self, "🌟 Daily Quote", quote)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate quote:\n{str(e)}")

    def add_task(self):
        task = self.task_entry.text().strip()
        time_str = self.time_entry.text().strip()
        repeat = self.repeat_box.currentText()
        if task and time_str:
            schedule_task(task, time_str, repeat)
            self.task_entry.clear()
            self.time_entry.clear()
        else:
            QMessageBox.warning(self, "⚠️ Missing Info", "Enter both task and time.")

    def view_tasks(self):
        if not schedule.jobs:
            QMessageBox.information(self, "📭 Scheduled Tasks", "No tasks scheduled.")
        else:
            tasks = "\n".join(
                [f"{i+1}. {job.job_func.args[0]} at {job.at_time}" for i, job in enumerate(schedule.jobs) if hasattr(job.job_func, "args")]
            )
            QMessageBox.information(self, "📅 Scheduled Tasks", tasks)

# Schedule daily motivational quote
schedule.every().day.at("08:00").do(daily_quote_job)

# Start scheduler thread
threading.Thread(target=run_scheduler, daemon=True).start()

# Run the App
if __name__ == "__main__":
    app = QApplication([])
    window = TaskReminderApp()
    window.show()
    app.exec_()
