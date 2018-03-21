from datetime import datetime

now = datetime.now()

format_iso_now = now.isoformat(timespec = "seconds")

print(format_iso_now)