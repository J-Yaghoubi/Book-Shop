from menutools import Color, Menu
from public.interface import Operations


Color.BORDER = 32
Color.HEADER = 100
Color.MENU = 5
Color.PROMPT = 130
Color.INTERFACE = 144


main = Menu(header='Book Shop', align='center')

main.add(('Main menu', [
    ('Explore', Operations.explore),
    ('Login', Operations.login),
    ('Register', Operations.register),
    ('About', Operations.about_us),
    ('Exit', main.exit)
]))

main.add(('Logged', [
    ('Shopping', Operations.shopping),
    ('Asset', Operations.assets),
    ('Add Book', Operations.add_book),
    ('Information', Operations.information),
    ('Edit Account', Operations.edit),
    ('Logout', Operations.logout)
]))

main.add(('Explore', [
    ('Enter shop', exit),
    ('Back', 'Main menu')
]))
