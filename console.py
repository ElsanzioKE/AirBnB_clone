#!/usr/bin/python3
"""This module imports cmd """
import cmd
class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(hbnb)"

    def do_quit(self, arg):
        """Quit command to exit program"""
        return True

    def do_EOF(self, arg):
        """Exit the program with EOF"""
        print("")
        return True

    if __name__ == '__main:__':
        HBNBCommand().cmdloop()
