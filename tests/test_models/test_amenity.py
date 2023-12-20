import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import pycodestyle
from os import getenv
from models.amenity import Amenity
from models.base_model import BaseModel

storage_type = getenv("HBNB_TYPE_STORAGE")


class TestAmenityBase(unittest.TestCase):
    def setUp(self):
        self.amenity = Amenity()

    def test_name_is_string(self):
        self.assertIsInstance(self.amenity.name, str)


class TestPEP8(unittest.TestCase):
    def test_pep8(self):
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors.")


class TestAmenityInheritsBaseModel(unittest.TestCase):
    def test_instance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, Amenity)
        self.assertTrue(issubclass(type(amenity), BaseModel))
        self.assertEqual(str(type(amenity)),
                         "<class 'models.amenity.Amenity'>")


class TestAmenityMethods(unittest.TestCase):
    def setUp(self):
        self.amenity = Amenity()
        self.amenity.name = "Barbie"

    def test_dict_method(self):
        expected_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str
        }
        instance_dict = self.amenity.to_dict()
        expected_dict_attrs = ["id", "created_at",
                               "updated_at", "name", "__class__"]

        self.assertCountEqual(instance_dict.keys(), expected_dict_attrs)
        self.assertEqual(instance_dict['name'], 'Barbie')
        self.assertEqual(instance_dict['__class__'], 'Amenity')

        for attr, types in expected_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, self.amenity.__dict__)
                self.assertIs(type(self.amenity.__dict__[attr]), types)
        self.assertEqual(self.amenity.name, "Barbie")

    def test_user_id_and_created_at(self):
        amenity_1 = Amenity()
        sleep(2)
        amenity_2 = Amenity()
        sleep(2)
        amenity_3 = Amenity()
        sleep(2)
        amenities = [amenity_1, amenity_2, amenity_3]

        for instance in amenities:
            self.assertIs(type(instance.id), str)

        self.assertNotEqual(amenity_1.id, amenity_2.id)
        self.assertNotEqual(amenity_1.id, amenity_3.id)
        self.assertNotEqual(amenity_2.id, amenity_3.id)

        self.assertTrue(amenity_1.created_at <= amenity_2.created_at)
        self.assertTrue(amenity_2.created_at <= amenity_3.created_at)
        self.assertNotEqual(amenity_1.created_at, amenity_2.created_at)
        self.assertNotEqual(amenity_1.created_at, amenity_3.created_at)
        self.assertNotEqual(amenity_3.created_at, amenity_2.created_at)

    def test_str_method(self):
        amenity = Amenity()
        str_output = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(str_output, str(amenity))

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        instance = Amenity()
        created_at = instance.created_at
        sleep(2)
        updated_at = instance.updated_at
        instance.save()
        new_created_at = instance.created_at
        sleep(2)
        new_updated_at = instance.updated_at

        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


class TestAmenityClass(unittest.TestCase):
    def test_is_subclass(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        expected_value = None if storage_type == 'db' else ""
        self.assertEqual(amenity.name, expected_value)

    def test_to_dict_creates_dict(self):
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in am.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], am.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], am.updated_at.strftime(t_format))

    def test_str_method(self):
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))
