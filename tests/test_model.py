import eagle
from eagle.localapi import WifiStatus

def test_wifi_status():
    attributes = {
        'enabled': False
        #,
    # <Type>router</Type>
    # <SSID>eagle-00aab8 (router)</SSID>
    # <Encryption>psk2</Encryption>
    # <EncryptionDetails>none</EncryptionDetails>
    # <Channel>unknown</Channel>
    # <IpAddress>192.168.7.1</IpAddress>
    # <Key>2bba5444cf92f271</Key>
    }
    status = WifiStatus(**attributes)
    assert status.enabled == False