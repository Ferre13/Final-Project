class Interval:
    """
    Time interval with start (hour, minute) and end (hour, minute).
    Also indicates whether it belongs to early morning (0-6), morning (6-12),
    afternoon (12-18), evening (18-24). An interval may belong to multiple.
    """

    def __init__(self, sh: int, sm: int, eh: int, em: int):
        # Set via properties (validation)
        self.start_hour = sh
        self.start_minute = sm
        self.end_hour = eh
        self.end_minute = em

        # Swap if start is after end
        if self.start_hour > self.end_hour:
            self.start_hour, self.end_hour = self.end_hour, self.start_hour
        elif self.start_hour == self.end_hour and self.start_minute > self.end_minute:
            self.start_minute, self.end_minute = self.end_minute, self.start_minute

    # -----------------------------
    # Properties with validation
    # -----------------------------
    @property
    def start_hour(self) -> int:
        return self._start_hour

    @start_hour.setter
    def start_hour(self, h: int):
        if isinstance(h, int) and 0 <= h <= 23:
            self._start_hour = h
        else:
            raise ValueError("Hour must be an integer between 0 and 23")

    @property
    def end_hour(self) -> int:
        return self._end_hour

    @end_hour.setter
    def end_hour(self, h: int):
        if isinstance(h, int) and 0 <= h <= 23:
            self._end_hour = h
        else:
            raise ValueError("Hour must be an integer between 0 and 23")

    @property
    def start_minute(self) -> int:
        return self._start_minute

    @start_minute.setter
    def start_minute(self, m: int):
        if isinstance(m, int) and 0 <= m < 60:
            self._start_minute = m
        else:
            raise ValueError("Minutes must be an integer between 0 and 59")

    @property
    def end_minute(self) -> int:
        return self._end_minute

    @end_minute.setter
    def end_minute(self, m: int):
        if isinstance(m, int) and 0 <= m < 60:
            self._end_minute = m
        else:
            raise ValueError("Minutes must be an integer between 0 and 59")

    # -----------------------------
    # Read-only computed properties
    # -----------------------------
    @property
    def belongs_to(self):
        """
        Returns a tuple with the parts of the day this interval belongs to.
        """
        parts = ("early morning", "morning", "afternoon", "evening")
        start_part = self.start_hour // 6
        end_part = self.end_hour // 6
        return parts[start_part : end_part + 1]

    @property
    def duration(self) -> int:
        """Duration in minutes."""
        start_total = self.start_hour * 60 + self.start_minute
        end_total = self.end_hour * 60 + self.end_minute
        return end_total - start_total

    # -----------------------------
    # Helpers
    # -----------------------------
    def _pad2(self, v: int) -> str:
        return f"{v:02d}"

    # -----------------------------
    # Dunder methods
    # -----------------------------
    def __str__(self) -> str:
        sh = self._pad2(self.start_hour)
        sm = self._pad2(self.start_minute)
        eh = self._pad2(self.end_hour)
        em = self._pad2(self.end_minute)
        header = f"Time range: [{sh}:{sm}-{eh}:{em}]"
        belongs = "Belongs to:" + "".join(f" {p}" for p in self.belongs_to)
        return header + "\n" + belongs

    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return False
        return (
            self.start_hour == other.start_hour
            and self.start_minute == other.start_minute
            and self.end_hour == other.end_hour
            and self.end_minute == other.end_minute
        )

    def __lt__(self, other) -> bool:
        if not isinstance(other, Interval):
            raise TypeError("Can only compare with another Interval")
        return self.duration < other.duration
