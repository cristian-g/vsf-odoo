{
    'name': 'RESTful API',
    'version': '0.0.1',
    'category': 'API',
    'author': 'Cristian González Ruz',
    'website': 'http://cristiangonzalez.com',
    'summary': 'RESTful API',
    'support': 'hello@cristiangonzalez.com',
    'description': """
RESTful API
===========
See https://github.com/cristian-g/restful
""",
    'depends': [
        'web',
    ],
    'data': [
        'data/ir_config_param.xml',
        'views/ir_model.xml',
        'views/res_users.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/main_screenshot.png'],
    'license': 'Other Propietary',
    'installable': True,
    'auto_install': False,
}
