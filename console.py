#!/usr/bin/python3
"""
    contains the entry point for the cmd
    """
import cmd

class HBNBCommand(cmd.Cmd):
    """
    command interpreter should implement:
    EOF andquit the program
    help(this action is provided by default by cmd but you
    """
    intro = ""
    prompt = "(hbnb)"

    def do_quit(self, args):
        """Quits command to exit the program"""
        return True

    def do_EOF(self, args):
        """Quit command to exit the program"""
        return True

if __name__ == '__main__':
       HBNBCommand().cmdloop()
