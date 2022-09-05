from menutools import Color, Menu
from public.interface import *


# Define style for menu
Color.BORDER = 32
Color.HEADER = 100
Color.MENU = 5
Color.PROMPT = 130
Color.INTERFACE = 144

# Create menu
main = Menu(header='Book Shop', align='center')

main.add(('Main menu', [('Explore', Operations.explore), ('Login', Operations.login), ('Register', Operations.register), ('About', Operations.about_us), ('Exit', main.exit)]))
main.add(('Logged', [('Shopping', Operations.shopping), ('Add Book', Operations.add_book), ('Edit Account', Operations.edit), ('Asset', Operations.assets), ('Logout', main.back)]))
main.add(('Explore', [('Enter shop', exit), ('Back', 'Main menu')]))

