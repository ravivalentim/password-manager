import mariadb
import sys
from menu import menu
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich import print

# Connect to MariaDB plataform
try:
    conn = mariadb.connect(
        user='root',
        password='root@server',
        host='localhost',
        port=3306,
        database='password_manager'
    )
except mariadb.Error as e:
    print(f'Erro connecting to MariaDB plataform: {e}')
    sys.exit(1)

# Get cursor
cur = conn.cursor()

# Rich console
console = Console()

banner = 'Welcome to Ravi\'s password manager [version 1.0] 😜'
print(Panel(Text(banner, justify="center", no_wrap=False), width=56))

# Data manipulation functions
def insert(name, login, password):
    try:
        cur.execute('INSERT INTO manager VALUES (?, ?, ?)',
                    (login, password, name)
        )
        conn.commit() 
    except mariadb.Error as e: 
        print(f'Error: {e}')

# view the query result
def view():
    table = Table(show_header=True, box=box.ROUNDED)
    
    table.add_column("Service", justify="center", style="white", no_wrap=True)
    table.add_column("Login", justify="center", style="white", no_wrap=True)
    table.add_column("Password", justify="center", style="white", no_wrap=True)

    for (login, password, name) in cur:
        table.add_row(name, login, password)

    console.print(table)

# select the login and password from table
def select(name):
    try:
        cur.execute(
            'SELECT * FROM manager WHERE name=?',
            (name,)
        )
        view()
    except mariadb.Error as e: 
        print(f'Error: {e}')

# delete login and password from table
def delete(name):
    console.print("\nWARNING: Are you sure you want to delete this data? Y/N ", style='red', end='')
    warning = str(input('')).lower()[0]
    if (warning == 'N'):
        return None
    try:
        cur.execute(
            'DELETE FROM manager WHERE name=?',
            (name,)
        )
    except mariadb.Error as e: 
        print(f'Error: {e}')

style = 'bold black'

# main loop
while (True):
    menu()
    console.print("\nEnter your option 🤔: ", style='bold white', end='')
    option = str(input(''))

    if option == '1':
        console.print("\nEnter the service name: ", style=style, end='')
        name = str(input(''))
        console.print("Enter the login credential ", style=style, end='')
        login = str(input(''))
        console.print("Enter the service password ", style=style, end='')
        password = str(input(''))
        insert(name, login, password)

    if (option == '2'):
        console.print("\nEnter the service name: ", style=style, end='')
        name = str(input(''))
        select(name)

    if (option == '3'):
        console.print("\nEnter the service name: ", style=style, end='')
        name = str(input(''))
        delete(name)

    if option == '4':
        console.print("\nBye ✌️: ", style=style, end='')
        break

conn.close()