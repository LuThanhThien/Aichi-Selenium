import os
import time
from datetime import datetime
from src.utils import file_utils as fu

def abs_path(*path):
    return os.path.join(*path)

class Paths(object):
    '''    Global paths    '''
    srcdir = os.path.dirname(os.path.abspath(__file__))
    basedir = os.path.dirname(srcdir)
    version = '1.0.1'
    logs = abs_path(basedir, "logs")
    configs = abs_path(basedir, "configs")
    drivers = abs_path(basedir, "drivers")
    contries_mapping = abs_path(configs, "mappings", "contries_mapping.json")
    nations_mapping = abs_path(configs, "mappings", "nations_mapping.json")
    meta_info = abs_path(configs, "info", "meta.yml")
    fake_info = abs_path(configs, "info", "fake.yml")
    urls_info = abs_path(configs, "info", "urls.yml")
    accounts_info = abs_path(configs, "info", "accounts.yml")
    customers_info = abs_path(configs, "info", "customers.yml")
    
class Configs(object):
    '''    Global configs    '''
    meta: dict = fu.read(Paths.meta_info)
    fake: dict = fu.read(Paths.fake_info)
    urls: dict = fu.read(Paths.urls_info)
    accounts: dict = fu.read(Paths.accounts_info)
    customers: dict = fu.read(Paths.customers_info)
    countries_mapping: dict = fu.read(Paths.contries_mapping)
    nations_mapping: dict = fu.read(Paths.nations_mapping)

class Mappings(object):
    '''    Global mappings    '''
    
    @staticmethod
    def get_country_name(country_code):
        return Configs.countries_mapping.get(country_code)
    
    @staticmethod
    def get_nation_name(nation_code):   
        return Configs.nations_mapping.get(nation_code)

class Accounts(object):
    '''    Global accounts    '''
    test_accounts = Configs.accounts['test_accounts']
    dev_accounts = Configs.accounts['dev_accounts']
    num_test_accounts = len(test_accounts) if test_accounts is not None else 0
    num_dev_accounts = len(dev_accounts) if dev_accounts is not None else 0
    num_accounts = num_dev_accounts + num_test_accounts

    @staticmethod
    def get_dev_account(index: int = 0):
        return Configs.accounts['dev_accounts'][index]
    
    @staticmethod
    def get_test_account(index: int = 0):
        return Configs.accounts['test_accounts'][index]

class Customers(object):
    '''    Global customers    '''
    customers = Configs.customers['customers'] 
    num_customers = len(customers) if customers is not None else 0
    
    @staticmethod
    def get_customer(index):
        return Configs.customers['customers'][index]

class Meta(object):
    '''        Meta configs        '''
    keyword = Configs.meta['keyword']
    test_mode = False if keyword in ['Tosan', 'Hirabari'] else True
    debug_mode = Configs.meta['debug_mode']
    onlyday = Configs.meta['onlyday']
    max_num_retry = Configs.meta['max_num_retry']
    default_num_threads = min(Configs.meta['default_num_threads'], Accounts.num_test_accounts)
    display_number = Configs.meta['display_number']
    main_phone_number_dash = Configs.meta['main_phone_number_dash']
    uc = Configs.meta['uc']
    headless = Configs.meta['headless']
    timeout = Configs.meta['timeout']
    

class Fake(object):
    '''        Fake configs        '''
    last_name = Configs.fake['last_name']
    first_name = Configs.fake['first_name']
    date_birth = Configs.fake['date_birth']
    gender = Configs.fake['gender']
    phone_number = Configs.fake['phone_number']
    phone_number_dash = Configs.fake['phone_number_dash']
    nation = Configs.fake['nation']
    country = Configs.fake['country']
    school_name = Configs.fake['school_name']
    prefacture = Configs.fake['prefacture']
    examin_number = Configs.fake['examin_number']

class URLs(object):
    '''    Global URLs    '''
    main_url = Configs.urls['main_url']
    login_url = Configs.urls['login_url']
    re_login_url = Configs.urls['re_login_url'] 
    disp_url = Configs.urls['disp_url']
    form_prefix_url = Configs.urls['form_prefix_url']
    form_url = Configs.urls['form_url']
    confirm_url = Configs.urls['confirm_url']
    inquery_url = Configs.urls['inquery_url']
    detail_base_url = Configs.urls['detail_base_url']

class Keywords(object):
    '''    Global keywords    '''
    Tosan = 'Tosan'
    Hirabari = 'Hirabari'

class Variables(object):
    '''    Global variables    '''
    # instances
    date = time.strftime("%Y_%m_%d")
    current_time = time.strftime("%H_%M_%S")
    datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


