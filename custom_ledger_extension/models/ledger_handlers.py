import json

from odoo import models
from odoo.tools import SQL


REFERENCE_FIELDS = {
    'cle_bill_number': 'name',
    'cle_supplier_reference': 'ref',
    'cle_our_reference': 'x_studio_po_number',
}


def enrich_results(env, results, current_groupby, detail_groupby):
    """Populate references in one ORM batch, respecting record access rules.

    Group totals and synthetic opening balances must never display an arbitrary
    document reference. Return the original engine structure unchanged.
    """
    entries = results if isinstance(results, list) else [(None, results)]
    ids_by_key = {}
    for key, values in entries:
        values.update({label: None for label in REFERENCE_FIELDS})
        if current_groupby != detail_groupby:
            continue
        if detail_groupby == 'id_with_accumulated_balance':
            if not isinstance(key, str) or key.startswith('balance_line_'):
                continue
            aml_id = json.loads(key)[1]
        else:
            aml_id = key
        if aml_id:
            ids_by_key[key] = aml_id
    records = env['account.move.line'].browse(list(set(ids_by_key.values()))).exists()
    moves_by_aml = {record.id: record.move_id for record in records}
    records.move_id.fetch(list(REFERENCE_FIELDS.values()))
    for key, values in entries:
        move = moves_by_aml.get(ids_by_key.get(key))
        if move:
            values.update({label: move[field] or None for label, field in REFERENCE_FIELDS.items()})
    return results



class PartnerLedgerHandler(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _get_additional_column_aml_values(self):
        return SQL(
            '%s account_move.name AS cle_bill_number, '
            'account_move.ref AS cle_supplier_reference, '
            'account_move.x_studio_po_number AS cle_our_reference,',
            super()._get_additional_column_aml_values(),
        )


class GeneralLedgerHandler(models.AbstractModel):
    _inherit = 'account.general.ledger.report.handler'

    def _report_custom_engine_general_ledger(
        self, expressions, options, date_scope, current_groupby, next_groupby,
        offset=0, limit=None, warnings=None,
    ):
        results = super()._report_custom_engine_general_ledger(
            expressions, options, date_scope, current_groupby, next_groupby,
            offset=offset, limit=limit, warnings=warnings,
        )
        return enrich_results(self.env, results, current_groupby, 'id_with_accumulated_balance')


class AgedPartnerBalanceHandler(models.AbstractModel):
    _inherit = 'account.aged.partner.balance.report.handler'

    def _aged_partner_report_custom_engine_common(
        self, options, internal_type, current_groupby, next_groupby, offset=0, limit=None,
    ):
        results = super()._aged_partner_report_custom_engine_common(
            options, internal_type, current_groupby, next_groupby,
            offset=offset, limit=limit,
        )
        return enrich_results(self.env, results, current_groupby, 'id')

    def _prepare_partner_values(self):
        values = super()._prepare_partner_values()
        values.update({label: None for label in REFERENCE_FIELDS})
        return values
