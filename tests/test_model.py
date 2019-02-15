import eagle
from eagle.localapi import WifiStatus, Variable, Component, Device

def test_wifi_status():
    attributes = {
        'enabled': False,
        'type': 'router',
        'ssid': 'eagle-00abcd (router)',
        'encryption': 'psk2',
        'encryption_details': 'none',
        'channel': 'unknown',
        'ip_address': '192.168.7.1',
        'key': '0000000000000000',
    }
    status = WifiStatus(**attributes)
    assert status.enabled == False
    assert status.type == 'router'
    assert status.ssid == 'eagle-00abcd (router)'
    assert status.encryption == 'psk2'
    assert status.encryption_details == 'none'
    assert status.channel == 'unknown'
    assert status.ip_address == '192.168.7.1'
    assert status.key == '0000000000000000'

def test_wifi_status_repr():
    attributes = {
        'enabled': False,
        'type': 'router',
        'ssid': 'eagle-00abcd (router)',
        'encryption': 'psk2',
        'encryption_details': 'none',
        'channel': 'unknown',
        'ip_address': '192.168.7.1',
        'key': '0000000000000000',
    }
    status = WifiStatus(**attributes)
    assert repr(status) == "WifiStatus(False, 'router', 'eagle-00abcd (router)', 'psk2', 'none', 'unknown', '192.168.7.1', '0000000000000000')"

def test_variable_repr():
    variable = Variable('aName', 'aValue', 'theUnits', 'the description')
    
    assert repr(variable) == "Variable('aName', 'aValue', 'theUnits', 'the description')"

def test_component_repr():
    variable = Component('aName', [Variable('var1', 1), Variable('var2', 2)])

    assert repr(variable) == "Component('aName', [Variable('var1', 1, '', ''), Variable('var2', 2, '', '')])"

def test_device_repr():
    variable = Device(name='dName', hardware_address='dHwAddress', network_interface='dNetInf', protocol='dProt', network_address='dNetAddr', 
                      manufacturer='dMan', model_id='dMod', last_contact='dLastCont', connection_status='dConnStatus',
                      components=Component('aName', [Variable('var1', 1), Variable('var2', 2)]))

    assert repr(variable) == "Device('dName', 'dHwAddress', 'dNetInf', 'dProt', 'dNetAddr', 'dMan', 'dMod', 'dLastCont', 'dConnStatus', Component('aName', [Variable('var1', 1, '', ''), Variable('var2', 2, '', '')]))"

