import eagle
from const import VAR_INSTANTANEOUSDEMAND
from config import HOST, USERNAME, PASSWORD

if __name__ == "__main__":
    client = eagle.LocalApi(host=HOST, username=USERNAME, password=PASSWORD)

    # Get Wifi status information
    wifi = client.wifi_status()
    print("Wifi:", "enabled" if wifi.enabled else "disabled")
    print("Type:", wifi.type)
    print("SSID:", wifi.ssid)
    print("Encryption:", wifi.encryption)
    print("Encryption details:", wifi.encryption_details)
    print("Channel:", wifi.channel)
    print("IP Address:", wifi.ip_address)
    print("Key:", wifi.key)

    devices = client.device_list()
    print("Found {} device(s)".format(len(devices)))
    for (devnum, device) in enumerate(devices):
        print("DEVICE {}:".format(devnum))
        print("  Hardware Address: ", device.hardware_address)
        print(device)

        print("DETAILS:")
        device = client.device_details(device.hardware_address)
        print(device)
        for comp in device.components:
            print("  Component:", comp.name)
            print("  Variables supported:")
            for variable in comp.variables:
                print("    {}".format(variable.name))

        print("QUERY:")
        device = client.device_query(device.hardware_address, filter_empty_vars=True)
        print(device)
        for comp in device.components:
            print("  Component:", comp.name)
            print("  Variables values:")
            for variable in comp.variables:
                print("    {}".format(variable))

        print("\nget_all_variables():")
        print(device.get_all_variables())

        print("\nget_all_variables('" + VAR_INSTANTANEOUSDEMAND + "'):")
        print(device.get_all_variables(VAR_INSTANTANEOUSDEMAND))
