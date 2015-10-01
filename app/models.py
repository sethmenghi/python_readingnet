from app import db


class Person(db.Model):
	"""Person, who is a donor or volunteer."""
	__tablename__ = 'persons'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	birth_date = db.Column(db.Date(), nullable=False)
	gender = db.Column(db.String(6), nullable=False)
	phone = db.Column(db.String(15), nullable=False)
	email = db.Column(db.String(250), nullable=False, unique=True)
	street_name = db.Column(db.String(250), nullable=False)
	city = db.Column(db.String(250), nullable=False)
	state = db.Column(db.String(2), nullable=False)
	zip_code = db.Column(db.String(10), nullable=False)
	volunteer = db.relationship('Volunteer', backref='person')
	donor = db.relationship('Donor', backref='person')

	def __init__(self, first, last, birth, gender, phone, email, 
				 street, city, state, zip_code):
		self.first_name = first
		self.last_name = last
		self.birth_date = birth
		self.gender = gender
		self.phone = phone
		self.email = email
		self.street_name = street
		self.city = city
		self.state = state
		self.zip_code = zip_code

	def __repr__(self):
		return '<Person[%d]: %s %s>' % (self.first_name, self.last_name)
		
	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		from forgery_py import name, date, internet, address, personal
		
		seed()
		for i in range(count):
			p = Person(name.first_name(), name.last_name(), date.date(),
					   personal.gender(), address.phone(), internet.email_address(),
					   address.street_address(), address.city(), 
					   address.state_abbrev(), address.zip_code())
			db.session.add(p)

			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


class Volunteer(db.Model):
	"""Volunteers add additional volunteers and query.""" #and purchase other books using cash
	__tablename__ = 'volunteers'
	id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)
	purchases = db.relationship('VolunteerPurchases', backref='volunteer')

	@staticmethod
	def generate_fake():
		from random import seed
		from sqlalchemy.exc import IntegrityError

		seed()
		user_count = Person.query.count() - 1
		for i in range(1,user_count):
			if (i % 4) == 0:
				person = Person.query.get(i)
				v = Volunteer(id=person.id)
				db.session.add(v)
				try:
					db.session.commit()
				except IntegrityError as e:
					print(e)
					db.session.rollback()


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)


class Donor(db.Model):
	__tablename__ = 'donors'
	id = db.Column(db.Integer, db.ForeignKey('persons.id'), primary_key=True)

	@staticmethod
	def generate_fake():
		from random import seed
		from sqlalchemy.exc import IntegrityError

		seed()
		user_count = Person.query.count() - 1
		for i in range(1,user_count):
			if (i % 3) == 0:
				person = Person.query.get(i)
				d = Donor(id=person.id)
				db.session.add(d)
				try:
					db.session.commit()
				except IntegrityError:
					db.session.rollback()


class BookDonation(db.Model):
	"""For each donor's donation need:
		book, information, quantity of books, date of donation, 
		if book w/ same status + condition, update quantity of that book
	"""
	__tablename__ = 'book_donations'
	id = db.Column(db.Integer, primary_key=True) #unique id given to each individual donation.
	isbn = db.Column(db.Integer, nullable = False) #not foreign key so when books removed from inventory donations aren't lost
	donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
	date = db.Column(db.Date, nullable=False)
	quantity = db.Column(db.Integer, nullable = False)
	condition = db.Column(db.String(250), nullable = False) #I think this also needs to be in primary key


class CashDonation(db.Model):
	"The amount donated, donation date, and donor are maintained."
	__tablename__ = 'cash_donations'
	id = db.Column(db.Integer, primary_key=True)
	donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
	date = db.Column(db.Date, nullable=False)
	cash = db.Column(db.Integer, nullable=False)


class ReadingLevels(db.Model):
	__tablename__ = 'reading_levels'
	reading_level = db.Column(db.String(250), primary_key=True)
	clients = db.relationship('Client', backref='reading_level')


class Client(db.Model):
	__tablename__ = 'clients'
	id = db.Column(db.Integer, primary_key=True)
	client_name = db.Column(db.String(250), nullable=False)
	phone = db.Column(db.String(15), nullable=False)
	email = db.Column(db.String(250), nullable=False, unique=True)
	street_name = db.Column(db.String(250), nullable=False)
	city = db.Column(db.String(250), nullable=False)
	state = db.Column(db.String(2), nullable=False)
	zip_code = db.Column(db.String(10), nullable=False)
	contact_name = db.Column(db.String(250))
	tokens = db.Column(db.Integer, default=20)
	completed_purchases = db.relationship('ClientPurchases', backref='client')
	held_purchases = db.relationship('ClientPurchasesHeld', backref='client')
	r_level = db.Column(db.String(250), db.ForeignKey('reading_levels.reading_level'), nullable=False)

	def __init__(self, client, phone, email, street, 
				 city, state, zip_code, level, contact=None):
		self.client_name = client
		self.phone = phone
		self.email = email
		self.street_name = street
		self.city = city
		self.state = state
		self.r_level = level
		self.zip_code = zip_code
		self.r_level = level # Didn't add this before submission
		if contact:
			self.contact_name = contact

	def __repr__(self):
		return '<Client Name %r>' % (self.client_name)

	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed, randint
		from forgery_py import name, internet, address
		
		seed()
		reading_levels = ['Teen', 'Adult', 'Children']
		for i in range(count):
			current_reading_level = reading_levels[randint(0,2)]
			rl = ReadingLevels.query.filter(ReadingLevels.reading_level == current_reading_level).first()
			c = Client(name.full_name(), address.phone(), 
					   internet.email_address(), 
					   address.street_address(), address.city(), 
					   address.state_abbrev(), 
					   address.zip_code(), current_reading_level, name.last_name())

			rl.clients.append(c)

			try:
				db.session.add(c)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


class BookGenre(db.Model):
	__tablename__ = 'book_genre'
	genre = db.Column(db.String(250), primary_key=True)
	genre_description = db.Column(db.String(250), nullable=False)


# Many-Many relationship between BookDetails and the authors
# An author may have many books, and a book may have many authors
# See: http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-many
authors_books = db.Table('authors_books', db.Model.metadata,
	db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
	db.Column('isbn', db.String(13), db.ForeignKey('book_details.isbn'))
)


class Author(db.Model):
	__tablename__ = 'authors'
	id = db.Column(db.Integer, primary_key=True)
	first = db.Column(db.String(250), nullable=False)
	last = db.Column(db.String(250), nullable=False)

	def __repr__(self):
		return '%s %s' % (self.first, self.last)

	@staticmethod
	def generate_fake(count=75):
		from random import seed
		from forgery_py import name
		from sqlalchemy.exc import IntegrityError

		seed()
		for i in range(count):
			a = Author(first=name.first_name(), last=name.last_name())
			db.session.add(a)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

class BookDetails(db.Model):
	__tablename__ = 'book_details'
	isbn = db.Column(db.String(13), primary_key=True)
	title = db.Column(db.String(250), nullable=False)
	# edition = db.Column(db.String(50), nullable=False)
	reading_level = db.Column(db.String(250), nullable=False)
	publisher = db.Column(db.String(250), nullable=False)
	# condition = db.Column(db.String(250), nullable = False)
	# genre = db.relationship('Genre', backref='books') do we need this?
	genre = db.Column(db.String(250), db.ForeignKey('book_genre.genre'))
	inventory = db.relationship('BookInventory', backref='books', lazy='dynamic')
	authors = db.relationship('Author', secondary=authors_books, 
							  backref=db.backref('books', lazy='dynamic'), 
							  lazy='dynamic')

	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		from forgery_py import lorem_ipsum, name
		from sqlalchemy.exc import IntegrityError

		seed()
		author_count = Author.query.count()
		reading_levels = ['Teen', 'Children', 'Adult']
		genres = ['Comic', 'Autobiography', 'Biography', 'Crime/Detective', 
				  'Fantasy', 'Historical Fiction', 'Magical Realism', 'Mystery', 
				  'Mythopoeia', 'Poetry', 'Realistic Fiction', 'Scientific Fiction', 
				  'Short Story', 'Textbook', 'Thriller', 'Western']

		for i in range(count):
			#needs to be 13 length
			isbn = str(randint(10000, 99999)) + str(randint(10000, 99999)) + str(randint(100, 999))
			bk = BookDetails(isbn=isbn, title=lorem_ipsum.title(), reading_level=reading_levels[randint(0,2)],
				publisher=name.company_name(), genre=genres[randint(0,len(genres)-1)])
			if author_count > 0:
				a1 = Author.query.offset(randint(0, author_count - 1)).first()
				a2 = Author.query.offset(randint(0, author_count - 1)).first()
				while(a1 == a2):
					a2 = Author.query.offset(randint(0, author_count - 1)).first()
				bk.authors.append(a1)
				bk.authors.append(a2)
			try:
				db.session.add(bk)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


class BookInventory(db.Model):
	"""List of used/new books in inventory."""
	__tablename__ = 'book_inventory'
	isbn = db.Column(db.String(13), db.ForeignKey('book_details.isbn'), primary_key=True)
	condition = db.Column(db.String(250), primary_key=True) #I think this also needs to be in primary key
	edition = db.Column(db.String(250), primary_key=True)
	quantity = db.Column(db.Integer, nullable=False)

	@staticmethod
	def generate_fake(count=25):
		from random import seed, randint
		from sqlalchemy.exc import IntegrityError

		seed()
		conditions = ['New', 'Used']
		for i in BookDetails.query.all():
			bk = i
			inventory1 = BookInventory(isbn=bk.isbn, condition=conditions[randint(0,1)],
									  edition=randint(1,9), quantity=randint(1,6))
			inventory2 = BookInventory(isbn=bk.isbn, condition=conditions[randint(0,1)],
										  edition=randint(1,9), quantity=randint(1,20))
			while(inventory2.edition == inventory1.edition):
				inventory2 = BookInventory(isbn=bk.isbn, condition=conditions[randint(0,1)],
										  edition=randint(1,9), quantity=randint(1,20))
			db.session.add(inventory1)
			db.session.add(inventory2)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


class CashInventory(db.Model):
	"""Updated as cash donations and purchases are made"""
	__tablename__ = 'cash_inventory'
	funds = db.Column(db.Integer, primary_key = True)


##################################################################
#### different types of purchases ####
class VolunteerPurchases(db.Model):
	#what if volunteer makes more than one purchase a day of the same books?
	"""contains historical info of purchases made by volunteers"""
	__tablename__ = 'volunteer_purchases'
	#name/username of purchaser? Should this be referencing persons.id? unique?
	purchase_id = db.Column(db.Integer, primary_key = True)
	volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'))
	date = db.Column(db.DateTime, primary_key = True)	#combined key?
	isbn = db.Column(db.String(13), db.ForeignKey('book_details.isbn'))
	condition = db.Column(db.String(250), nullable = False)
	edition = db.Column(db.String(250), nullable = False)
	cost = db.Column(db.Integer, default=0)


class ClientPurchases(db.Model):
	#note same problems as volunteer purchases
	"""contains historical info of client purchases. for selling advertisements rights"""
	#should this be referencing persons.id?
	id = db.Column(db.Integer, primary_key = True)
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
	date = db.Column(db.DateTime, nullable = False)	#combined key?
	isbn = db.Column(db.String(13), db.ForeignKey('book_details.isbn'))
	condition = db.Column(db.String(250), nullable = False)
	edition = db.Column(db.String(250), nullable = False)
	quantity = db.Column(db.Integer, nullable = False)


class ClientPurchasesHeld(db.Model):
	#note same problems as above
	"""if client attempts to purchase book not at reading level (high or low?)"""
	id = db.Column(db.Integer, primary_key = True)	
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id')) #lets us pipe to client reading level
	date = db.Column(db.DateTime, primary_key = True)	#combined key?
	isbn = db.Column(db.String(13), db.ForeignKey('book_details.isbn'))	#lets us pipe to book reading level
	condition = db.Column(db.String(250), nullable = False)
	edition = db.Column(db.String(250), nullable = False)
	quantity = db.Column(db.Integer, nullable = False)







