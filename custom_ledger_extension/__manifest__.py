{
    'name': 'Custom Ledger Extension',
    'version': '19.0',
    'category': 'Accounting/Accounting',
    'summary': 'Bill Number, Supplier Reference and Our Reference on accounting reports, Analytics Hyperlink, Accounts report L',
    'author': 'SARANG T',
    'license': 'LGPL-3',
    'depends': ['account_reports', 'analytic'],
    'data': ['data/report_columns.xml'],
    'assets': {
        'web.assets_backend': [
            'custom_ledger_extension/static/src/js/analytic_distribution_links.js',
            'custom_ledger_extension/static/src/js/report_loading.js',
            'custom_ledger_extension/static/src/xml/report_loading.xml',
            'custom_ledger_extension/static/src/scss/report_loading.scss',
        ],
    },
    'installable': True,
    'application': False,
}
