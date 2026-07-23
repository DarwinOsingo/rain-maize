class Book:
    def __init__(self,title,author):
        self.title = title
        self.author = author
        self.is_borrowed = False    

class Member :
    def __init__(self,name,books_taken):
        self.name = name
        self.books_taken = []
class Library:
    def __init__(self):
        self.book = []
        self.members = []
    def add_book(self,book):
        self.book.append(book)
        print(f"{book.title} has been added ")
    
    def register_member(self,member):
        self.members.append(member)
        print(f"Welcome to the Library {member.name}")
    def borrow_book(self,book,member):
        if member not in self.members:
            print("You must be a library member to borrow a book")
            return
        if book not in self.book:
            print("The book you typed is not in our system please retry")
            return
        
        elif book.is_burrowed:
            print("The book has been borrowed and will be returned at a later date")
        else:
            book.is_taken = True
            member.books_taken.append(book)
            
            print(f"You have succesfully borrowed {book.title}")
    def return_book(self,book,member):
        if member not in self.members:
            print("You cannot return a book if you arent a member")
            return
        elif book.is_borrowed:
            print("Thankyou for returning the book")
            self.book.append(book)
            book.is_taken = False
        else:
            print("You cannot return a book that you havent taken out buddy")
    def show_books(self,books):
        print("="*50)
        print("\n WELCOME TO THE LIBRARY")
        print("="*50)
        for book in books:
            status = "Borrowed" if book.is_borrowed else "Avaialable"
            print(f"\n{book.title} status :{status}")
    def show_member_books(self,member):
        print("="*50)
        print(f"\n WELCOME TO THE LIBRARY :{member} These are your books!")
        print("="*50)
        for index,book in enumerate(member.books_taken,start=1):
            print(f"\n  {index}:{book}")





    
    

        