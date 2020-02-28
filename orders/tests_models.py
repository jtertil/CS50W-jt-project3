import unittest

from django.db.utils import DataError
from django.test import TestCase

from orders.models import Size, Extra, Type, Item, User


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


class ItemTest(TestCase):
    def setUp(self) -> None:

        Type.objects.create(name='test_type')
        Size.objects.create(name='test_size')

        for num in range(1, 11):
            Extra.objects.create(name=f'test_extra_{num}')

        self.name_valid = 'i' * Item._meta.get_field('name').max_length
        self.name_toolong = self.name_valid + 'i'
        self.type_valid = Type.objects.filter(name='test_type').first()
        self.type_as_string = 'type_as_string'
        self.size_valid = Size.objects.filter(name='test_size').first()
        self.size_as_string = 'size_as_string'
        self.extras_price_valid = '0.5'
        self.extras_price_negative = '-1'
        self.base_price_valid = '12.7'
        self.base_price_negative = '-100'

        self.default_extras_price = Item._meta.get_field(
            'extras_price').default
        self.default_is_special = Item._meta.get_field(
            'is_special').default
        self.default_extras_max_quantity = Item._meta.get_field(
            'extras_max_quantity').default

    def test_create_item_with_valid_data(self):
        i = Item.objects.create(
            name=self.name_valid,
            type=self.type_valid,
            size=self.size_valid,
            base_price=self.base_price_valid
        )

        self.assertTrue(isinstance(i, Item))
        self.assertEqual(
            i.__str__(), f'{self.name_valid} - {self.base_price_valid}$')
        self.assertEqual(i.name, self.name_valid)
        self.assertEqual(i.type, self.type_valid)
        self.assertEqual(i.size, self.size_valid)
        self.assertEqual(i.extras_price, self.default_extras_price)
        self.assertEqual(i.is_special, self.default_is_special)
        self.assertEqual(
            i.extras_max_quantity, self.default_extras_max_quantity)

    def test_create_item_with_valid_data_add_extras(self):
        i = Item.objects.create(
            name=self.name_valid,
            type=self.type_valid,
            size=self.size_valid,
            base_price=self.base_price_valid
        )

        all_extra_obj = Extra.objects.all()
        i.extras_available.set(all_extra_obj)

        self.assertEqual(all_extra_obj.count(), i.extras_available.count())

    def test_create_item_with_invalid_type(self):
        i = Item.objects.create
        self.assertRaises(ValueError, i,
                          name=self.name_valid,
                          type=self.type_as_string,
                          size=self.size_valid,
                          base_price=self.base_price_valid
                          )

    def test_create_item_with_invalid_size(self):
        i = Item.objects.create
        self.assertRaises(ValueError, i,
                          name=self.name_valid,
                          type=self.type_valid,
                          size=self.size_as_string,
                          base_price=self.base_price_valid
                          )

    def test_create_item_with_invalid_base_price(self):
        i = Item.objects.create
        self.assertRaises(ValueError, i,
                          name=self.name_valid,
                          type=self.type_valid,
                          size=self.size_valid,
                          base_price=self.base_price_negative
                          )

    def test_create_item_with_invalid_extras_price(self):
        i = Item.objects.create
        self.assertRaises(ValueError, i,
                          name=self.name_valid,
                          type=self.type_valid,
                          size=self.size_valid,
                          base_price=self.base_price_valid,
                          extras_price=self.extras_price_negative
                          )


class BasketTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='test_user',
            password='idontcare!',
            email='test_user@email.com',
            first_name='Fist_name',
            last_name='Last_name'
        )

        Type.objects.create(name='test_type')
        Size.objects.create(name='test_size')

        for num in range(1, 11):
            Extra.objects.create(name=f'test_extra_{num}')

        name = 'test_item_name'
        type = Type.objects.first()
        size = Size.objects.first()
        extras_available = Extra.objects.all()[:4]
        extras_price = 0.5
        is_special = True
        extras_max_quantity = 2
        base_price = 10

        Item.objejects.create(
            name=name,
            type=type,
            size=size,
            extras_available=extras_available,
            extras_price=extras_price,
            is_special=is_special,
            extras_max_quantity=extras_max_quantity,
            base_price=base_price
        )


        self.name_valid = 'i' * Item._meta.get_field('name').max_length
        self.name_toolong = self.name_valid + 'i'
        self.type_valid = Type.objects.filter(name='test_type').first()
        self.type_as_string = 'type_as_string'
        self.size_valid = Size.objects.filter(name='test_size').first()
        self.size_as_string = 'size_as_string'
        self.extras_price_valid = '0.5'
        self.extras_price_negative = '-1'
        self.base_price_valid = '12.7'
        self.base_price_negative = '-100'

        self.default_extras_price = Item._meta.get_field(
            'extras_price').default
        self.default_is_special = Item._meta.get_field(
            'is_special').default
        self.default_extras_max_quantity = Item._meta.get_field(
            'extras_max_quantity').default
