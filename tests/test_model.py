import eagle
from eagle.localapi import WifiStatus

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
