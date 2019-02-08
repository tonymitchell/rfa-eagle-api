import eagle
from config import HOST, USERNAME, PASSWORD

if __name__ == "__main__":

    client = eagle.LocalApi(host=HOST, username=USERNAME, password=PASSWORD)
    meters = eagle.Meter.get_meters(client)
    for meter in meters:
        meter.update()
        print("Demand:", meter.instantaneous_demand)
