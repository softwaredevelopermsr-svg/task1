/** @odoo-module **/

import { AnalyticDistribution } from "@analytic/components/analytic_distribution/analytic_distribution";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { formatPercentage } from "@web/views/fields/formatters";
import { _t } from "@web/core/l10n/translation";

patch(AnalyticDistribution.prototype, {
    setup() {
        super.setup(...arguments);
        this.cleAnalyticAction = useService("action");
    },

    planSummaryTags() {
        if (this.props.record.resModel !== "account.move.line") {
            return super.planSummaryTags(...arguments);
        }
        return Object.values(this.accountTotalsByPlan()).flatMap((planSummary) =>
            Object.values(planSummary).map((account) => ({
                id: String(account.planId) + "_" + String(account.accId),
                text: this.planIsComplete(account.total)
                    ? account.accName
                    : formatPercentage(account.total) + " " + account.accName,
                colorIndex: account.planColor,
                canEdit: true,
                title: _t("Open analytic account: %s", account.accName),
                onClick: (ev) => this.cleOpenAnalyticAccount(ev, account.accId),
            }))
        );
    },

    async cleOpenAnalyticAccount(ev, accountId) {
        ev.preventDefault();
        ev.stopPropagation();
        if (!Number.isInteger(accountId) || accountId <= 0) {
            return;
        }
        return this.cleAnalyticAction.doAction({
            type: "ir.actions.act_window",
            name: _t("Analytic Account"),
            res_model: "account.analytic.account",
            res_id: accountId,
            views: [[false, "form"]],
            target: "new",
        });
    },
});
