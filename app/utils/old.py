# FROM APP.DB_FILL.py
# def add_person_quick(id, first_name, last_name, birth_date, gender,phone,email,street_name,city,state,zip_code):
# 	bool addVolunteer = addV;
# 	bool addDonor = addD;

# 	new_person = Person(id, first_name, last_name,birth_date, 
# 						gender,phone,email,street_name,city,
# 						state,zip_code)
# 	db.session.add(new_person)
# 	if addVolunteer = True:
# 		volunteer = Volunteer()
# 		volunteer.person_id = new_person.id
# 		volunteer.person = new.person
# 		db.session.add(volunteer)
# 		db.session.commit()
# 	if addDonor = True:
# 		donor = Donor()
# 		donor.person_id = new_person.id
# 		volunteer.person = new.person
# 		db.session.add(volunteer)
# 		db.session.commit()

# def add_client_quick(id,client_name,phone,email,street_name,city,state,zip_code,contact_name,tokens):
# 	new_client = (id,client_name,phone,email,street_name,city,state,zip_code,contact_name,tokens)
# 	db.session.add(new_client)
# 	db.session.commit()

# f_nm = "steve"
# steve.append(x)

#fill book_genre table

# FROM APP.MODELS

# class Address(db.Model):
# 	"""Address of a person or client. Street name includes number+name"""
# 	__tablename__ = 'addresses'
# 	id = db.Column(db.Integer, primary_key=True)
# 	street_name = db.Column(db.String(250), nullable=False)
# 	zip_code = db.Column(db.String(10), nullable=False)
	
# 	def __init__(self, street_name, zip_code):
# 		self.street_name = street_name
# 		self.zip_code = zip_code
# FORM APP.FORMS
# #delete this...cascade...
# class VolunteerPurchaseBook(Form): #how do we input for multiple authors?
# 	form_type = 'Book'
# 	isbn = IntegerField('ISBN', validators=[Required()])
# 	title = StringField('Title', validators=[Required()])
# 	edition = StringField('Edition', validators=[Required()])
# 	authors = TextAreaField('Authors (First Last)', validators=[Required()]) 
# 	reading_level = StringField('Reading Level', validators=[Required()])
# 	condition = SelectField('Condition', validators=[Required()], choices=[("New", "New"), ("Used", "Used")])
# 	publisher = StringField('Publisher', validators=[Required()])
# 	genre = StringField('Book Genre', validators=[Required()])
# 	cost = IntegerField('Cost'	)
# 	submit = SubmitField('Purchase')


# FROM APP.VIEWS
# @app.route('/volunteer_purchase_book', methods=['GET', 'POST'])
# @login_required #and they have to be a volunteer...can we check they're a volunteer not a donor?
# def volunteer_purchase_book():
# 	#bookdetails must also be updated
# 	#include cost, check cost against cashinventory.
# 	form = VolunteerPurchaseBook()
# 	if request.method == 'POST' and form.validate():
# 		# book = VolunteerPurchases(form.isbn.data, form.title.data.title(), 
# 		# 						form.edition.data.title(), form.reading_level.data.title(),
# 		# 						form.publisher.data.title(),form.genre.data.title(),
# 		# 						form.condition.data.title(), form.cost.data)
# 		# book = VolunteerPurchases()
# 		# book.isbn = form.isbn.data
# 		# book.title = form.title.data.title()
# 		# book.edition = form.edition.data.title()
# 		# book.reading_level = form.reading_level.data.title()
# 		# book.publisher = form.publisher.data.title()
# 		# book.genre = form.genre.data.title()
# 		# book.condition = form.condition.data.title()
# 		# book.cost = form.cost.data

# 		#also capture current session and store in volunteer_id?
# 		# book.volunteer_id = Volunteer.query.get(current_user.id) #this doesn't work
# 		# flash("CurrentUser (%s)" % (book.volunteer_id))
# 		#assign id? does it automatically increment?

# 		#add to volunteer_purchase_book
# 		# db.session.add(book)
# 		#add to book_details
# 		bookD = BookDetails()
# 		bookD.isbn = book.isbn 
# 		bookD.title = book.title
# 		bookD.reading_level = book.reading_level
# 		bookD.publisher = book.publisher
# 		bookD.genre = book.genre
# 		bookD.condition = book.condition
# 		bookD.inventory.author = form.author.data.title() #is this correct?

# 		#add to book_inventory

# 		#add to author_book?


# 		funds = CashInventory.query.get(funds) #is this how do I select a single tuple?
# 		flash("Funds: %f ") % (funds)
# 		# if (cost.cost > funds): #is this correct?
# 			#print out an error for funds
# 		# else:
# 			#need to add to bookdonation, bookinventory, and bookdetails...
# 			# db.session.add(book)
# 			#decrement funds
# 			#flash success
# 			#flash("Purchased book(%d): %s" % (book.isbn, book.title))
# 			#db.session.commit()
# 		return redirect(url_for('volunteer_purchase_book'))
# 	return render_template('add.html', form = form)