from eagle.localapi import parse_response
from eagle.const import *
#
# Test parsing
#


def test_parse_unknown_tag():
    xml = '<NotAValidTag></NotAValidTag>'
    r = parse_response(xml)
    assert r is None

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

def test_parse_wifi_status_wifi_disabled():
    xml = '<WiFiStatus>\n  <Enabled>N</Enabled>\n  <Type>router</Type>\n  <OperatingState>down</OperatingState>\n  <LastUpTime>never</LastUpTime>\n  <LastUpTimeString>never</LastUpTimeString>\n  <SSID>eagle-00beef (router)</SSID>\n  <Encryption>psk2</Encryption>\n  <EncryptionDetails>none</EncryptionDetails>\n  <Channel>unknown</Channel>\n  <IpAddress>192.168.7.1</IpAddress>\n  <Key>0123456789abcdef</Key>\n</WiFiStatus>\n'
    r = parse_response(xml)
    assert r.__class__.__name__ == 'WifiStatus'
    assert r.enabled == False
    assert r.operating_state == 'down'
    assert r.ssid == 'eagle-00beef (router)'
    assert r.ip_address == '192.168.7.1'

def test_parse_wifi_status_wifi_enabled():
    xml = '<WiFiStatus>\n  <Enabled>Y</Enabled>\n  <Type>client</Type>\n  <OperatingState>up</OperatingState>\n  <LastUpTime>1576300561</LastUpTime>\n  <LastUpTimeString>Sat Dec 14 05:16:01 2019</LastUpTimeString>\n  <SSID>mySSID</SSID>\n  <Encryption>psk2</Encryption>\n  <EncryptionDetails>none</EncryptionDetails>\n  <Channel>11</Channel>\n  <IpAddress>192.168.7.1</IpAddress>\n  <Key>0123456789abcdef</Key>\n</WiFiStatus>\n'
    r = parse_response(xml)
    assert r.__class__.__name__ == 'WifiStatus'
    assert r.enabled == True
    assert r.operating_state == 'up'
    assert r.last_up_time == 1576300561
    assert r.ssid == 'mySSID'
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
    assert r.get_variable(VAR_INSTANTANEOUSDEMAND).value == '2.790000'
    assert r.get_variable(VAR_INSTANTANEOUSDEMAND).units == 'kW'
    assert r.get_variable(VAR_CURRENTSUMMATIONDELIVERED).value == '91937.250000'
    assert r.get_variable(VAR_PRICE).value == '0.088400'
    assert r.get_variable(VAR_PRICE).description == 'Price of electricity'
