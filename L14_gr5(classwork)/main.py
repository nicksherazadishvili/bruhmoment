from flask import Flask, redirect, url_for, render_template, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class Books(Base):
    __tablename__ = 'Amazon'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    author = Column(String(40), nullable=False)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f'Book title: {self.title}; Author: {self.author}; Price: {self.price}'
    
engine = create_engine('sqlite:///books.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in flask_session:
        subjects = ['Python', 'Calculus', 'DB']
        return render_template('user.html', subjects=subjects)
    return redirect(url_for('login'))

@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    flask_session.pop('user', None)
    return 'You are logged out'

@app.route('/amazonproducts', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        if title and author and price:
            try:
                price = float(price)
                new_book = Books(title=title, author=author, price=price)
                db_session.add(new_book)
                db_session.commit()
                return 'Data added successfully'
            except ValueError:
                return 'Invalid input for price'
    return render_template('amazonproducts.html')

if __name__ == "__main__":
    app.run(debug=True)

book1 = Books(title='Python', author='Guido van Rossum', price=100.0)
db_session.add(book1)
db_session.commit()

book2 = Books(title='Calculus', author='Newton', price=200.0)
db_session.add(book2)
db_session.commit()

result = db_session.query(Books).all()
for row in result:
    print(row)

