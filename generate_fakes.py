#!flask/bin/python
from app import db
from app.models import ReadingLevels, BookGenre, Volunteer, Person, Donor, CashInventory, Author, BookDetails, BookInventory, Client


def generate_fakes():
	Author.generate_fake()
	BookDetails.generate_fake()
	BookInventory.generate_fake()
	Client.generate_fake()
	Person.generate_fake()
	Volunteer.generate_fake()
	Donor.generate_fake()

if __name__ == '__main__':
	generate_fakes()
