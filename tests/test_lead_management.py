from odoo.tests.common import TransactionCase

class TestLeadManagement(TransactionCase):
    def test_create_lead(self):
        lead = self.env['lead.management'].create({
            'name': 'Test Lead',
            'email': 'test@example.com',
            'phone': '1234567890',
        })
        self.assertEqual(lead.name, 'TEST LEAD')
