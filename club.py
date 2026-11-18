"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event
from collections import Counter

class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if capacity < 1 or title in self.events:
            raise ValueError(f"capacity must be at least 1, got {capacity}")
        event = Event(title, capacity)
        self.events[title] = event
        return event

    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        try:
            event = self.events[title]
        except KeyError:
            raise UnknownEventError(title)

        return event

    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        error = f"Sorry, I don't understand {line!r}."
        try:
            command, event, name = [i.strip() for i in line.split(",")]
        except:
            return error
        command = command.lower()

        try:
            event = self.events[event]
            if command == "join":
                msg = event.sign_up(name)
            elif command == "leave":
                msg = event.cancel(name)
            else:
                return error

            if msg == "seat": 
                return f"{name} has a seat at {event.title}."
            elif msg == "waitlist":
                return f"{name} is on the waitlist for {event.title}."
            else:
                return f"{name} left {event.title}." + (f" {msg} gets the seat." if not(msg is None) else "")

        except SignupError:
            return f"Sorry, {name} is already signed up for {event.title}."

    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        name_counter = Counter([member for event in self.events.values() for member in event.seats])
        return dict(name_counter)

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
