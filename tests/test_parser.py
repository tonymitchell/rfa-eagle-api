from eagle.localapi import parse_response
#
# Test parsing
#

# def parse_response(response_text):
#     root = etree.fromstring(response_text)
#     if root.tag == 'DeviceList':
#         response = parse_device_list(root)
#     elif root.tag == 'Device':
#         response = parse_device(root)
#     elif root.tag == 'WiFiStatus':
#         response = parse_wifi_status(root)
#     else:
#         response = None
#         print('WARN: Unknown tag: ', root.tag)
#     return response

def test_parse_device_list():
    xml = '<DeviceList><Device></Device></DeviceList>'
    r = parse_response(xml)
    assert isinstance(r, list)
    assert len(r) == 1
    assert r[0].__class__.__name__ == 'Device'

def test_parse_device_list_multiple():
    xml = '<DeviceList><Device></Device><Device></Device></DeviceList>'
    r = parse_response(xml)
    assert isinstance(r, list)
    assert len(r) == 2
    assert r[0].__class__.__name__ == 'Device'

def test_parse_wifi_status():
    xml = '<WiFiStatus><Enabled>N</Enabled><Type>router</Type><SSID>eagle-00beef (router)</SSID><Encryption>psk2</Encryption><EncryptionDetails>none</EncryptionDetails><Channel>unknown</Channel><IpAddress>192.168.7.1</IpAddress><Key>0123456789abcdef</Key></WiFiStatus>'
    r = parse_response(xml)
    assert r.__class__.__name__ == 'WifiStatus'
    assert r.enabled == False
    assert r.ssid == 'eagle-00beef (router)'
    assert r.ip_address == '192.168.7.1'

def test_parse_device_list_sample():
    with open("tests/sample_device_list_response.xml") as f:
        xml = f.read()
    r = parse_response(xml)
    assert len(r) == 1
    assert r[0].__class__.__name__ == 'Device'
    assert r[0].hardware_address == '0x0007810000123456'
    assert len(r[0].components) == 0

def test_parse_device_query_sample():
    with open("tests/sample_device_query_response.xml") as f:
        xml = f.read()
    r = parse_response(xml)
    assert r.__class__.__name__ == 'Device'
    assert r.hardware_address == '0x0007810000123456'
    assert r.get_variable('zigbee:InstantaneousDemand').value == '2.790000'
    assert r.get_variable('zigbee:InstantaneousDemand').units == 'kW'
    assert r.get_variable('zigbee:CurrentSummationDelivered').value == '91937.250000'
    assert r.get_variable('zigbee:Price').value == '0.088400'
    assert r.get_variable('zigbee:Price').description == 'Price of electricity'
