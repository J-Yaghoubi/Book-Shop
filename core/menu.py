import os
import sys

class Color:
    HEADER = 0
    MENU = 0
    SHELL = 0
    INTERFACE = 0

class Menu:
    """
    A class to create a menu.

    Attributes
    ----------
    header : str
        text that print on head of program
    divider : str
        character that divide the index number from menu-title
    shell : str
        character that represent that program is waiting for key

    Methods
    -------
    add(sub_menu):
        Get the tuple and save it as new defined route   

    exit:
        Close the program and end the program

    select:
        Get a sub_menu title and set the cursor on this route and 
        make it current route

    next:
        Select next route as a current route

    back:
        Select previous route as a current route

    execute:
        run the program and print list of options in the current route
    """

    def __init__(self, header: str = None, divider: str = '.', shell: str = '>>') -> None:
        self.header = header
        self.shell = shell
        self.divider = divider
        self.cursor = 0
        self.sub = []
        self.key = 0
        self.c_header = u"\u001b[38;5;" + str(Color.HEADER) + "m "
        self.c_menu = u"\u001b[38;5;" + str(Color.MENU) + "m " 
        self.c_shell = u"\u001b[38;5;" + str(Color.SHELL) + "m " 
        self.c_interface = u"\u001b[38;5;" + str(Color.INTERFACE) + "m "    

    def _refresh_screen(self) -> None:
        """Clear screen"""
        os.system('clear') if os.name == 'posix' else os.system('cls')

    def _key_await(self, any=False) -> int:
        """
        Await for receiving user selection keyboard

        Parameters
        ----------
        any : boolean
            it will await for all keys of 'any' sets to true
        """

        print(self.c_shell)

        if any:
            print('Press any key...')
            return input(self.shell + ' ' + self.c_interface)
        try:
            key = int(input(self.shell + ' ' + self.c_interface))
        except:
            self._refresh_screen()
            self._show_menus()
            return self._key_await()
        else:
            return key - 1

    def _show_menus(self) -> None:
        """
        A protect method for using with internal methods
        The functionality of this method is clearing the screen and printing the menu list
        """
        self._refresh_screen()
        print(self.c_header + self.header, '\n') if self.header else None

        order = 1
        for m in self.sub[self.cursor][1]:
            print(self.c_menu + str(order) + self.divider, m[0])
            order += 1

    def select(self, route: str) -> None:
        """
        Set menu cursor on preferred route

        Parameters
        ----------
        route : str
            it will search the input str in menu routes and set cursor on requested route
        """
        for cur in self.sub:
            if cur[0] == route:
                self.cursor = self.sub.index(cur)
                break

    def next(self) -> None:
        """Select next route if exists"""
        if self.cursor < len(self.cursor) - 1: self.cursor += 1
        self.execute()

    def back(self) -> None:
        """Select previous route if exists"""
        if self.cursor > 0: self.cursor -= 1
        self.execute()

    def exit(self) -> None:
        """Exit from program"""
        sys.exit()

    def add(self, sub_menu: tuple) -> None:
        """Define new route"""
        self.sub.append(sub_menu)

    @property
    def current_title(self):
        return self.sub[self.cursor][1][self.key][0]

    @property
    def current_function(self):
        return self.sub[self.cursor][1][self.key][1]

    def execute(self) -> None:
        """
        Execute the menu

        """
        self._show_menus()
        self.key = self._key_await()

        if self.key > len(self.sub[self.cursor][1])-1 or self.key < 0:
            self.execute()
        else:
            if isinstance(self.current_function, str):
                self.select(self.current_function)
                self.execute()
            else:
                self._refresh_screen()
                print(f'{self.current_title}\n')
                situation = self.current_function()
                if situation:
                    self.select(situation)
                self._key_await(any=True)
                self.execute()
