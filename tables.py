import mysql.connector


connection = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    passwd= 'bwave',
    database= 'full_stack_bank_application'
)

cursor = connection.cursor()

cursor.execute('SHOW TABLES')

tables = cursor.fetchall()
for table in tables:
    print(table[0])


cursor.close()
connection.close()