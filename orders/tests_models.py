import unittest

from django.db.utils import DataError
from django.test import TestCase

from orders.models import Size, Extra, Type, Item


class SizeTest(TestCase):

    name_valid = 's' * Size._meta.get_field('name').max_length
    name_toolong = name_valid + 's'

    def test_create_size_with_valid_name(self):
        s = Size.objects.create(name=self.name_valid)
        self.assertTrue(isinstance(s, Size))
        self.assertEqual(s.__str__(), self.name_valid)

    def test_create_size_with_invalid_name(self):
        s = Size.objects.create
        self.assertRaises(DataError, s, name=self.name_toolong)


class ExtraTest(TestCase):

    name_valid = 'e' * Extra._meta.get_field('name').max_length
    name_toolong = name_valid + 'e'

    def test_create_extra_with_valid_name(self):
        e = Extra.objects.create(name=self.name_valid)
        self.assertTrue(isinstance(e, Extra))
        self.assertEqual(e.__str__(), self.name_valid)

    def test_create_extra_with_invalid_name(self):
        e = Size.objects.create
        self.assertRaises(DataError, e, name=self.name_toolong)


class TypeTest(TestCase):
    name_valid = 't' * Type._meta.get_field('name').max_length
    name_toolong = name_valid + 't'
    description_blank = ''
    description_valid = 't' * Type._meta.get_field('description').max_length
    description_toolong = description_valid + 't'
    extras_name_blank = ''
    extras_name_valid = 'e' * Type._meta.get_field('extras_name').max_length
    extras_name_toolong = description_valid + 'e'

    def test_create_type_with_valid_data(self):
        t = Type.objects.create(
            name=self.name_valid,
            description=self.description_valid,
            extras_name=self.extras_name_valid
        )
        self.assertTrue(isinstance(t, Type))
        self.assertEqual(t.__str__(), self.name_valid)
        self.assertEqual(t.description, self.description_valid)
        self.assertEqual(t.extras_name, self.extras_name_valid)

    def test_create_type_with_valid_name_and_blank_desc_and_exn(self):
        t = Type.objects.create(
            name=self.name_valid,
            description=self.description_blank,
            extras_name=self.extras_name_blank
        )
        self.assertTrue(isinstance(t, Type))
        self.assertEqual(t.__str__(), self.name_valid)
        self.assertEqual(t.description, self.description_blank)
        self.assertEqual(t.extras_name, self.extras_name_blank)

    def test_create_type_with_invalid_name(self):
        t = Type.objects.create
        self.assertRaises(DataError, t,
                          name=self.name_toolong,
                          description=self.description_valid,
                          extras_name=self.extras_name_valid
                          )

    def test_create_type_with_invalid_desc(self):
        t = Type.objects.create
        self.assertRaises(DataError, t,
                          name=self.name_valid,
                          description=self.description_toolong,
                          extras_name=self.extras_name_valid
                          )

    def test_create_type_with_invalid_exn(self):
        t = Type.objects.create
        self.assertRaises(DataError, t,
                          name=self.name_valid,
                          description=self.description_valid,
                          extras_name=self.extras_name_toolong
                          )

