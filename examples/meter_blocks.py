import time

import eagle
from config import HOST, USERNAME, PASSWORD

if __name__ == "__main__":

    client = eagle.LocalApi(host=HOST, username=USERNAME, password=PASSWORD)
    meters = eagle.Meter.get_meters(client)
    for meter in meters:
        
        print("Found {} block(s)".format(len(meter.blocks)))
        print("Blocks:", meter.blocks)
        print("Block 1 Price:",     meter.block1_price)
        print("Block 1 Threshold:", meter.block1_threshold)
        print("Block 2 Price:",     meter.block2_price)
        print("Block 2 Threshold:", meter.block2_threshold)
        print("Block 3 Price:",     meter.block3_price)
        print("Block 3 Threshold:", meter.block3_threshold)
        print("Block 4 Price:",     meter.block4_price)
        print("Block 4 Threshold:", meter.block4_threshold)
        print("Block 5 Price:",     meter.block5_price)
        print("Block 5 Threshold:", meter.block5_threshold)
        print("Block 6 Price:",     meter.block6_price)
        print("Block 6 Threshold:", meter.block6_threshold)
        print("Block 7 Price:",     meter.block7_price)
        print("Block 7 Threshold:", meter.block7_threshold)
        print("Block 8 Price:",     meter.block8_price)
        print("Block 8 Threshold:", meter.block8_threshold)
