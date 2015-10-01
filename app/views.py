from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import DonateCash, LoginForm, CreatePerson, CreateClient, CreateBook, RemovePerson, RemoveClient, RemoveBook, ClientPurchaseBook, BookSearchByTitle, AddTokens
from .models import ClientPurchasesHeld, CashDonation, Volunteer, Donor, Person, Client, BookInventory, CashInventory, VolunteerPurchases, ClientPurchases, BookDetails, BookDonation, Author, BookGenre
import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
	return Volunteer.query.get(int(user_id))



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Person.query.filter_by(email=form.email.data).first()
		if user is not None:
			user = Volunteer.query.get(user.id)
			if user is not None: #and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				flash("Logged in successfully.")
				return redirect(request.args.get('next') or url_for('index'))
			# login and validate the user...
			# 	person = Person.query.filter(Person.email == form.email.data).first()
			# volunteer = Volunteer.query.get(person.id)
	flash('Invalid email or password.')
	return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/view_books", methods=['GET', 'POST'])
def view_books():
	books = BookDetails.query.order_by(BookDetails.title).all()
	quantities = []
	for book in books:
		inventoried_books = BookInventory.query.filter(BookInventory.isbn == book.isbn).all()
		sum_quantities = 0
		for b in inventoried_books:
			sum_quantities += b.quantity
		quantities.append(sum_quantities)
	return render_template('books.html', books=zip(books,quantities))


@app.route("/view_persons", methods=['GET', 'POST'])
@login_required
def view_persons():
	persons = Person.query.order_by(Person.last_name).all()
	volunteers = Volunteer.query.order_by(Volunteer.id).all()
	donors = Donor.query.order_by(Donor.id).all()
	clients = Client.query.order_by(Client.id).all()
	return render_template('persons.html', persons=persons, 
							volunteers=volunteers, 
							donors=donors, clients=clients)


@app.route("/view_genres", methods=['GET','POST'])
def view_genres():
	genres = BookGenre.query.order_by(BookGenre.genre).all()
	return render_template('genre.html', genres=genres)


@app.route('/search_by_title', methods=['GET','POST'])
@login_required
def search_by_title():
	form = BookSearchByTitle()
	if request.method == 'POST' and form.validate():
		
		title_to_search = form.title.data.title()
		title_to_search = "%" + title_to_search + "%"
		books = BookDetails.query.filter(BookDetails.title.like(title_to_search)).all()

		quantities = []
		for book in books:
			quantity = int(db.session.query(func.sum(BookInventory.quantity)).filter(BookInventory.isbn == book.isbn)[0][0])
			quantities.append(quantity)
		return render_template('books.html', books=zip(books,quantities))
	return render_template('search.html', form=form)


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
	"""Creates a form to add a person to the database."""
	form = CreatePerson()
	if request.method == 'POST' and form.validate():
		new_person = Person(form.first.data.title(), form.last.data.title(),  
							form.birth.data, form.gender.data.title(),
							form.phone.data.title(), form.email.data, 
							form.street_name.data.title(),form.city.data.title(), 
							form.state.data.upper(), form.zip_code.data)
		db.session.add(new_person)
		if form.volunteer.data:
			volunteer = Volunteer()
			volunteer.person_id = new_person.id
			volunteer.person = new_person
			db.session.add(volunteer)
		if form.donor.data:
			donor = Donor()
			donor.person_id = new_person.id
			donor.person = new_person
			db.session.add(donor)
		db.session.commit()
		flash("Added id(%d): %s %s" % (new_person.id, 
									   new_person.first_name, 
									   new_person.last_name))
		return redirect(request.args.get("next") or url_for("add_person"))
	return render_template('add.html', form=form)


@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
	"""Creates a form to add a person to the database."""
	form = CreateClient()
	if request.method == 'POST' and form.validate():
		client = Client(form.name.data.title(), form.phone.data, 
							form.email.data, form.street_name.data.title(),
							form.city.data.title(), form.state.data.upper().title(), 
							form.zip_code.data, form.reading_level.data.title(), # added after submission before demo -> added table before submission forgot to add
							form.contact.data.title(),
							)
		db.session.add(client)
		db.session.commit()
		flash("Added id(%d): %s" % (client.id, 
									   client.client_name))
		return redirect(url_for('add_client'))
	return render_template('add.html', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
@app.route('/volunteer_purchase_book', methods=['GET', 'POST'])
@login_required
def add_book():
	"""Creates a form to add a book to the database."""
	form = CreateBook()
	funds = CashInventory.query.first().funds
	if request.method == 'POST' and form.validate():
		if form.cost.data > 0 and form.cost.data > CashInventory.query.first().funds:
			flash ("Error: we don't have enough funds for that!")
			return redirect(url_for('add_book'))
		author_objects = []
		# Get the split objects 
		authors = form.authors.data
		authors = authors.splitlines()
		for author in authors:
			author = author.split()	
			if len(author) % 2 > 0:
				flash ("Error: incorrect format in authors field!")
				return redirect(url_for('add_book'))
			first = author[0]
			last = author[1]
			# Get name of author in database
			auth = Author.query.filter(Author.first==first, Author.last==last).first()
			if not auth:
				# Create a new author if not already in database
				auth = Author()
				auth.first = first
				auth.last = last
				db.session.add(auth)
			author_objects.append(auth)
		# Book does not exist + create new book + create its inventory
		book = BookDetails.query.filter(BookDetails.isbn == form.isbn.data).first()
		if not book:
			book = BookDetails(isbn=form.isbn.data, 
							   title=form.title.data.title(), 
			 				   reading_level=form.reading_level.data.title(), 
			 				   publisher=form.publisher.data.title(), 
			 				   genre=form.genre.data)
			# Add authors to Book (M-M)
			for author in author_objects:
				book.authors.append(author)

			inventory = BookInventory(isbn=book.isbn, 
									  edition=form.edition.data, 
									  condition=form.condition.data, 
									  quantity=1)
			db.session.add(book)
			db.session.add(inventory)
		# Book is already in inventory	
		else:
			inventory = BookInventory.query.filter(book.isbn == BookInventory.isbn, 
										  		   form.edition.data == BookInventory.edition, 
										  		   form.condition.data == BookInventory.condition).first()
			if inventory:
				inventory.quantity = inventory.quantity + 1
			# Inventory doesn't exist
			else: 
				inventory = BookInventory(isbn=book.isbn, 
									 	  edition=form.edition.data, 
									 	  condition=form.condition.data, 
									 	  quantity=1)
				inventory.books = book
				flash("Added book(%s): %s" % (book.isbn, book.title))

				db.session.add(inventory)
		# Check funds
		book_cost = form.cost.data
		cash_inventory = CashInventory.query.first()
		final_funds = cash_inventory.funds - book_cost
		if (final_funds >= 0):
			date = datetime.datetime.now()
			donation = BookDonation(isbn=book.isbn, donor_id=form.donor_id.data,
									date=date, quantity=1, condition=form.condition.data)
			cash_inventory.funds = final_funds
			# Create the Volunteer Purchase
			purchase = VolunteerPurchases(volunteer_id=current_user.get_id(),
										  date=date,
										  isbn=book.isbn,
										  condition=form.condition.data,
										  edition=form.edition.data,
										  cost=book_cost)
			db.session.add(purchase)
			db.session.add(donation)


		else:
			flash("Insufficient money for donation")
			db.session.rollback()
		db.session.commit()
		return redirect(url_for('add_book'))
	return render_template('volunteer_purchase.html', form=form, funds=funds)


@app.route('/remove_person', methods=['GET', 'POST'])
@login_required
def remove_person():
	"""Creates a form to remove a person from the database."""
	form = RemovePerson()
	if request.method == 'POST' and form.validate():
		if form.email.data:
			person = Person.query.filter(Person.email == form.email.data).first()
			form.person_id.data = person.id
			# Get person from database via OBJECT.query.get
		volunteer = Volunteer.query.get(form.person_id.data)
		donor = Donor.query.get(form.person_id.data)
		if volunteer:
			db.session.delete(volunteer)
		if donor:
			db.session.delete(donor)
		removed_person = Person.query.get(form.person_id.data)
		db.session.delete(removed_person)
		db.session.commit()
		flash("Deleted id(%d): %s %s" % (form.person_id.data, 
										 removed_person.first_name, 
										 removed_person.last_name))
		return redirect(url_for('remove_person'))			
	return render_template('remove.html', form=form)


@app.route('/remove_client', methods=['GET', 'POST'])
@login_required
def remove_client():
	"""Creates a form to remove a person from the database."""
	form = RemoveClient()
	if request.method == 'POST' and form.validate():
		# Get person from database via OBJECT.query.get
		client = Client.query.get(form.client_id.data)
		db.session.delete(client)
		flash("Deleted id(%d): %s" % (form.client_id.data, 
										 client.client_name))
		db.session.commit()

		return redirect(url_for('remove_client'))
	return render_template('remove.html', form=form)


@app.route('/remove_book', methods=['GET', 'POST'])
@login_required
def remove_book():
	form = RemoveBook()
	if request.method == 'POST' and form.validate():
		# find correct book
		book = BookInventory.query.filter(BookInventory.isbn == form.isbn.data, 
										BookInventory.condition == form.condition.data,
										BookInventory.edition == form.edition.data).first()
		if book.quantity - form.quantity.data < 0:
			flash ("Error: not enough books to for that order!")
			return render_template('remove.html', form=form)
		elif book.quantity - form.quantity.data == 0:
			flash("Book(s) successfully removed! It was the last one!")
			db.session.delete(book)
			db.session.commit()
		else:
			book.quantity = book.quantity - form.quantity.data
			flash ("Book(s) removed.")
		return redirect(url_for('remove_book'))
	return render_template('remove.html', form=form)


@app.route('/client_purchase_book', methods=['GET','POST'])
@login_required #and they have to be a client...
def client_purchase_book():
	form = ClientPurchaseBook()
	if request.method == 'POST' and form.validate():

		cost = form.quantity.data
		#if book is new, multiply queryantity by 3
		if form.condition.data == "New":
			cost = cost * 3

		client = Client.query.filter(Client.id == form.client_id.data).first()
		if cost > client.tokens:
			flash ("Error: not enough tokens to purchase these books!")
			return render_template("remove.html", form=form) 
		else:
					# find correct book
			book = BookInventory.query.filter(BookInventory.isbn == form.isbn.data, 
										BookInventory.condition == form.condition.data,
										BookInventory.edition == form.edition.data).first()
			
			client = Client.query.filter(Client.id == form.client_id.data).first()
			if client.r_level != book.books.reading_level:
				held = ClientPurchasesHeld(client_id=form.client_id.data, date=datetime.datetime.now(),
											isbn=form.isbn.data, condition=form.condition.data,
											edition=form.edition.data, quantity=form.quantity.data)
				db.session.add(held)
				db.session.commit()
			else:	
				purchase = ClientPurchases(client_id=form.client_id.data,
											isbn=form.isbn.data, 
											date=datetime.datetime.now(),
											condition=form.condition.data,
											edition=form.edition.data, 
											quantity=form.quantity.data) 
				if book.quantity - form.quantity.data < 0:
					flash ("Error: not enough books to for that order!")
					return render_template('remove.html', form=form)
				elif book.quantity - form.quantity.data == 0:
					flash("Book(s) successfully purchased! You got the last one!")
					current_isbn = book.isbn
					count = BookInventory.query.filter(BookInventory.isbn == book.isbn).count() - 1
					db.session.delete(book)
					#if count <= 0:
						#details = BookDetails.query.filter(BookDetails.isbn == current_isbn).first()
						#if details:
							#db.session.delete(details)
					db.session.add(purchase)
					client.tokens = client.tokens - cost
					db.session.commit()
				else:
					book.quantity = book.quantity - form.quantity.data
					db.session.add(purchase)
					client.tokens = client.tokens - cost
					db.session.commit()
					flash ("Book(s) successfully purchased. There are %d left" % book.quantity)
				return redirect(url_for('client_purchase_book'))
	return render_template("client_purchase.html", form=form, inventory=BookInventory.query.all()) 


@app.route('/add_tokens', methods=["GET","POST"])
@login_required
def add_tokens():
	form = AddTokens()
	if request.method == 'POST' and form.validate():
		client_id = form.client_id.data
		tokens = form.tokens_to_add.data
		client = Client.query.filter(client_id==Client.id).first()
		client.tokens = client.tokens + tokens
		db.session.commit()
		flash("Tokens to add %d final tokens %d" % (tokens, client.tokens)) 

		return redirect(url_for('add_tokens'))
	return render_template("add.html", form=form)	


@app.route('/add_cash', methods=["GET","POST"])
@login_required
def add_cash():
	form = DonateCash()
	if request.method == 'POST' and form.validate():
		donation = CashDonation(donor_id=form.donor_id.data, 
								date=datetime.datetime.now(), 
								cash=form.amount.data)
		funds = CashInventory.query.first()
		funds.funds = funds.funds + form.amount.data
		db.session.add(donation)
		db.session.commit()

		return redirect(url_for('add_cash'))
	return render_template('add.html', form=form)


@app.route('/view_donations', methods=["GET","POST"])
@login_required
def view_donations():
	cash_donations = CashDonation.query.order_by(CashDonation.id).all()
	book_donations = BookDonation.query.order_by(BookDonation.id).all()
	
	return render_template('donation.html', cash_donations=cash_donations, 
							book_donations=book_donations)


@app.route('/view_purchases', methods=["GET", "POST"])
@login_required
def view_purchases():
	purchases = ClientPurchases.query.all()
	held = ClientPurchasesHeld.query.all()
	volunteers = VolunteerPurchases.query.all()
	return render_template('purchases.html', held=held, purchases=purchases, volunteers=volunteers)


@app.route('/view_inventory', methods=["GET", "POST"])
def view_inventory():
	inventory = BookInventory.query.all()
	return render_template('inventory.html', inventory=inventory)


@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def remove(id):
	purchase_held = ClientPurchasesHeld.query.filter(ClientPurchasesHeld.id == id).first()
	purchase = ClientPurchases(client_id=purchase_held.id,
							isbn=purchase_held.isbn, 
							date=datetime.datetime.now(),
							condition=purchase_held.condition,
							edition=purchase_held.edition, 
							quantity=purchase_held.quantity) 
	book = BookInventory.query.filter(BookInventory.isbn == purchase_held.isbn, 
									   BookInventory.condition == purchase_held.condition,
									   BookInventory.edition == purchase_held.edition).first()
	if not book:
		flash('Book is Sold Out Now. Took too long for you to commit!')
		db.session.delete(purchase_held)
		db.session.commit()
		return redirect('/view_purchases')
	if book.quantity - purchase.quantity < 0:
		flash ("Error: not enough books to for that order!")
		return render_template('purchase.html')
	elif book.quantity - purchase.quantity == 0:
		flash("Book(s) successfully purchased! You got the last one!")
		current_isbn = book.isbn
		count = BookInventory.query.filter(BookInventory.isbn == book.isbn).count() - 1
		db.session.delete(book)
		#if count <= 0:
			#details = BookDetails.query.filter(BookDetails.isbn == current_isbn).first()
			#if details:
				#db.session.delete(details)
		db.session.delete(purchase_held)
		db.session.add(purchase)
		db.session.commit()
	else:
		book.quantity = book.quantity - purchase_held.quantity
		db.session.add(purchase)
		db.session.delete(purchase_held)
		db.session.commit()
		flash ("Book(s) successfully purchased. There are %d left" % book.quantity)
		return redirect('/view_purchases')

	return redirect('/view_purchases')


@app.route('/sample_queries', methods=["GET","POST"])
@login_required
def sample_queries():
	query1 = "SELECT AVG(tokens), MIN(tokens), MAX(tokens) FROM CLIENTS"
	query2 = "SELECT GENRE, SUM(QUANTITY) FROM BOOK_INVENTORY i, BOOK_DETAILS b WHERE (i.isbn = b.isbn) GROUP BY GENRE;"
	result = db.session.execute(query1)
	rows = []
	for row in result:
		rows.append(row)
	flash("%s" % query1) 
	flash("Returned:\tAvg(%s), Min(%d), Max(%d)" % (str(rows[0][0]), rows[0][1], rows[0][2]))
	result = db.session.execute(query2)
	rows = []
	for row in result:
		rows.append(row)
	flash(query2)
	flash("Returned:\t{}".format(rows))

	# Which book, regardless of the status of new or used, 
	#has more copies in inventory than any other? If there is a tie, list all the top books.
	books = BookDetails.query.all()
	quantities = []
	for book in books:
		quantity = int(db.session.query(func.sum(BookInventory.quantity)).filter(BookInventory.isbn == book.isbn)[0][0])
		quantities.append(quantity)
	maximum = max(quantities)
	index = quantities.index(maximum)
	if type(index) is not int:
		for i in index:
			flash("MAX QUANTITY ISBN: %s, %s, %d" % (books[index].isbn, books[index].title, quantities[index]))
	else:
		flash("MAX QUANTITY [ISBN: %s, Title: %s, Quantity: %d]" % (books[index].isbn, books[index].title, quantities[index]))

	#db.session.query(func.max(BookInventory.quantity))
	return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


# @app.route("/search", methods=['GET', 'POST'])
# def search():
# 	form = BookSearch()
# 	if request.method == 'POST' and form.validate():
# 		pass				


# 	return render_template('search.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	# """Allows user to edit profile"""
	
	form = CreatePerson()

	# if request.method == 'POST' and form.validate():
	# 	new_person = Person(form.first.data.title(), form.last.data.title(), 
	# 						form.birth.data, form.gender.data.title(),
	# 						form.phone.data.title(), form.email.data, 
	# 						form.street_name.data.title(),form.city.data.title(), 
	# 						form.state.data.upper(), form.zip_code.data)
	# 	db.session.add(new_person)
	# 	if form.volunteer.data:
	# 		volunteer = Volunteer()
	# 		volunteer.person_id = new_person.id
	# 		volunteer.person = new_person
	# 		db.session.add(volunteer)
	# 	if form.donor.data:
	# 		donor = Donor()
	# 		donor.person_id = new_person.id
	# 		donor.person = new_person
	# 		db.session.add(donor)
	# 	db.session.commit()
	# 	flash("Added id(%d): %s %s" % (new_person.id, 
	# 								   new_person.first_name, 
	# 								   new_person.last_name))
		
	# 		if form.validate_on_submit():
	# 	new_user = Person.query.filter_by(email=form.email.data).first()
	# 	if new_user is not None:
	# 		old_user = Volunteer.query.get(user.id)
	# 		if user is not None: #and user.verify_password(form.password.data):
	# 			login_user(user, form.remember_me.data)
	# 			flash("Logged in successfully.")
	# 			return redirect(request.args.get('next') or url_for('index'))

	#return redirect(request.args.get("next") or url_for("add_person"))
	return render_template('add.html', form=form)