import time

import eagle
from config import HOST, USERNAME, PASSWORD

if __name__ == "__main__":

    client = eagle.LocalApi(host=HOST, username=USERNAME, password=PASSWORD)
    meters = eagle.Meter.get_meters(client)
    for meter in meters:
        print("Demand: {} ({})".format(meter.instantaneous_demand, meter.device.last_contact))

    print("Waiting for 10 seconds before taking next reading.")
    for i in range(10,0,-1):
        print(str(i).rjust(2), end='\r')
        time.sleep(1)

    for meter in meters:
        meter.update()
        print("Demand: {} ({})".format(meter.instantaneous_demand, meter.device.last_contact))
