# this line imports functionality into our project, so we don't have to write it ourselves 
from flask import Flask, render_template, request, redirect 
#importing the database language SQL for implementing database
import sqlite3

# The below line represents the start of every good Flask app
app = Flask (__name__) #this is the line of code we would always write, basically it creates a flask object

items = []

db_path = 'checklist.db' # Creates a database file to store user data..

# This below function creates a table in the databse thereby storing the data in a table format

def create_table():
    conn = sqlite3.connect(db_path) # Connects the SQL database to the mentioned database created 'db_path' using a connection variable
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS checklist 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT)''') 
    conn.commit() 
    conn.close() 

def get_items():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM checklist") 
    items = c.fetchall() 
    conn.close()
    return items

def add_item(item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO checklist (item) VALUES (?)", (item,)) 
    conn.commit()
    conn.close()

def update_item(item_id, new_item):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE checklist SET item = ? WHERE id = ?", (new_item, item_id)) 
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM checklist WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# Creating the 'read' functionality
@app.route ('/')
def checklist():
    create_table()
    items = get_items()
    return render_template ('checklist.html', items=items)

# Creating the 'create' functionality
@app.route ('/add', methods = ['POST'])
def add():
    item = request.form['item']
    add_item(item) #Appends the new item to the list 'items' which are currently not yet stored in the database
    return redirect('/')

# Creating the 'update' functionality
@app.route ('/edit/<int:item_id>', methods = ['GET', 'POST']) # User would retrieve an item and can also update for which GET and POST
def edit(item_id):
    
    if request.method == 'POST':
        new_item = request.form ['item']
        update_item(item_id, new_item)
        return redirect ('/')
    else:
        items = get_items()
        item = next((x[1] for x in items if x[0] == item_id), None)
        return render_template ('edit.html', item = item, item_id = item_id)

# Creating the delete functionality
@app.route ('/delete/<int:item_id>')
def delete(item_id):
    delete_item(item_id) 
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)