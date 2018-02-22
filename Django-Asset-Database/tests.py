from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .forms import *


# Create your tests here.

class AssetFormTestCase(TestCase):
    def setUp(self):
        self.testbuilding = Building.objects.create(name="A Test Building")
        self.assetformpass = {'name': 'test', 'location': self.testbuilding.id, 'room': 'Room1', }
        self.assetformfail = {'name': '', 'location': 5, 'room': '', }
        User.objects.create(username='testuser')


class ComputerModelTest(AssetFormTestCase):
    def test_asset_form_pass(self):
        self.assertTrue(AssetForm(data=self.assetformpass).is_valid())

    def test_asset_form_fail(self):
        self.assertFalse(AssetForm(data=self.assetformfail).is_valid())

    def test_assets_view_Pass(self):
        c = Client()
        c.force_login(User.objects.get(username="testuser"))
        c.post('/add_assets/', data=self.assetformpass)
        self.assertTrue(Asset.objects.get(name=self.assetformpass['name']))

    def test_assets_view_Fail(self):
        c = Client()
        c.force_login(User.objects.get(username="testuser"))
        with self.assertRaises(BaseException):
            Asset.objects.get(c.post('/add_assets/', data=self.assetformfail))
