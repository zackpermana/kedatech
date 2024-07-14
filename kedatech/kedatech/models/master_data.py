# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.exceptions import AccessError, UserError, ValidationError

class MasterData(models.Model):
    _name = "master.product"
    _description = "Master Data Product"

    name = fields.Char(string='Material Name', required=True)
    code = fields.Char(string='Material Code', required=True)
    type = fields.Selection([('fabric','Fabric'),('jeans','Jeans'),('cotton','Cotton')], string="Material Type", required=True)
    buy_price = fields.Float(string='Buying Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, tracking=True, help="You can find a vendor by its Name, TIN, Email or Internal Reference.")


    @api.model
    def create(self, vals):
        if vals['buy_price'] < 100:
            raise UserError(_('You cannot set buy Price less than 100'))
        
        product_id = self.search([('code','=', vals['code'])])
        if product_id:
            raise UserError(_('Code Product has been used to %s' % product_id.name))
        res = super(MasterData, self).create(vals)
        return res


    