# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Lead Tag Model
class LeadTag(models.Model):
    _name = 'lead.tag'
    _description = 'Lead Tags'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color Index', default=0)
    lead_ids = fields.Many2many('lead.management', string='Associated Leads')


# Attachment Inheritance
class Attachment(models.Model):
    _inherit = 'ir.attachment'

    lead_ids = fields.Many2many('lead.management', string='Associated Leads')
    

# Lead Communication Model
class LeadCommunication(models.Model):
    _name = 'lead.communication'
    _description = 'Lead Communication'

    name = fields.Selection([
        ('contact', 'Contact'),
        ('call', 'Call'),
        ('meeting', 'Meeting')
    ], string='Communication Type', required=True)
    notes = fields.Text(string='Notes')
    meeting_date = fields.Datetime(string='Metting Date', required=True)
    meeting_link = fields.Char(string='Metting Link')
    lead_id = fields.Many2one('lead.management', string='Associated Lead')
    
    @api.model
    def create(self, vals):
        record = super(LeadCommunication, self).create(vals)

        record.lead_id.write({'meeting_date': record.meeting_date})

        return record    


# Campaign Model
class Campaign(models.Model):
    _name = 'sale.campaign'
    _description = 'Sales Campaigns'

    name = fields.Char(string='Campaign Name', required=True)
    description = fields.Text(string='Description')
    manager = fields.Many2one('res.users', string='Campaign Manager', required=True)
    lead_ids = fields.One2many('lead.management', 'campaign', string='Associated Leads', readonly=True)


# Project Scope Model
class ProjectScope(models.Model):
    _name = 'project.scope'
    _description = 'Project Scope'

    name = fields.Char(string='Scope Name', required=True)
    description = fields.Text(string='Scope Description')
    price = fields.Float(string='Price', required=True)
    lead_ids = fields.Many2many('lead.management', string='Associated Leads')

