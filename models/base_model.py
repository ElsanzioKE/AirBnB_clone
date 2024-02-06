#!/usr/bin/python3
import uuid
from datetime import datetime as dt

class BaseModel:
    """Base class representing a model with a unique identifier, creation time, and last update time.

    Attributes:
        id (str): Unique identifier generated using uuid.uuid4().
        created_at (datetime): Date and time when the instance is created.
        updated_at (datetime): Date and time when the instance is last updated.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        # check if kwargs is not None and not empty
        if kwargs is not None and kwargs != {}:
            # iterate through key-value pairs in kwargs
            for key, value in kwargs.items():
                # skip setting __class__ attribute
                if key == "__class__":
                    continue
                # Convert created_at and updated_at strings to datetime objects
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    # set other attributes
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = dt.now()
            self.updated_at = dt.now()

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime.
        """
        self.updated_at = dt.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance.

        Returns:
            dict: Dictionary representation of the instance.
        """
        class_name = self.__class__.__name__
        formatted_created_at = self.created_at.isoformat()
        formatted_updated_at = self.updated_at.isoformat()

        return {
            **self.__dict__,
            "__class__": class_name,
            "created_at": formatted_created_at,
            "updated_at": formatted_updated_at
        }

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: String representation of the instance.
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"

