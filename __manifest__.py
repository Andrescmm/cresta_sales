# -*- coding: utf-8 -*-
{
    'name': "Cresta Sales",

    'summary': """
        Module for sales process. That can facilitate the sales process in a company.""",

    'description': """
        Module for sales process. That can facilitate the sales process in a company.
    """,

    'author': "Andres Cusirramos",
    'website': "http://www.yourcompany.com",
    'category': 'Sales',
    'version': '1.0.1',
    'depends': ['base', 'web'],
    'images': ['static/src/img/cresta.png'],

    'data': [
        'security/ir.model.access.csv',
        'security/lead_management_security.xml',
        'data/sequence_data.xml',
        'report/quotation_report.xml',
        'report/contract_report.xml',
        'report/ir_actions_report.xml',
        'report/invoice_report.xml',
        'views/lead_views.xml',
        'views/campaign_views.xml',
        'views/project_views.xml',
        'views/task_views.xml',
        'views/project_scope_views.xml',
        'views/communication_views.xml',
        'views/quotation_views.xml',
        'views/invoice_views.xml',
        'views/menu_items.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
    "installable": True,
    "application": True,
}