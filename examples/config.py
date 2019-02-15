# Common configuration values for examples

# The IP address of your EAGLE-200 device
HOST=''
# Username (Cloud ID)
USERNAME=''
# Password (Install Code)
PASSWORD=''

if HOST == '' or USERNAME == '' or PASSWORD == '':
    print("ERROR: EAGLE login configuration has not been set.")
    exit(1)
