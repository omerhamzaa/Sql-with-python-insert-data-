import sqlite3
import csv
from fastapi import FastAPI
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

conn = sqlite3.connect('Sentiment .db')
conn1 = sqlite3.connect('iris.db')
conn2 = sqlite3.connect('student.db')
c = conn.cursor()
c1 = conn1.cursor()
c2 = conn2.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Sentiment
             (ID INTEGER PRIMARY KEY,review object, sentiment object )''')
# Create second table
c1.execute('''CREATE TABLE IF NOT EXISTS Iris
             (ID INTEGER PRIMARY KEY,SepalLengthCm float64, SepalWidthCm float64, PetalLengthCm float64, PetalWidthCm float64, Species object )''')
# Create 3rd table
c2.execute('''CREATE TABLE IF NOT EXISTS Student
             (ID INTEGER PRIMARY KEY,time float64, marks int64 )''')


with open(r'C:\Users\razza\Desktop\student\student marks.csv', 'r') as file:
    # Your code to read the CSV file

    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        c2.execute("INSERT INTO Student (time, marks) VALUES (?, ?)", row)

with open(r'C:\Users\razza\Desktop\iris\iris.csv', 'r') as file:
    # Your code to read the CSV file

    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        c1.execute("INSERT INTO Iris (SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species) VALUES (?, ?, ?, ?, ?)", row)

with open(r'C:\Users\razza\Desktop\analysis\Sentiment data.csv', 'r') as file:

    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        c.execute("INSERT INTO Sentiment (review, sentiment) VALUES (?, ?)", row)
        

c.execute("SELECT * FROM Sentiment")
data = c.fetchall()
reviews = [row[1] for row in data]
sentiments = [row[2] for row in data]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(reviews)
X_train, X_test, y_train, y_test = train_test_split(X, sentiments, test_size=0.2, random_state=42)
classifier = BernoulliNB()
classifier.fit(X_train, y_train)

@app.get("/Sentiment_analysis_accuracy")
async def accuracy():
    accuracy = classifier.score(X_test, y_test)

    return {"Accuracy of Bernouli naive bayes with Sentiment data :", accuracy}

@app.get("/get Student data")
async def get_all_data():
    c2.execute("SELECT * FROM Student")
    return("Student Data is ",c2.fetchall())

@app.get("/get Iris data")
async def get_all_data():
    c1.execute("SELECT * FROM Iris")
    return("Iris  Data is ",c1.fetchall())

@app.get("/get Sentiment data")
async def get_all_data():
    c.execute("SELECT * FROM Sentiment")
    return("Sentiment Data is ",c.fetchall())