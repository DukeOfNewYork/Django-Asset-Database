from django.test import TestCase, Client
from .models import *
from .forms import *


class AssetFormTestCase(TestCase):
    def setUp(self):
        self.test_building = Building.objects.create(name="A Test Building")
        self.asset_form_pass = {'name': 'test', 'location': self.test_building.id, 'room': 'Room1', }
        self.asset_form_fail = {'name': '', 'location': 5, 'room': '', }
        User.objects.create(username='testuser')


class ComputerModelTest(AssetFormTestCase):
    def test_asset_form_pass(self):
        self.assertTrue(AssetForm(data=self.asset_form_pass).is_valid())

    def test_asset_form_fail(self):
        self.assertFalse(AssetForm(data=self.asset_form_fail).is_valid())


class AddAssetViewTest(AssetFormTestCase):
    def test_assets_view_Pass(self):
        c = Client()
        c.force_login(User.objects.get(username="testuser"))
        c.post('/add_assets/', data=self.asset_form_pass)
        test_asset = Asset.objects.get(name=self.asset_form_pass['name'])
        self.assertTrue(test_asset.name == self.asset_form_pass['name'])
        self.assertTrue(test_asset.location.id == self.asset_form_pass['location'])
        self.assertTrue(test_asset.room == self.asset_form_pass['room'])

    def test_assets_view_Fail(self):
        c = Client()
        c.force_login(User.objects.get(username="testuser"))
        with self.assertRaises(BaseException):
            Asset.objects.get(c.post('/add_assets/', data=self.asset_form_fail))
