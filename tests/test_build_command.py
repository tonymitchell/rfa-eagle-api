import eagle

def test_build_command_simple():
    api = eagle.LocalApi('', '', '')
    cmd = api._build_command('a_command_name')
    assert cmd == '<Command><Name>a_command_name</Name></Command>'

def test_build_command_with_hardware_address():
    api = eagle.LocalApi('', '', '')
    cmd = api._build_command('a_command_name', 'address')
    assert cmd == '<Command><Name>a_command_name</Name><DeviceDetails><HardwareAddress>address</HardwareAddress></DeviceDetails></Command>'

def test_build_command_with_hardware_address_and_vars():
    api = eagle.LocalApi('', '', '')
    cmd = api._build_command('a_command_name', 'address', {'Main':['var1','var2']})
    assert cmd == '<Command><Name>a_command_name</Name><DeviceDetails><HardwareAddress>address</HardwareAddress></DeviceDetails><Components><Component><Name>Main</Name><Variables><Variable><Name>var1</Name></Variable><Variable><Name>var2</Name></Variable></Variables></Component></Components></Command>'
    
def test_build_command_with_hardware_address_and_emptyvars():
    api = eagle.LocalApi('', '', '')
    cmd = api._build_command('a_command_name', 'address', {})
    assert cmd == '<Command><Name>a_command_name</Name><DeviceDetails><HardwareAddress>address</HardwareAddress></DeviceDetails><Components><All>Y</All></Components></Command>'

