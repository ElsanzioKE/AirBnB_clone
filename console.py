#!/usr/bin/python3
"""
contains the entry point of the command interpreter
uses cmd module
implements quit and EOF to exit the program
implements help although its defaulted we keep it updated
custom prompt (hbnb)
implements empty line and enter does nothing
it's not executed when imported but when called
"""
import cmd
import json
import models
from models.base_model import BaseModel
from models import storage
import shlex # we are parsing command-line input that includes quoted strings

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = {
            "BaseModel": BaseModel,
            # Add more class mappings as needed
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
            class_obj = self.valid_classes[class_name] # get the class object from the dictionary
            new_instance = class_obj() # instantiate a new object of the specified class
            storage.save() # save the new instance to the JSON file
            print(new_instance.id)

    def do_show(self, arg):
        """
        Shows the string representation of an instance based on the class name and id.
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

            objects = storage.all() # get all instances from storage
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found ***")

    def do_all(self, arg):
        """
        prints all string representation of all instances based or not on class name
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
