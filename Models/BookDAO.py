class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "books"

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q


	def reserve(self, user_id, book_id):
		if not self.available(book_id):
			return "err_out"

		q = self.db.query("INSERT INTO reserve (user_id, book_id) VALUES('{}', '{}');".format(user_id, book_id))
		
		self.db.query("UPDATE @table set count=count-1 where id={};".format(book_id))
		self.db.commit()

		return q

	def getBooksByUser(self, user_id):
		q = self.db.query("select * from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBooksCountByUser(self, user_id):
		q = self.db.query("select count(reserve.book_id) as books_count from @table left join reserve on reserve.book_id = @table.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBook(self, id):
		q = self.db.query("select * from @table where id={}".format(id))

		book = q.fetchone()

		print(book)
		return book

	def available(self, id):
		book = self.getById(id)
		count = book['count']

		if count < 1:
			return False

		return True

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		book = q.fetchone()

		return book

	def list(self, availability=1):
		query="select * from @table"
		# Usually when no-admin user query for book
		if availability==1: query= query+"  WHERE availability={}".format(availability)
		
		books = self.db.query(query)
		
		books = books.fetchall()


		return books

	def getReserverdBooksByUser(self, user_id):
		query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
		
		books = self.db.query(query)
		
		books = books.fetchone()


		return books

	def search_book(self, name, availability=1):
		query="select * from @table where name LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books
	def add(self, book_details):
		try:
			# Construct the SQL query
			query = f"INSERT INTO {self.db.table} (name, description, author, availability, edition, count) VALUES ('{book_details['name']}', '{book_details['description']}', '{book_details['author']}', {book_details['availability']}, '{book_details['edition']}', {book_details['count']})"
			# Execute the query
			self.db.query(query)
			self.db.commit()
			return True
		except Exception as e:
			print(f"Error adding book: {e}")
			return False
		
	def update(self, book_info, id):
		name = book_info['name']
		author = book_info['author']
		edition = book_info['edition']
		count = book_info['count']
		availability = book_info['availability']
		description = book_info['description']
		
		sql = "UPDATE {} SET name = '{}', author = '{}', edition = '{}', count = '{}', availability = '{}', description = '{}' WHERE id = {}".format('@table', name, author, edition, count, availability, description, id)
		q = self.db.query(sql)
		
		self.db.commit()
		return q

