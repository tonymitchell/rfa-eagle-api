*************
RFA-Eagle-API
*************

Unofficial client for Eagle-200 from Rainforest Automation
=======================================================

Provides the ability to query the local API interface of the Eagle-200

**Example 1. Query and print all variables from device**
::
  import eagle

  client = eagle.LocalApi(host='<device ip>', username='<Cloud ID>', password='<Install Code>')
  devices = client.device_list()
  for device in devices:
      device = client.device_query(device.hardware_address)
      print(device.get_all_variables())

**Example 2. Use Meter wrapper class for simplified access to electricity meter data**
::
  import eagle

  client = eagle.LocalApi(host='<device ip>', username='<Cloud ID>', password='<Install Code>')
  meters = eagle.Meter.get_meters(client)
  for meter in meters:
      meter.update()
      print("Demand:", meter.instantaneous_demand)

**Links:**

* Rainforest Automation https://rainforestautomation.com/
* Eagle-200 https://rainforestautomation.com/rfa-z114-eagle-200-2/
* Developer Resources: https://rainforestautomation.com/support/developer/
* Local API documentation: http://rainforestautomation.com/wp-content/uploads/2017/02/EAGLE-200-Local-API-Manual-v1.0.pdf
