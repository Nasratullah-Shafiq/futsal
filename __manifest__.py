# poultry_farm_management/__manifest__.py
{
    'name': 'Futsal Management System',
    'version': '17.0.1.0.0',
    'category': 'Sports',
    'sequence': -20,
    'summary': 'Internal futsal field booking and match management system',
    'description': """
    Futsal Management System (Odoo 17)
    This module is designed for managing internal futsal operations including field scheduling, match organization, and customer reservations.

    Key Features:
    ------------------------------------------------
    - Futsal field management
    - Time slot reservation system
    - Weekly availability tracking (busy/free slots)
    - Match scheduling and organization
    - Player and team management (optional extension)
    - Booking confirmation and conflict prevention
    - Internal management dashboard (future extension)

    This system is intended for internal management of futsal/gymnasium operations rather than public booking services.
    """,
    'author': 'Nasratullah Shafiq / Generated',
    'website': '',
    'license': 'LGPL-3',

    'depends': ['base', 'hr', 'account', 'calendar', 'contacts', 'mail', ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/futsal_default_users.xml',
        'data/futsal_default_weekdays.xml',
        # 'data/futsal_default_currency.xml',
        'data/futsal_default_slot.xml',

        # Menus should load first
        'views/menu.xml',

        # Wizard files
        # 'wizard/views/finance_report_wizard_views.xml',


        # view files
        'views/futsal_reservation_views.xml',
        # 'views/salary_payment_views.xml',
        #
        # 'views/sales_views.xml',

        # Reports - actions before templates
        # 'report/finance_report_action.xml',


    ],
    # 'assets': {
    #     'web.assets_backend': [
    # 'futsal/static/src/xml/dashboard.xml',
    # 'futsal/static/src/js/dashboard.js',
    # 'futsal/static/src/css/dashboard.css',
    # ],
    # },

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
