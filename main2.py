import pandas as pd
from abc import ABC, abstractmethod

# Load hotel data from CSV
df = pd.read_csv("hotels.csv", dtype={"id": str})


class Hotel:
    """
    Represents a hotel entity with booking and availability logic.
    """
    watermark = "The Real Estate Company"

    def __init__(self, hotel_id):
        """Initialize a Hotel object using its ID."""
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book the hotel by updating its availability status in the dataset."""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is currently available."""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"

    @classmethod
    def get_hotel_count(cls, data):
        """Get the total number of hotels in the dataset."""
        return len(data)

    def __eq__(self, other):
        """Check if two Hotel instances represent the same hotel."""
        return self.hotel_id == other.hotel_id


class Ticket(ABC):
    """Abstract base class representing a generic ticket."""

    @abstractmethod
    def generate(self):
        pass


class ReservationTicket(Ticket):
    """
    A ticket generated for hotel reservations.
    """

    def __init__(self, customer_name, hotel_object):
        """Initialize a ReservationTicket."""
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        """Generate the reservation ticket content."""
        content = f"""
        Thank you for your reservation!
        Your booking details:
        Name: {self.the_customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

    @property
    def the_customer_name(self):
        """Return a cleaned and formatted version of the customer's name."""
        name = self.customer_name.strip().title()
        return name

    @staticmethod
    def convert(amount):
        """Convert an amount to a new currency (example multiplier: 1.2)."""
        return amount * 1.2


class DigitalTicket(Ticket):
    """A digital version of a ticket."""

    def generate(self):
        """Generate the digital ticket content."""
        return "Howdy! This is your digital ticket"
