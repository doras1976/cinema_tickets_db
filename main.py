import os
import platform
import random
import string
import sqlite3
from fpdf import FPDF


class User:
    """Represents a user that can buy a cinema seat"""

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buys the ticket if the seat is free and the card is valid """
        if seat.is_free():
            if card.validate_balance_deduct_ticket_price(price=seat.get_price()):
                # occupy the seat
                seat.occupy()
                # create the ticket, turn it to pdf and pop it up on the screen
                ticket = Ticket(user=self, price=seat.get_price(), seat_number=seat.seat_id)
                ticket.to_pdf()
                return "Purchase successful"
            else:
                return "There was a problem with your card"
        else:
            return "Seat is taken"


class Seat:

    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute("""
               SELECT "price" FROM "Seat"
               WHERE "seat_id"=?
               """, [self.seat_id])
        results = cursor.fetchall()[0][0]
        connection.close()
        return results

    def is_free(self):
        """find out if the seat is taken"""
        db_connection = sqlite3.connect(self.database)
        cursor = db_connection.cursor()
        cursor.execute("""SELECT "taken" FROM Seat WHERE seat_id = ?""", [self.seat_id])
        taken = cursor.fetchall()[0][0]
        db_connection.close()
        if taken == 1:
            return False  # seat is not free
        else:
            return True  # seat is free

    def occupy(self):
        """Occupy the seat"""
        db_connection = sqlite3.connect(self.database)
        db_connection.execute("""
                            UPDATE "Seat" SET "taken"=? WHERE "seat_id"=?
                            """, [1, self.seat_id])
        db_connection.commit()
        db_connection.close()


class Card:

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.holder = holder
        self.type = type
        self.number = number
        self. cvc = cvc

    def validate_balance_deduct_ticket_price(self, price):
        """Checks if card has enough balance and deduct ticket price"""
        # Check that card has enough balance
        db_connection = sqlite3.connect(self.database)
        cursor = db_connection.cursor()
        cursor.execute("""SELECT "balance" FROM Card 
                          WHERE "number" = ? and "cvc" = ?""", [self.number, self.cvc])
        balance = cursor.fetchall()[0][0]
        if balance >= price:
            # deduct price from balance
            db_connection.execute("""
                    UPDATE "Card" SET "balance"=? WHERE "number"=? and "cvc"=?
                    """, [balance-price, self.number, self.cvc])
            db_connection.commit()
            db_connection.close()
            return True


class Ticket:

    def __init__(self, user, price, seat_number):
        self.user = user
        self.price = price
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.seat_number = seat_number

    def to_pdf(self):
        # Define the filename for the ticket PDF
        filename = f"ticket_{self.id}.pdf"

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Set title
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "Cinema Ticket", ln=True, align='C')

        # Add user details, seat number, ticket ID, and price
        pdf.set_font("Arial", size=14)
        pdf.ln(10)
        pdf.cell(0, 10, f"Name: {self.user.name}", ln=True)
        pdf.cell(0, 10, f"Seat Number: {self.seat_number}", ln=True)
        pdf.cell(0, 10, f"Ticket ID: {self.id}", ln=True)
        pdf.cell(0, 10, f"Price: ${self.price:.2f}", ln=True)

        # Output the PDF to a file
        pdf.output(filename)

        print(f"Ticket saved as {filename}")

        # Open the PDF to pop up on the screen
        if platform.system() == "Windows":
            os.system(f"start {filename}")
        elif platform.system() == "Darwin":
            os.system(f"open {filename}")
        else:
            os.system(f"xdg-open {filename}")


if __name__ == "__main__":

    # name = input("Your full name: ")
    # seat_id = input("Preferred seat number: ")
    # card_type = input("Your card type: ")
    # card_number = input("Your card number: ")
    # card_cvc = input("Your card cvc: ")
    # card_holder = input("Card holder name: ")
    #
    # user = User(name=name)
    # seat = Seat(seat_id=seat_id)
    # card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    user = User(name="dora")
    seat = Seat(seat_id="A1")
    card = Card(type="Visa", number="12345678", cvc="123", holder="John Smith")

    print(user.buy(seat=seat, card=card))