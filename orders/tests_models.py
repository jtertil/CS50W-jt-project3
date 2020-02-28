from unittest import skip

from django.db.utils import DataError
from django.test import TestCase

from orders.models import Size, Extra, Type, Item, User, Basket


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

        self.assertIsInstance(i, Item)
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

        i = Item.objects.create(
            name='test_item_name',
            type=Type.objects.first(),
            size=Size.objects.first(),
            extras_price=0.5,
            is_special=True,
            extras_max_quantity=2,
            base_price=10
        )

        i.extras_available.set(Extra.objects.all()[:4])

        self.user = User.objects.first()
        self.item = Item.objects.first()
        self.extras_selected_valid = Extra.objects.all()[:3]
        self.extras_selected_too_much = Extra.objects.all()
        self.extras_selected_not_available = Extra.objects.all()[5:7]

        self.special_info_valid = 'i' * Basket._meta.get_field(
            'special_info').max_length
        self.special_info_toolong = self.special_info_valid + 'i'
        self.price_valid = '11'
        self.price_negative = '-11'

    def test_create_basket_with_valid_data(self):
        b = Basket.objects.create(
            user=self.user,
            item=self.item,
            special_info=self.special_info_valid,
            price=self.price_valid
        )

        self.assertIsInstance(b, Basket)
        self.assertEqual(
            b.__str__(), f'{self.item.name} - {self.price_valid}$')
        self.assertEqual(b.user, self.user)
        self.assertEqual(b.item, self.item)
        self.assertEqual(b.special_info, self.special_info_valid)

    def test_create_basket_with_valid_data_add_extras(self):
        b = Basket.objects.create(
            user=self.user,
            item=self.item,
            special_info=self.special_info_valid,
            price=self.price_valid
        )
        b.extras_selected.set(self.extras_selected_valid)

        self.assertEqual(
            b.extras_selected.count(), self.extras_selected_valid.count())

    def test_create_basket_with_valid_data_add_extras_too_much(self):
        b = Basket.objects.create(
            user=self.user,
            item=self.item,
            special_info=self.special_info_valid,
            price=self.price_valid
        )
        b.extras_selected.set(self.extras_selected_too_much)

        self.assertRaises(ValueError, b.save)

    def test_create_basket_with_valid_data_add_extras_not_available(self):
        b = Basket.objects.create(
            user=self.user,
            item=self.item,
            special_info=self.special_info_valid,
            price=self.price_valid
        )
        b.extras_selected.set(self.extras_selected_not_available)

        self.assertRaises(ValueError, b.save)

    def test_create_basket_with_invalid_special_info(self):
        b = Basket.objects.create

        self.assertRaises(DataError, b,
                          user=self.user,
                          item=self.item,
                          special_info=self.special_info_toolong,
                          price=self.price_valid
                          )

    def test_create_basket_with_invalid_price(self):
        b = Basket.objects.create
        self.assertRaises(ValueError, b,
                          user=self.user,
                          item=self.item,
                          special_info=self.special_info_valid,
                          price=self.price_negative
                          )

    def test_basket_as_dict(self):
        b = Basket.objects.create(
            user=self.user,
            item=self.item,
            special_info=self.special_info_valid,
            price=self.price_valid
        )
        b.extras_selected.set(self.extras_selected_valid)
        d = b.as_dict()

        self.assertIsInstance(d, dict)
        self.assertEqual(d['id'], b.pk)
        self.assertEqual(d['item'], self.item.name)
        self.assertEqual(d['extras_name'], self.item.type.extras_name)
        self.assertEqual(
            d['extras_selected'], [e.name for e in self.extras_selected_valid])
        self.assertEqual(d['special_info'], self.special_info_valid)
        self.assertEqual(d['price'], self.price_valid)

