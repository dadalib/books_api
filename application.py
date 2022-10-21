import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

# Set up db
uri = os.getenv("DATABASE_URL")
if uri.startswith('postgres://'):
    uri = uri.replace("postgres://","postgresql://",1)
    print("uri changed",uri)

engine = create_engine(uri)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("bookks.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn, :tittle, :author, :year)",
        {"isbn":isbn,"tittle":title,"author":author,"year":int(year) })

        print(f"Added book:{title}")
    
    db.commit()

if __name__ == '__main__':
    main()
