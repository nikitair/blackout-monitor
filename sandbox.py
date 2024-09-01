import datetime
import zoneinfo
from datetime import timezone

t1 = datetime.datetime(2024, 9, 1, 11, 51, 2, 554808, tzinfo=zoneinfo.ZoneInfo(key='GMT'))

t2 = datetime.datetime.now(timezone.utc)

# Calculate the difference
time_diff = t2 - t1

# Extract hours and minutes
hours, remainder = divmod(time_diff.total_seconds(), 3600)
minutes, _ = divmod(remainder, 60)

# Print the difference in hh:mm format
print(f"{int(hours):02} hours {int(minutes):02} minutes")