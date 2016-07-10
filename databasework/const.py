# -*- encoding: utf-8 -*-
from models import *

UPLOADMODEL = {
    'Cell': Cell,
    'Msc': Msc,
    'Bsc': Bsc,
    'Bts': Bts,
    'Phone': Phone,
    'Ms': Ms,
    'Ant': Ant,
    'Test': Test,
    'Fpnt': Fpnt,
}

FOREIGNKEY_FIELDS = ['msc', 'bsc', 'cell', 'ant', 'phone', 'bts', 'ms', 'test', 'fpnt']

CHOICES = [
    ('Cell', u'小区Cell信息'),
    ('Ms', u'移动台MS信息'),
    ('Msc', 'Msc'),
    ('Bts', 'Bts'),
    ('Bsc', 'Bsc'),
    ('Ant', 'Ant'),
    ('Phone', 'Phone'),
    ('Test', 'Test'),
    ('Fpnt', 'Fpnt'),
]

