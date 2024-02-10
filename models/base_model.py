#!/usr/bin/python3
        
"""
defines all common attributes and methods for other classes:
    1. public attributes:
        id: assign with uuid when instance is
        created to always have a unique id
        created _at: assign using datetime
        updated_at: assign using datetime
    2. __str__: should prnt clsnam id dict
    3. public methods:
        save: updates the updated_at with datetime
        to_dict: returns a dictionary containing all keys/values
        of __dict__ of the instance:
            use self.__dict__ only attributes are returned
            key __class__ must be added to the dict
            with classneme of the object
            created_at and updated_at must be
            converted to a string in ISO format:
            the method will be the first piece of serialization
"""

from datetime import datetime as dt
import uuid
import models
from models import storage


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        BaseModel constructor
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = dt.utcnow()
        self.updated_at = dt.utcnow()

        # check if kwargs is not None and not empty
        if kwargs is not None and kwargs != {}:
            # iterate through key-value pairs in kwargs
            for key, value in kwargs.items():
                # skip setting __class__ attribute
                if key == "__class__":
                    continue
                # Convert created_at and updated_at strings to datetime objects
                elif key == "created_at" or key == "updated_at":
                   value = dt.fromisoformat(value) 
                
                else:
                    # set other attributes
                    setattr(self, key, value)
        
        models.storage.new(self)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime.
        B
        """
        self.updated_at = dt.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance.

        Returns:
            dict: Dictionary representation of the instance.
        """
        dictionary = {**self.__dict__}
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation of the instance.
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"

