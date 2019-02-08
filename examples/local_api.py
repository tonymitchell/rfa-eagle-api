import eagle
from config import HOST, USERNAME, PASSWORD

if __name__ == "__main__":
    client = eagle.LocalApi(host=HOST, username=USERNAME, password=PASSWORD)

    # Get Wifi status information
    wifi = client.wifi_status()
    print("Wifi:", "enabled" if wifi.enabled else "disabled")
    print("SSID:", wifi.ssid)
    print("IP:", wifi.ip_address)

    devices = client.device_list()
    print("Found {} device(s)".format(len(devices)))
    for (devnum, device) in enumerate(devices):
        print("DEVICE {}:".format(devnum))
        print("  Hardware Address: ", device.hardware_address)

        print("DETAILS:")
        device = client.device_details(device.hardware_address)
        for comp in device.components:
            print("  Component:", comp.name)
            print("  Variables supported:")
            for variable in comp.variables:
                print("    {}".format(variable.name))

        print("QUERY:")
        device = client.device_query(device.hardware_address, filter_empty_vars=True)
        for comp in device.components:
            print("  Component:", comp.name)
            print("  Variables values:")
            for variable in comp.variables:
                print("    {}".format(variable))

        print("\nget_all_variables():")
        print(device.get_all_variables())

        print("\nget_all_variables('zigbee:InstantaneousDemand'):")
        print(device.get_all_variables('zigbee:InstantaneousDemand'))
