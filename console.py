\\\\\\\\\\\\#!/usr/bin/python3
"""
contains the entry point of the command interpreter
uses cmd module
implements quit and EOF to exit the program
implements help although its defaulted we keep it updated
custom prompt (hbnb)
implements empty line and enter does nothing
it's not executed when imported but when called
"""
import ast
import cmd
import json
import models
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import re
import shlex  # we are parsing command-line input that includes quoted strings


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Amenity": Amenity,
            "State": State,
            "Review": Review,
            "Place": Place,
            "City": City,
            }

    def do_quit(self, arg):
        """
        implements quit to exit the program
        """
        return True

    def emptyline(self):
        """
        do nothing on emptyline and enter
        """
        pass

    def do_EOF(self, arg):
        """
        implement EOF to exit the program
        """
        print()
        return True

    def help_quit(self):
        """Help message for the quit command"""
        print("Quit command to exit the program")
        print()

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        prints the id. Ex: $ create BaseModel
        """
        commands = shlex.split(arg)
        class_name = commands[0]
        if len(commands) == 0:
            print("** class name missing **")
        elif class_name not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            class_obj = self.valid_classes[class_name]  # get class from dict
            new_instance = class_obj()  # instantiate new obj of specified cls
            storage.save()  # save the new instance to the JSON file
            print(new_instance.id)

    def do_show(self, arg):
        """
        Shows the string representation of an
        instance based on the class name and id.
        """
        commands = shlex.split(arg)
        class_name = commands[0]
        if len(commands) == 0:
            print("** class name missing **")
        elif class_name not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            # construct the key for the instance
            instance_id = commands[1]
            key = "{}.{}".format(class_name, instance_id)

            objects = storage.all()  # get all instances from storage
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found ***")

    def do_all(self, arg):
        """
        prints all string representation of all
        instances based or not on class name
        """
        objects = storage.all()
        commands = shlex.split(arg)
        if len(commands) == 0:
            # if no arguments, print string rep of all instances
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            # if a valid classis provided as an argument
            for key, value in objects.items():
                # check if the instance belongs to the specifies class
                if key.split('.')[0] == commands[0]:
                    # if it belongs to the specified class
                    print(str(value))

    def do_destroy(self, arg):
        """
        deletes an instance based on the class name and id save to json file
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_update(self, arg):
        """
        updates an instance based on classname and id
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)

                if curly_braces:
                    try:
                        str_data = curly_braces.group(1)
                        arg_dict = ast.literal_eval("{" + str_data + "}")

                        attribute_names = list(arg_dict.keys())
                        attribute_values = list(arg_dict.values())
                        try:
                            attr_name1 = attribute_names[0]
                            attr_value1 = attribute_values[0]
                            setattr(obj, attr_name1, attr_value1)
                        except Exception:
                            pass
                        try:
                            attr_name2 = attribute_names[1]
                            attr_value2 = attribute_values[1]
                            setattr(obj, attr_name2, attr_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    attr_name = commands[2]
                    attr_value = commands[3]

                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)

                obj.save()
    def default(self, arg):
        """
        Default behavior for cmd module when input is invalid
        """
        arg_list = arg.split('.')

        cls_nm = arg_list[0]  # incoming class name

        command = arg_list[1].split('(')

        cmd_met = command[0]  # incoming command method

        e_arg = command[1].split(')')[0]  # extra arguments

        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }

        if cmd_met in method_dict.keys():
            if cmd_met != "update":
                return method_dict[cmd_met]("{} {}".format(cls_nm, e_arg))
            else:
                if not cls_nm:
                    print("** class name missing **")
                    return
                try:
                    obj_id, arg_dict = split_curly_braces(e_arg)
                except Exception:
                    pass
                try:
                    call = method_dict[cmd_met]
                    return call("{} {} {}".format(cls_nm, obj_id, arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(arg))
            return False

if __name__ == "__main__":
    HBNBCommand().cmdloop()
