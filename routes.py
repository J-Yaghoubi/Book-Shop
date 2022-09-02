from core.menu import Color, Menu
from public import *
from public.utils import *

# Define style for menu
Color.HEADER = 32
Color.MENU = 5
Color.SHELL = 130
Color.INTERFACE = 144

# Create menu
main = Menu(header='Book Shop')
main.add(('Main menu', [('Explore', Operations.explore), ('Login', Operations.login), ('Register', Operations.register), ('About', Operations.about_us), ('Exit', main.exit)]))
main.add(('Logged', [('Shopping', Operations.shopping), ('Add Book', Operations.add_book), ('Edit Account', Operations.edit), ('Asset', Operations.assets), ('Logout', main.back)]))
main.add(('Explore', [('Enter shop', exit), ('Back', 'Main menu')]))


