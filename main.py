import pandas as pd

df = pd.read_csv("./hotels.csv", dtype={"id":str})
df_card = pd.read_csv("./cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("./card_security.csv", dtype=str)


class Hotel:
	def __init__(self, hotel_id):
		self.hotel_id = hotel_id
		self.name = df.loc[df["id"]== self.hotel_id, "name"].squeeze()
	
	def book(self):
		"""Book a hotel by changing its availability to no."""
		df.loc[df["id"]==self.hotel_id, "available"] = "no"
		df.to_csv("./hotels.csv", index=False)


	def available(self):
		"""Check if the hotel is available."""
		available = df.loc[df["id"]==self.hotel_id, "available"].squeeze()
		if available == "yes":
			return True
		else:
			return False

class SpaHotel(Hotel):
	def book_spa_package(self):
		pass

class ReservationTicket:
	def __init__(self, customer_name, hotel_object):
		self.customer_name = customer_name
		self.hotel = hotel_object
	
	def generate(self):
		content = f"""
		Thank you for your reservation.
		Here are your bookin date:
		Name : {self.customer_name}
		Hotel Name : {self.hotel.name}
		"""
		return content


class CreditCard:
	def __init__(self, number):
		self.number = number

	def validate(self, expiration, holder, cvc):
		card_data = {"number": self.number, "expiration": expiration,
					 "holder": holder, "cvc": cvc}
		if card_data in df_card:
			return True
		else:
			return False


class SecureCreditCard(CreditCard):
	def authentication(self, given_password):
		password = df_cards_security.loc[df_cards_security["number"]==self.number, "password"]
		
		if password.empty:
			print("No matching card found.")
			return False

		password = password.squeeze()
		if pd.isna(password):
			print("Password not found.")
			return False
		if password == given_password:
			return True
		else:
			return False


class SpaTicket:
	def __init__(self, customer_name, hotel_object):
		self.customer_name = customer_name
		self.hotel = hotel_object

	def generate(self):
		content = f"""
		Thank you for your reservation.
		Here are your SPA booking date:
		Name : {self.customer_name}
		Hotel Name : {self.hotel.name}
		"""
		return content

		
print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
	# card_number = input("Enter your credit card numbers :")
	# expiration_date = input("Enter your credi	t card expiration date: ")
	credit_card = SecureCreditCard(number="1234567812341234")
	if credit_card.validate(expiration="12/26",
							holder="Andrew Lee",
							cvc="123"):
		if credit_card.authentication(given_password="mypass"):
			hotel.book()
			name = input("Enter your name: ")
			reservation_ticket = ReservationTicket(customer_name=name,
											 	   hotel_object=hotel)
			print(reservation_ticket.generate())
			spa_reservation = input("Do you want to book SPA? :")
			
			if spa_reservation == "yes":
				hotel.book_spa_package()
				spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
				print(spa_ticket.generate())
		else:
			print("Credit Card Authentication failed.")
	else:
		print("Your credit card has problems.")

else:
	print("Hotel is not available.")

