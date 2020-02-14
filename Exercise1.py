import sqlite3 # To get the libraryr

conn = sqlite3.connect('orgdb.sqlite')
'''This will create file orgdb when it runs. We make a connection here. This connection check access to the file. '''

cur = conn.cursor()
''' This is like our handle. We send SQL commands through cursor, and get the responses through the same cursor. '''

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt' # Here we are using 'mbox.txt' as our file
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1] # Grabbing email address
    ram = email.split('@') # Splitting the email
    org = ram[1] # Grabbing the domain name of email like 'gmail.com'
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,)) # We are opening a record set using this.
    ''' Here Counts is our Table.
    The question mark is a placeholder. It is a way to make sure that we don't allow SQL injection. This question mark (placeholder) will ultimately
    be replaced by org.
    '''


    row = cur.fetchone() # Command to grab the first one. row will be the information that we get from database.
    # row will be none if there are no records that meet our criteria.
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,)) # We will insert row into counts.
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()
    ''' The database is efficiently keeping some of the information in memory and at some point, it has to write all the stuff out to disk.
    We do this using commit method.
    '''

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close() # FInally we close the connection.
