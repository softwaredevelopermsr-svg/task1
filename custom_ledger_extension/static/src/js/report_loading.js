/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AccountReportController } from "@account_reports/components/account_report/controller";

patch(AccountReportController.prototype, {
    get cleLoadingEnabled() {
        return Boolean(this.cachedFilterOptions?.cle_loading_indicator
            || this.options?.cle_loading_indicator);
    },

    get cleReportBusy() {
        return this.cleLoadingEnabled && Boolean(
            this.clePendingDisplays || this.asyncDataLoading
        );
    },

    async displayReport(...args) {
        if (!this.cleLoadingEnabled) {
            return super.displayReport(...args);
        }
        this.clePendingDisplays = (this.clePendingDisplays || 0) + 1;
        try {
            return await super.displayReport(...args);
        } catch (error) {
            if (this.clePendingDisplays === 1) {
                this.asyncDataLoading = false;
            }
            throw error;
        } finally {
            this.clePendingDisplays = Math.max(0, this.clePendingDisplays - 1);
        }
    },

    async displayLoadingSymbolWhenTakingTooLong(...args) {
        if (this.cleLoadingEnabled) {
            return;
        }
        return super.displayLoadingSymbolWhenTakingTooLong(...args);
    },
});
