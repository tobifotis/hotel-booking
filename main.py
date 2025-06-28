import pandas as pd

# Load data from CSV files
df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    """
    Represents a hotel with booking and availability functionality.
    """

    def __init__(self, hotel_id):
        """Initialize the Hotel with its ID and retrieve its name."""
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book the hotel by setting its availability to 'no'."""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is currently available."""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"


class Ticket:
    """
    Represents a booking ticket for a hotel reservation.
    """

    def __init__(self, customer_name, hotel_object):
        """Initialize the ticket with customer name and hotel."""
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        """Generate and return the ticket content."""
        content = f"""
        Thank you for your reservation!
        Your booking details:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    """
    Represents a basic credit card with validation capability.
    """

    def __init__(self, number):
        """Initialize the credit card with a number."""
        self.number = number

    def validate(self, expiration, holder, cvc):
        """Validate the card details against the records."""
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}
        return card_data in df_cards


class SecureCreditCard(CreditCard):
    """
    Extends CreditCard with an authentication method using a password.
    """

    def authenticate(self, given_password):
        """Authenticate the card using the stored password."""
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        return password == given_password


# --- Program flow ---

print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234")

    if credit_card.validate(expiration="12/26", holder="JOHN DOE", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()

            name = input("Enter your name: ")
            ticket = Ticket(customer_name=name, hotel_object=hotel)
            print(ticket.generate())
        else:
            print("Credit card authentication failed.")
    else:
        print("There was an issue validating your credit card.")
else:
    print("Hotel is currently closed.")
