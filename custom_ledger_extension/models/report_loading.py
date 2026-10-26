from odoo import models


class AccountReport(models.Model):
    _inherit = 'account.report'

    def get_options(self, previous_options):
        options = super().get_options(previous_options)
        options['cle_loading_indicator'] = True
        return options
