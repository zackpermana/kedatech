# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'KedaTech',
    'version' : '1.1',
    'summary': 'Master Data KedaTech',
    'description': """
        This module for KedaTech Master Data
    """,
    'category': '',
    'website': '',
    'depends' : ['base_setup', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/master_data_views.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
