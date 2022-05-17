from datetime import datetime
import time

class Shows:
    def __init__(self, name: str, date: datetime, genre: str, duration: int, description: str, time: time) -> None:
        self.name = name
        self.genre = genre
        self.duration = duration
        self.date = date
        self.description = description
        self.time = time