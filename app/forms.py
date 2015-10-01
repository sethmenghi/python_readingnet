from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, BooleanField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
	email = StringField('Volunteer Email', validators=[Required(), Length(1,64)])
	#password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Remember Me', default=False)
	submit = SubmitField('Login')


class CreatePerson(Form):
	form_type = 'Person'
	first = StringField('First Name', validators=[Required()])
	last = StringField('Last Name', validators=[Required()])
	birth = DateField('Birth Date (mm/dd/yyyy)', validators=[Required()], format='%m/%d/%Y')
	gender = SelectField('Gender', validators=[Required()], choices=[("Male", "Male"), ("Female", "Female")])
	phone = StringField('Phone Number', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	street_name = StringField('Street Address', validators=[Required()])
	city = StringField('City', validators=[Required()])
	state = StringField('State (XX)', validators=[Required(), Length(min=2,max=2)])
	zip_code = StringField('Zip Code', validators=[Required()])

	volunteer = BooleanField('Volunteer')
	donor = BooleanField('Donor')
	submit = SubmitField('Save')


class CreateClient(Form):
	form_type = 'Client'
	name = StringField('Client Name', validators=[Required()])
	phone = StringField('Phone Number', validators=[Required()])
	email = StringField('Email Address', validators=[Required()])
	reading_level = SelectField('Reading Level', validators=[Required()], choices=[("Adult", "Adult"), ("Teen", "Teen"), ("Children", "Children")])
	street_name = StringField('Street Address', validators=[Required()])
	city = StringField('City', validators=[Required()])
	state = StringField('State (XX)', validators=[Required(), Length(min=2,max=2)])
	zip_code = StringField('Zip Code', validators=[Required()])
	contact = StringField('Contact Person')
	submit = SubmitField('Save')


class CreateBook(Form): #how do we input for multiple authors?
	form_type = 'Book'
	donor_id = StringField('Donor ID', validators=[Required()])
	isbn = IntegerField('ISBN', validators=[Required()])
	title = StringField('Title', validators=[Required()])
	edition = SelectField('Edition', validators=[Required()], choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9+","9+")])
	authors = TextAreaField('Authors (First Last)', validators=[Required()]) 
	reading_level = SelectField('Reading Level', validators=[Required()], choices=[("Adult", "Adult"), ("Teen", "Teen"), ("Children", "Children")])
	condition = SelectField('Condition', validators=[Required()], choices=[("New", "New"), ("Used", "Used")])
	publisher = StringField('Publisher', validators=[Required()])
	genre = SelectField('Book Genre', validators=[Required()], choices=[("Autobiography","Autobiography"),("Biography","Biography"),("Comic","Comic"),("Crime/Detective","Crime/Detective"),("Fantasy","Fantasy"), ("Historical Fiction", "Historical Fiction"),("Magical Realism", "Magical Realism"), ("Mystery","Mystery"),("Mythopoeia","Mythopoeia"),("Poetry", "Poetry"),("Realistic Fiction", "Realistic Fiction"),("Scientific Fiction", "Scientific Fiction"),("Short Story","Short Story"),("Textbook", "Textbook"),("Thriller", "Thriller"),("Western", "Western")])
	cost = IntegerField('Cost', default=0) #if cost is zero, treat as a donation (add to donation table, give tokens?). Otherwise it's a purchase, compare it to the funds, and push it into the purchase table
	submit = SubmitField('Submit')


class RemovePerson(Form):
	form_type = 'Person'
	person_id = IntegerField('PersonID')
	email = StringField('Email', validators=[Email()])
	submit = SubmitField('Remove')


class RemoveClient(Form):
	form_type = 'Client'
	client_id = IntegerField('ClientID')
	submit = SubmitField('Remove')


class RemoveBook(Form):
	form_type ='Book'
	isbn = IntegerField('ISBN')
	edition = SelectField('Edition', validators=[Required()], choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9+","9+")])
	condition = SelectField('Condition', validators=[Required()], choices=[("New", "New"), ("Used", "Used")])
	quantity = IntegerField('Quantity', validators=[Required()], default=1)
	submit = SubmitField('Remove')


class ClientPurchaseBook(Form):
	form_type = 'Book'
	# title = StringField('Title', validators=[Required()])
	# authors = TextAreaField('Authors (First Last)', validators=[Required()]) 
	isbn = IntegerField('ISBN', validators=[Required()])
	edition = SelectField('Edition', choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9+","9+")], default="")
	condition = SelectField('Condition', validators=[Required()], choices=[("New", "New"), ("Used", "Used")])
	quantity = IntegerField('Quantity', validators=[Required()], default=1)
	client_id = IntegerField('Client ID', validators=[Required()])
	submit = SubmitField('Purchase')
	#what else? more maybe..?

class SearchBooks(Form):
	form_type = 'Book'
	isbn = IntegerField('ISBN')
	title = StringField('Title')
	edition = SelectField('Edition', choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9+","9+")], default="")
	authors = TextAreaField('Authors (First Last)') 
	reading_level = SelectField('Reading Level', choices=[("Adult", "Adult"), ("Teen", "Teen"), ("Children", "Children")], default="")
	condition = SelectField('Condition', choices=[("New", "New"), ("Used", "Used")])
	publisher = StringField('Publisher')
	genre = SelectField('Book Genre', choices=[("Autobiography","Autobiography"),("Biography","Biography"),("Comic","Comic"),("Crime/Detective","Crime/Detective"),("Fantasy","Fantasy"), ("Historical Fiction", "Historical Fiction"),("Magical Realism", "Magical Realism"), ("Mystery","Mystery"),("Mythopoeia","Mythopoeia"),("Poetry", "Poetry"),("Realistic Fiction", "Realistic Fiction"),("Scientific Fiction", "Scientific Fiction"),("Short Story","Short Story"),("Textbook", "Textbook"),("Thriller", "Thriller"),("Western", "Western")])
	submit = SubmitField('Search')

class BookSearchByTitle(Form):
	form_type = 'Book'
	title = StringField('Title', validators=[Required()])
	submit = SubmitField('Search')

class AddTokens(Form):
	form_type = 'Client'
	client_id = IntegerField('Client ID', validators=[Required()])
	tokens_to_add = IntegerField('Tokens to Add', validators=[Required()])
	submit = SubmitField('Submit')

class DonateCash(Form):
	form_type = 'Donation'
	donor_id = IntegerField('Donor ID', validators=[Required()])
	amount =  IntegerField('Amount', validators=[Required()])
	submit = SubmitField('Donate')


# class EditProfile(Form):
# 	form_type = 'Person'
# 	first = StringField('First Name', validators=[Required()])
# 	last = StringField('Last Name', validators=[Required()])
# 	birth = DateField('Birth Date (mm/dd/yyyy)', validators=[Required()], format='%m/%d/%Y')
# 	gender = SelectField('Gender', validators=[Required()], choices=[("Male", "Male"), ("Female", "Female")])
# 	phone = StringField('Phone Number', validators=[Required()])
# 	email = StringField('Email Address', validators=[Required()])
# 	street_name = StringField('Street Address', validators=[Required()])
# 	city = StringField('City', validators=[Required()])
# 	state = StringField('State (XX)', validators=[Required(), Length(min=2,max=2)])
# 	zip_code = StringField('Zip Code', validators=[Required()])

# 	volunteer = BooleanField('Volunteer')
# 	donor = BooleanField('Donor')
# 	submit = SubmitField('Save')



