from ..app import db
from ..app.models import BookGenre, Volunteers, Persons, Donors, ReadingLevels

def init_persons():
	Persons.generate_fake(100)
	Donors.generate_fake()
	Volunteers.generate_fake()

def init_reading_levels():
	rl = ReadingLevels()
	rl.reading_level = "Adult"
	db.session.add(rl)

	rl = ReadingLevels()
	rl.reading_level = "Teen"
	db.session.add(rl)	

	rl = ReadingLevels()
	rl.reading_level = "Children"
	db.session.add(rl)

	db.session.commit()

def init_genre():
	book_genre = BookGenre()
	book_genre.genre = "Autobiography"
	book_genre.genre_description = "Ready to read how proud someone is of themselves? Then you've come to the right place!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Biography"
	book_genre.genre_description = "When being self-obsessed isn't enough, why not read all about the intimate details of someone else?"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Comic"
	book_genre.genre_description = "Re-live your childhood years by reading graphic about superheros, or just every day life in this interesting art medium."
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Crime/Detective"
	book_genre.genre_description = "Who killed Mrs. Peabody? Was it the butler? The maid? Some rich person that's bored (i.e. the rest of the house)? You'll have to read to find out!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Fantasy"
	book_genre.genre_description = "When the real world isn't enough, escape to a far off land of complicated names that somehow always serves as a reflection of mankind."
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Historical Fiction"
	book_genre.genre_description = "Ever wondered, \"Wouldn't it be cool if someone wrote a story of what it was like living in <insert period author didn't live during>\"? So did these authors apparently."
	db.session.add(book_genre)
	
	book_genre = BookGenre()
	book_genre.genre = "Magical Realism"
	book_genre.genre_description = "Also known as Realismo Magico, these stories depict what happens when the gentle hand of fate puts everything 'just right' for something magical to happen"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Mystery"
	book_genre.genre_description = "Not really sure how this is different from crime, but it's suspenseful nonetheless!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Mythopoeia"
	book_genre.genre_description = "I don't actually know what this is but I imagine it is a mix of myth and something else. I'd buy a book--It sounds interesting!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Poetry"
	book_genre.genre_description = "When life is too convoluted, why not spend time seeing how poets distill our complicated world into just a few lines?"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Realistic Fiction"
	book_genre.genre_description = "It's fiction, but it seems real! In other words, it's almost everything other than fantasy or folklore."
	db.session.add(book_genre)
	
	book_genre = BookGenre()
	book_genre.genre = "Scientific Fiction"
	book_genre.genre_description = "Ever thought it would be really cool to do something impossible? In the world of SciFi, something is only impossible if you say it is."
	db.session.add(book_genre)
	
	book_genre = BookGenre()
	book_genre.genre = "Short Story"
	book_genre.genre_description = "Not interested in a big commitment? Read a short story and leave with one or two interesting thoughts!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Textbook"
	book_genre.genre_description = "Oh come on, who wants to actually learn? Go get a SciFi book!"
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Thriller"
	book_genre.genre_description = "These short novels are just exciting enough to capture your attention until the book is finished, but they are quickly forgotten. So sad."
	db.session.add(book_genre)

	book_genre = BookGenre()
	book_genre.genre = "Western"
	book_genre.genre_description = "Re-live the glamorized west during the settlement of the Great Frontier!"
	db.session.add(book_genre)
	db.session.commit()

if __name__ == '__main__':
	init_genre()
	init_persons()