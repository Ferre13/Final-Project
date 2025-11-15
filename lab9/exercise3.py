class TimeInterval:
    """
    Time interval represented by initial and final instant (hours and minutes).
    Morning (6:00 - 12:00), afternoon (12:00 - 18:00), evening (18:00 - 0:00) and night (0:00 - 6:00). Can belong to more than one (10:00 - 14:00).
    """
    def __init__(self, initial_hour: int, initial_minutes: int, final_hour: int, final_minutes: int):
        self.initial_hour = initial_hour
        self.initial_minutes = initial_minutes
        self.final_hour = final_hour
        self.final_minutes = final_minutes

        night_end = 360 # 6:00
        morning_end = 720 # 12:00
        afternoon_end = 1080 # 18:00
        evening_end = 1440 # 0:00

        initial_time = initial_hour * 60 + initial_minutes
        final_time = final_hour * 60 + final_minutes

        if initial_time > final_time:
            self.initial_time = final_time
            self.final_time = initial_time
            self.initial_hour = final_hour
            self.initial_minutes = final_minutes
            self.final_hour = initial_hour
            self.final_minutes = final_minutes
        else:
            self.initial_time = initial_time
            self.final_time = final_time
            self.initial_hour = initial_hour
            self.initial_minutes = initial_minutes
            self.final_hour = final_hour
            self.final_minutes = final_minutes
        
        self.is_night = (self.final_time > 0 and self.initial_time < night_end)
        self.is_morning = (self.final_time > night_end and self.initial_time < morning_end)
        self.is_afternoon = (self.final_time > morning_end and self.initial_time < afternoon_end)
        self.is_evening = (self.final_time > afternoon_end and self.initial_time < evening_end)

    @property
    def initial_hour(self):
        return self.__initial_hour

    @initial_hour.setter
    def initial_hour(self, initial_hour):
        if not isinstance(initial_hour, int):
            raise TypeError("Initial hour must be an integer.")
        if not 0 <= initial_hour <= 23:
            raise ValueError("Initial hour must be between 0 and 23.")
        self.__initial_hour = initial_hour

    @property
    def initial_minutes(self):
        return self.__initial_minutes

    @initial_minutes.setter
    def initial_minutes(self, initial_minutes):
        if not isinstance(initial_minutes, int):
            raise TypeError("Initial minutes must be an integer.")
        if not 0 <= initial_minutes <= 59:
            raise ValueError("Initial minutes must be between 0 and 59.")
        self.__initial_minutes = initial_minutes

    @property
    def final_hour(self):
        return self.__final_hour

    @final_hour.setter
    def final_hour(self, final_hour):
        if not isinstance(final_hour, int):
            raise TypeError("Final hour must be an integer.")
        if not 0 <= final_hour <= 23:
            raise ValueError("Final hour must be between 0 and 23.")
        self.__final_hour = final_hour

    @property
    def final_minutes(self):
        return self.__final_minutes

    @final_minutes.setter
    def final_minutes(self, final_minutes):
        if not isinstance(final_minutes, int):
            raise TypeError("Final minutes must be an integer.")
        if not 0 <= final_minutes <= 59:
            raise ValueError("Final minutes must be between 0 and 59.")
        self.__final_minutes = final_minutes

    def __str__(self):
        time_range = f"\nTime range: [{self.initial_hour:02}:{self.initial_minutes:02} - {self.final_hour:02}:{self.final_minutes:02}]"

        day_parts = []
        if self.is_night:
            day_parts.append("night")
        if self.is_morning:
            day_parts.append("morning")
        if self.is_afternoon:
            day_parts.append("afternoon")
        if self.is_evening:
            day_parts.append("evening")

        parts_str = ""
        for i in range(len(day_parts)):
            parts_str += f"{day_parts[i]} "

        return f"{time_range} \n\nBelongs to: {parts_str}"

    @property
    def duration(self) -> int:
        return self.final_time - self.initial_time

    def __eq__(self, other):
        if not isinstance(other, TimeInterval):
            return False
        return (self.initial_time == other.initial_time and self.final_time == other.final_time)

intervals = []

num_intervals = int(input("How many time intervals do you want to add? "))
while num_intervals <= 0:
    num_intervals = int(input("How many time intervals do you want to add? "))

print(f"\nEnter {num_intervals} time intervals (not repeated).")

while len(intervals) < num_intervals:
    print(f"\nInterval {len(intervals) + 1} of {num_intervals}:")
    h1 = int(input("Initial hour (0-23): "))
    m1 = int(input("Initial minutes (0-59): "))
    h2 = int(input("Final hour (0-23): "))
    m2 = int(input("Final minutes (0-59): "))

    new_interval = TimeInterval(h1, m1, h2, m2)

    if new_interval in intervals:
        print("Error: This time interval already exists in the list. Please try again.")
    else:
        index = 0
        for each in intervals:
            if new_interval.duration <= each.duration:
                index += 1
        intervals.insert(index, new_interval)

for interval in intervals:
    print(interval)