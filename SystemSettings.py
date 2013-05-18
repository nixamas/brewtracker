'''
Created on May 18, 2013

@author: Ryan
'''
from ConfigParser import SafeConfigParser

def read_config():
    parser = SafeConfigParser()
    parser.read('config.ini')
    print str(parser)
    
def get_reading_interval():
    return int(get_value('reading_interval'))

def get_desired_temp():
    return int(get_value('desired_temp'))

def get_range():
    return int(get_value('range'))

def get_admin_email():
    return get_value('admin_email')

def get_value(option):
    parser = SafeConfigParser()
    parser.read('config.ini')
    return parser.get('BREW_BUDDY_SETTINGS', option)

def set_reading_interval(value):
    return set_value('reading_interval', value)

def set_desired_temp(value):
    return set_value('desired_temp', value)

def set_range(value):
    return set_value('range', value)

def set_admin_email(value):
    return set_value('admin_email', value)

def set_value(option, value):
    print("setting " + str(option) + " to value : " + str(value))
    parser = SafeConfigParser()
    parser.read('config.ini')
    parser.set('BREW_BUDDY_SETTINGS', option, value)
    try:
        fp = open('config.ini','w')
        parser.write(fp)
    except:
        print("error opening config.ini");
    

if __name__ == "__main__":
    print(str(get_reading_interval()))
    print(str(get_desired_temp()))
    print(get_range())
    print(str(get_admin_email()))
    
    set_reading_interval("30")
    set_desired_temp("70")
    set_range("10")
    set_admin_email("nixamas@gmail.com")
    
    print(str(get_reading_interval()))
    print(str(get_desired_temp()))
    print(get_range())
    print(str(get_admin_email()))
    
    
    
    
    
    
    