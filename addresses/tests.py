from django.test import TestCase
from django.urls import reverse

from .models import Address, AddressConfig


class AddressModelTests(TestCase):
    def test_default_state_applied(self):
        # when there is a config object with a default state, saving an address
        # without specifying state should fill it in
        AddressConfig.objects.create(default_state="WA")
        addr = Address(street_address="123 Fake St", suburb="Peel")
        addr.save()
        self.assertEqual(addr.state, "WA")

    def test_no_config_default_empty(self):
        addr = Address(street_address="1 Main St", suburb="Metro")
        addr.save()
        self.assertEqual(addr.state, "")


class AddressListViewTests(TestCase):
    def setUp(self):
        # create some addresses with specific created_at ordering using save()
        Address.objects.create(street_address="1 A St", suburb="Alpha", state="NSW")
        Address.objects.create(street_address="2 B St", suburb="Beta", state="VIC")
        Address.objects.create(street_address="3 C St", suburb="Gamma", state="QLD")

    def test_default_sort_is_date_descending(self):
        resp = self.client.get(reverse("address_list"))
        self.assertEqual(resp.status_code, 200)
        addresses = list(resp.context["addresses"])
        # last created should appear first
        self.assertEqual(addresses[0].street_address, "3 C St")
        self.assertEqual(addresses[-1].street_address, "1 A St")

    def test_sort_by_suburb(self):
        resp = self.client.get(reverse("address_list") + "?sort=suburb")
        self.assertEqual(resp.status_code, 200)
        addresses = list(resp.context["addresses"])
        self.assertEqual(addresses[0].suburb, "Alpha")
        self.assertEqual(addresses[-1].suburb, "Gamma")

    def test_template_displays_rows(self):
        resp = self.client.get(reverse("address_list"))
        content = resp.content.decode()
        self.assertIn("1 A St", content)
        self.assertIn("Alpha", content)
        self.assertIn("3 C St", content)

    def test_can_add_address_via_post(self):
        data = {"street_address": "9 New Rd", "suburb": "Newtown", "state": "WA"}
        resp = self.client.post(reverse("address_list"), data)
        # should redirect back
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Address.objects.filter(street_address="9 New Rd").exists())

    def test_form_prefills_default_state(self):
        AddressConfig.objects.create(default_state="TAS")
        resp = self.client.get(reverse("address_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('value="TAS"', resp.content.decode())

    def test_can_delete_address_via_post(self):
        addr = Address.objects.create(
            street_address="33 To Delete", suburb="Gone", state="VIC"
        )
        resp = self.client.post(reverse("address_delete", args=[addr.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Address.objects.filter(pk=addr.pk).exists())
