from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from character_lists import letters, symbols, numbers
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# TODO: Save file in a secure location on computer
# TODO: Test saved file for identical site and login details, replace with new password
# TODO: Address overwriting problem - if site already has a login, only replace password if login matches


def generate_password():
    """Generates a random set of letters, numbers, and symbols of semi-random length before combining and randomizing
    them. Enters the password into the password field, then copies the password to the clipboard so it can easily be
    pasted."""
    # Define password length
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # Choose random letters, symbols, numbers and add to lists
    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    # Create full password and randomize the input order, join the list to a string
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    new_password = ''.join(password_list)

    # Delete any current password entries and add new one to window
    password_entry.delete(0, 'end')
    password_entry.insert(0, new_password)
    pyperclip.copy(new_password)


def save_password():
    """Verifies user has entered info into all three fields, then saves the login details to a file following user
    confirmation, wiping the site and password so user can immediately enter new details.

    Has popup warnings for missing data and for user confirmation."""
    site = website_entry.get()
    login = username_entry.get()
    pw = password_entry.get()
    new_data = {
        site: {
            'email': login,
            'password': pw,
        }
    }

    if len(site) == 0 or len(login) == 0 or len(pw) == 0:  # Verify fields are populated
        messagebox.showwarning(title='Oops!', message='Please don"t leave any fields empty!')
    else:  # Delete site and password, update file

        try:
            # Try to open JSON file
            with open('data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # Create file if it does not exist
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            # Update JSON file if it existed
            data.update(new_data)

            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)
        finally:
            # Delete entry fields in app
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #
# Creates the window and a canvas to host the lock image and text overlay
window = Tk()
window.title('Password Generator')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Creates all labels, buttons, and entries by row
# Row 1
website = Label(text='Website:')
website.grid(row=1, column=0)

website_entry = Entry(width=53)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, pady=3)

# Row 2
username = Label(text='Email/Username:')
username.grid(row=2, column=0)

username_entry = Entry(width=53)
username_entry.insert(0, 'jchase466@gmail.com')
username_entry.grid(row=2, column=1, columnspan=2, pady=3)

# Row 3
password = Label(text='Password:')
password.grid(row=3, column=0)

password_entry = Entry(width=34)
password_entry.grid(row=3, column=1, columnspan=1)

generate = Button(text='Generate Password', width=14, command=generate_password)
generate.grid(row=3, column=2, pady=3)

# Row 4
add = Button(text='Add', width=43, command=save_password)
add.grid(row=4, column=1, columnspan=2, pady=3)

window.mainloop()  # Keeps window running
