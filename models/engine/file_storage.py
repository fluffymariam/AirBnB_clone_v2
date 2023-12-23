import json
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        if cls:
            filtered_objects = {}
            for key, value in self.__objects.items():
                class_name, obj_id = key.split('.')
                if class_name == cls.__name__:
                    filtered_objects[key] = value
            return filtered_objects
        else:
            return self.__objects

    def new(self, obj):
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        serialized_objects = {
                key: value.to_dict()
                for key, value in self.__objects.items()
            }
        with open(self.__file_path, 'w', encoding="UTF-8") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as file:
                objects_data = json.load(file)
                for key, value in objects_data.items():
                    obj = eval(value["__class__"])(**value)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            del self.__objects[key]

    def close(self):
        self.reload()
