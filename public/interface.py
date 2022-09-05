from configs import Info
from configs import LoggedUser
from configs import DbConfig
from model import User
from model import Content
from model import Comment
from exceptions import StructureError
from core.managers import DBManager
from core.cryptic import *
import shutil
from core.utils import clear_screen
import logging
from hashlib import sha1
import os
from getpass import getpass


class Operations:
    """
        The program will give user requests through menu-selecting
        and handle them through methods of this class
    """

    @staticmethod
    def about_us() -> None:
        """
            Print information of project and author
        """
        print(f"Project: {Info.PROJECT.value}")
        print(f"Version: {Info.VERSION.value}")
        print(f"Author: {Info.AUTHOR.value}")
        print(f"Description: {Info.DESCRIPTION.value}")

    @staticmethod
    def register() -> None:
        """
            Register new user and save the information on the users-table
        """
        inputs = []
        for c, m in zip(User.columns, User.messages):
            inputs.append(input(f'{c} ({m}) >> '))
        try:
            find = DBManager().read('id', User, f"username = '{inputs[4].lower()}'")   

            if find:
                print('\nUsername is duplicated. Try again later...')
            else:    
                # Add to database    
                u = User(inputs[0].lower(), inputs[1].lower(), inputs[2], inputs[3], inputs[4].lower(), inputs[5])
                DBManager().insert(u)
                
                # Generate key and store in file
                write_key('users/' + u.code + '.key')

                # Log the operation
                logging.debug(f'New User has been registered: {inputs[0].lower()} {inputs[1].lower()}')
                print('\nRegistration has been successful')
                print(f'\nThis is your encrypting code: {u.code}\nStore it in safe place...')

        except StructureError as e:
            logging.warning(f'Problem in reregistration for: {inputs[0].lower()} {inputs[1].lower()}')
            print(f'\n{e}')

    @staticmethod
    def edit() -> None:
        """
            Handle the request of changing the user information
        """

        find = DBManager().read('first_name, last_name, phone, password', User, f"id='{LoggedUser.ID}'") 
        print('Feed.update Enter.old-data\n')

        fname = input(f'{User.columns[0]} ({User.messages[0]}) => ')
        lname = input(f'{User.columns[1]} ({User.messages[1]}) => ')
        phone = input(f'{User.columns[2]} ({User.messages[2]}) => ')
        password = input(f'{User.columns[5]} ({User.messages[5]}) => ')

        if fname == '': fname = find[0][0]
        if lname == '': lname = find[0][1]
        if phone == '': phone = find[0][2]
        if password == '': password = find[0][3]

        try:    
            # validate the inputted data
            User(fname, lname, phone , '0111111111', 'test', password)
            # update information's
            DBManager().update(User, '(first_name, last_name, phone, password)', f"('{fname.lower()}', '{lname.lower()}', '{phone}', '{password}')", f"id = '{LoggedUser.ID}'")
            logging.debug(f'Data edited for: {find[0][0]} {find[0][1]}')
            print('\nEdit has been successful')

        except StructureError as e:
            logging.warning(f'Failed to edit data for: {find[0][0]} {find[0][1]}')
            print(e)

    @staticmethod
    def explore() -> None:
        """
            Explore in the shop and print contents list without any functionality
        """
        data = DBManager().read('id, name, owner', Content, '')
        print('ID        Book Name           Owner')
        print('==================================================\n')
        for row in data:
            print(f"{str(row[0]):<10}{row[1]:<20}{row[2]:<26}") 
        logging.warning(f'Anonymous user explored the shop')

    @staticmethod
    def login() -> None | str:
        """
            User login process
        """

        u = (input(f'username >> ')).lower()
        p = getpass(f'password >> ') 
        p += DbConfig.PASSWORD.value
        p = sha1(p.encode()).hexdigest()        

        find = DBManager().read('id, first_name, last_name', User, f"username = '{u}' and password = '{p}'")   
        
        if not find:
            logging.warning(f'Failed attempt for login')
            print('\nSorry!\nPlease check your input or register as new client')
        else:
            find = find[0]
            LoggedUser.ID = find[0]
            LoggedUser.FULLNAME = f'{find[1]} {find[2]}'
            logging.debug(f'{find[1]} {find[2]} has been logged in')       
            print(f'\nWelcome {LoggedUser.FULLNAME}')
            return 'Logged'

    @staticmethod
    def add_book() -> None:
        """
            Gift a book to the shop and increase the balance
        """
        name = input('Book name.extension >> ') 
        path = input('Book patch >> ') 
        result = DBManager().read('name', Content, f"name = '{name}'")  

        if result:
            logging.warning(f'attempt for adding duplicated {name}')  
            print('You can not add duplicated file to store!')
        else:
            try:
                # Transfer file to store
                shutil.copy2(path + name, 'store/' + name)
            except:
                print('Transferring has been field. Please check the path and filename')
                logging.warning(f'Failed attempt for adding: {name}')

            else:    
                # Read the key and encrypt file with this key
                code = DBManager().read('code', User, f"id = '{LoggedUser.ID}'")[0][0]
                crypto_key = load_key(f'users/{code}.key') 
                encrypt('store/' + name, crypto_key)

                # Save information to the database
                DBManager().insert(Content(LoggedUser.FULLNAME, LoggedUser.ID, name))
                logging.debug(f'{name} has been registered for {LoggedUser.FULLNAME}')   

                # Increase balance by one and update the database
                Operations.change_balance()
                logging.debug(f'Balance for {LoggedUser.FULLNAME} increased by 0ne')  

                print('Your gift added to the store successfully...')

    @staticmethod            
    def assets() -> None:
        """
            List the user's asset and provide some functionality to working on them
        """
        clear_screen()
        content_id = []   
        content_name = []
        data = DBManager().read('id, name', Content, f"user_id = '{LoggedUser.ID}' ")   
        for idx, row in enumerate(data, 1):
            print(idx, row[1])
            content_id.append(row[0])
            content_name.append(row[1]) 

        # If user own assets
        if content_name:
            key = input('\nID.select C.cancel >> ')    
            if key.lower() != 'c':
                try:
                    key = int(key)
                except:
                    Operations.assets()
                else:        
                    if key < 1 or key > len(content_name):
                        Operations.assets()   
                    else:
                        users_comment = DBManager().read('comment', Comment, f"id = '{content_id[key-1]}'") 
                        for c in users_comment:
                            print(c)

                        switch = input('R.remove-content >> ')

                        # Delete information from database and content from the store
                        if  switch.lower() == 'r':
                            if os.path.exists(f"store/{content_name[key-1]}"):
                                os.remove(f"store/{content_name[key-1]}")

                            DBManager().delete(Content, f'id = {content_id[key-1]}')    
                            Operations.change_balance(False)
                            logging.warning(f'Content removed from the shop: {content_name[key-1]}')

                        else:
                            Operations.assets()

    @staticmethod
    def change_balance(increase: bool = True) -> None:
        bal = DBManager().read('balance', User, f"id = '{LoggedUser.ID}'")   
        bal = int(bal[0][0]) + 1 if increase else int(bal[0][0]) - 1
        DBManager().update(User, 'balance', bal, f"id = '{LoggedUser.ID}'") 

    @staticmethod
    def shopping() -> None:
        """
            Shopping and commenting on content
        """
        # if the user balance is zero he can not do shopping
        bal = DBManager().read('balance', User, f"id = '{LoggedUser.ID}'")
        if int(bal[0][0]) < 1:
            print('Gift and get! your balance is zero write now ...')
        else:     
            # Read the content of store that the user is not its owner
            data = DBManager().read('id, name, owner, user_id', Content, f"user_id != '{LoggedUser.ID}'")
            Operations.shopping_continue(data)

    @staticmethod   
    def shopping_continue(data: list) -> None:

        # list the content on shop
        clear_screen()
        print('ID        Book Name           Owner')
        print('============================================\n')
       
        content_id = []   
        content_name = []
        user_id = []
        for row in data:
            print(f"{len(content_id)+1:<10}{row[1]:<20}{row[2]:<20}") 
            content_id.append(row[0])
            content_name.append(row[1]) 
            user_id.append(row[3])

        # If there is information then get key from user
        if content_id:
            key = input('\nID.select C.cancel >> ')
            if key.lower() != 'c':
                try:
                    key = int(key)
                except:
                    Operations.shopping_continue(data)
                else:
                    if key < 1 or key > len(content_id):
                        Operations.shopping()   
                    else:
                        users_comment = DBManager().read('comment', Comment, f"content_id = '{content_id[key-1]}'") 
                        print('\n<-- Comments on your selected content -->\n')
                        for c in users_comment:
                            print(c[0])
                        switch = input('\nC.comment B.buy >> ')
                        # Buy the content
                        if  switch.lower() == 'b':
                            if os.path.exists(f"store/{content_name[key-1]}"):
                                # Re-crypt the file
                                code = DBManager().read('code', User, f"id = '{user_id[key-1]}'")[0][0]
                                crypto_key = load_key(f'users/{code}.key')
                                decrypt(f'store/{content_name[key-1]}', crypto_key)
                                code = DBManager().read('code', User, f"id = '{LoggedUser.ID}'")[0][0] 
                                crypto_key = load_key(f'users/{code}.key')
                                encrypt(f'store/{content_name[key-1]}', crypto_key)

                                # Change the owner of content
                                DBManager().update(Content, 'user_id', f'{LoggedUser.ID}', f"id = '{content_id[key-1]}'") 
                                logging.debug(f'Owner has been changed for: {content_name[key-1]}')

                                # Decrease balance by one and update the database
                                Operations.change_balance(False)
                                logging.debug(f'Balance has been updated for: {LoggedUser.FULLNAME}')

                                print('Your shopping has been successfully\n')                            
                            else:
                                DBManager().delete(Comment, f'content_id = {content_id[key-1]}')   
                                DBManager().delete(Content, f'id = {content_id[key-1]}')    
                                logging.warning(f'Database and store was not sync for: {content_name[key-1]}')
                                print('Shop was in update process, please refresh the page\n')

                        # Comment on the content
                        elif switch.lower() == 'c':
                            clear_screen()
                            comment = input('Your comment (max 250) >> ')[:249]
                            if comment: 
                                DBManager().insert(Comment(comment, LoggedUser.ID, content_id[key-1]))
                                logging.debug(f'Comment on content id: {content_id[key-1]} by: {LoggedUser.FULLNAME}') 
                                print('Your comment has been send successfully\n')
                        else:
                            Operations.shopping_continue(data)


    