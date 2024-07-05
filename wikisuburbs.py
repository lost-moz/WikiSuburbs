import sqlite3    
from flask import Flask, render_template, request
app = Flask(__name__) #creates an app
# Establishing connection, open a SQLite connection, create a database cursor
cur = sqlite3.connect('wikisuburbs.db', check_same_thread=False).cursor()
cur.execute('SELECT * FROM main') #return all results from the table main
records = cur.fetchall()#fetches all the records (rows) of a query result.
cur.execute('SELECT DISTINCT SUBURB FROM main ORDER BY SUBURB ASC') # returns all the suburbs in table main by alphabetical order
subs = cur.fetchall()#fetches all the records (rows) of a query result
cur.execute('SELECT DISTINCT STRUCTURETYPE FROM main') # returns all the structure types in table main
tab = cur.fetchall()#fetches all the records (rows) of a query result

suburbs = []
for i in range(len(subs)):
    suburbs.append(str(subs[i]).replace("('","").replace("',)",""))
print(suburbs)
@app.route('/', methods=['POST','GET']) #the landing page will run the function below to generate HTML 
def index(): #the function will run when the website directory is http://127.0.0.1:5000
    error = None #Assign no value to error when website is opened or refreshed
    search = ""
    if request.method == "POST": #Does code below if the user inputs data into forms
        search = request.form['sub'].title() #assigns value of the text box into search variable
        structures = request.form.getlist('structuretype') #assigns values of the checklist into structures list
        if search not in suburbs: #Does code below if the user inputs a suburb that doesn't exist in Brisbane in the text box
            error = "The suburb '"+search+"' does not exist" #returns an error
        else:
            global records #Allows the variable records to be altered in this function
            if len(structures) == 5: #Does code below if there is 5 values in the structures list
                cur.execute('SELECT * FROM main WHERE SUBURB = ?', (search,)) #returns all results from table main where suburb equals to the search variable
                records = cur.fetchall()#fetches all the records (rows) of a query result.
            elif len(structures) == 4: #Does code below if there is 4 values in the structures list
                cur.execute('SELECT * FROM main WHERE SUBURB = ? AND (STRUCTURETYPE = ? OR STRUCTURETYPE = ? OR STRUCTURETYPE = ? OR STRUCTURETYPE = ?)',\
                (search,str(structures[0]),str(structures[1]),str(structures[2]),str(structures[3]),))
                records = cur.fetchall()#fetches all the records (rows) of a query result.
            elif len(structures) == 3: #Does code below if there is 3 values in the structures list
                cur.execute('SELECT * FROM main WHERE SUBURB = ? AND (STRUCTURETYPE = ? OR STRUCTURETYPE = ? OR STRUCTURETYPE = ?)',\
                (search,str(structures[0]),str(structures[1]),str(structures[2]),))
                records = cur.fetchall() #fetches all the records (rows) of a query result.
            elif len(structures) == 2: #Does code below if there is 2 values in the structures list
                cur.execute('SELECT * FROM main WHERE SUBURB = ? AND (STRUCTURETYPE = ? OR STRUCTURETYPE = ?)', \
                (search,str(structures[0]),str(structures[1]),))
                records = cur.fetchall()#fetches all the records (rows) of a query result.
            elif len(structures) == 1:#Does code below if there is 1 value in the structures list
                cur.execute('SELECT * FROM main WHERE SUBURB = ? AND STRUCTURETYPE = ?', (search,str(structures[0]),))
                records = cur.fetchall()#fetches all the records (rows) of a query result.
    return render_template('index.html', records=records, subs=suburbs, error = error, search=search)#render the html template index.html including the variable


if __name__ == '__main__': #if this is the main file for the application, run the application
    app.run(debug = True)