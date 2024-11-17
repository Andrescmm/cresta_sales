# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response


class Leads(http.Controller):
    @http.route('/api/create_lead', type='json', auth='public')
    def create_lead(self, **kwargs):
        data = json.loads(request.httprequest.data)
        lead_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
        }
        lead = request.env['lead.management'].sudo().create(lead_data)
        if lead:
            return {'status': 'success'}
        else:
            return {'status': 'failed'}