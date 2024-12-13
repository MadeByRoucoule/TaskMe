import time
import threading
from datetime import datetime
from plyer import notification

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.running = False

    def add_notification(self, title: str, message: str, date_time: datetime):
        self.notifications.append({
            "title": title,
            "message": message,
            "date_time": date_time
        })
        self.notifications.sort(key=lambda x: x['date_time']) 

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            now = datetime.now()
            for notification_task in self.notifications[:]:
                if notification_task["date_time"] <= now:
                    self._send_notification(
                        notification_task["title"], notification_task["message"]
                    )
                    self.notifications.remove(notification_task)
            time.sleep(1)

    def _send_notification(self, title: str, message: str, timeout:int=10):
        notification.notify(
            title=title,
            message=message,
            timeout=timeout
        )
