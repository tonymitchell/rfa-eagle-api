#
# Unofficial client for the Rainforest Automation EAGLE-200 
#

from typing import List

import collections
import json
import logging
from lxml import etree
import requests
import inflection
from datetime import datetime, timezone

from .const import (
    VAR_INSTANTANEOUSDEMAND,VAR_CURRENTSUMMATIONDELIVERED, VAR_CURRENTSUMMATIONRECEIVED, VAR_PRICE, VAR_RATELABEL, 
    VAR_PRICETIER, VAR_PRICESTARTTIME, VAR_PRICEDURATION, VAR_BLOCKPERIODNUMBEROFBLOCKS, VAR_BLOCKNPRICE, VAR_BLOCKNTHRESHOLD,
    VAR_BLOCKPERIODSTART, VAR_BLOCKPERIODDURATION, VAR_BLOCKPERIODCONSUMPTION, VAR_BILLINGPERIODSTART, VAR_BILLINGPERIODDURATION,
    VAR_BLOCK1PRICE, VAR_BLOCK1THRESHOLD,
    VAR_BLOCK2PRICE, VAR_BLOCK2THRESHOLD,
    VAR_BLOCK3PRICE, VAR_BLOCK3THRESHOLD,
    VAR_BLOCK4PRICE, VAR_BLOCK4THRESHOLD,
    VAR_BLOCK5PRICE, VAR_BLOCK5THRESHOLD,
    VAR_BLOCK6PRICE, VAR_BLOCK6THRESHOLD,
    VAR_BLOCK7PRICE, VAR_BLOCK7THRESHOLD,
    VAR_BLOCK8PRICE, VAR_BLOCK8THRESHOLD,
    )

_LOGGER = logging.getLogger(__name__)

def enable_debug_logging():
    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True



#
# Response models
#

class WifiStatus:
    """
    Expected Response:
    <WiFiStatus>
    <Enabled>N</Enabled>
    <Type>router</Type>
    <SSID>eagle-00beef (router)</SSID>
    <Encryption>psk2</Encryption>
    <EncryptionDetails>none</EncryptionDetails>
    <Channel>unknown</Channel>
    <IpAddress>192.168.7.1</IpAddress>
    <Key>0123456789abcdef</Key>
    </WiFiStatus>        
    """
    def __init__(self, enabled = False, type ='', ssid ='', encryption ='', encryption_details ='', channel ='', ip_address = '', key = '', **kwargs):
        self._enabled = enabled
        self._type = type
        self._ssid = ssid
        self._encryption = encryption
        self._encryption_details = encryption_details
        self._channel = channel
        self._ip_address = ip_address
        self._key = key

    def __repr__(self):
        attrs = ("enabled", "type", "ssid", "encryption", "encryption_details", "channel","ip_address","key")
        args = ", ".join(["%s=%r" % (n, getattr(self, n)) for n in attrs])
        return "%s(%s)" % (self.__class__.__name__, args)

    # Properties
    @property
    def enabled(self):
        """ Return True if Wifi enable, otherwise false """
        return self._enabled
    @property
    def type(self):
        return self._type
    @property
    def ssid(self):
        return self._ssid
    @property
    def encryption(self):
        return self._encryption
    @property
    def encryption_details(self):
        return self._encryption_details
    @property
    def channel(self):
        return self._channel
    @property
    def ip_address(self):
        return self._ip_address
    @property
    def key(self):
        return self._key



class Variable:
    """
    <Variable>
        <Name>zigbee:InstantaneousDemand</Name>
        <Value>1.562000</Value>
        <Units>kW</Units>
        <Description>Instantaneous Demand</Description>
    </Variable>
    """
    def __init__(self, name, value, units = "", description = ""):
        self._name = name
        self._value = value
        self._units = units
        self._description = description

    def __repr__(self):
        attrs = ("name", "value", "units", "description")
        args = ", ".join(["%s=%r" % (n, getattr(self, n)) for n in attrs])
        return "%s(%s)" % (self.__class__.__name__, args)


    @property
    def name(self):
        return self._name
    @property
    def value(self):
        return self._value
    @property
    def units(self):
        return self._units
    @property
    def description(self):
        return self._description


class Component:
    def __init__(self, name, variables = []):
        self.name = name
        self.variables = variables

    def __repr__(self):
        attrs = ("name", "variables")
        args = ", ".join(["%s=%r" % (n, getattr(self, n)) for n in attrs])
        return "%s(%s)" % (self.__class__.__name__, args)


    def get_variable(self, name) -> Variable:
        for variable in self.variables:
            if variable.name == name:
                return variable
        return None


class Device:
    """ """
    def __init__(self, 
                 name='', hardware_address='', network_interface='', protocol='', network_address='', 
                 manufacturer='', model_id='', last_contact='', connection_status='', 
                 components = []):
        self._name=name
        self._hardware_address=hardware_address
        self._network_interface=network_interface
        self._protocol=protocol
        self._network_address=network_address
        self._manufacturer=manufacturer
        self._model_id=model_id
        self._last_contact=last_contact
        self._connection_status=connection_status
        self._components = components

    def __repr__(self):
        attrs = ("name", "hardware_address", "network_interface", "protocol", "network_address", 
                 "manufacturer", "model_id", "last_contact", "connection_status", "components")
        args = ", ".join(["%s=%r" % (n, getattr(self, n)) for n in attrs])
        return "%s(%s)" % (self.__class__.__name__, args)


    def get_variable(self, name) -> Variable:
        for component in self.components:
            variable = component.get_variable(name)
            if variable is not None:
                return variable
        return None

    def get_all_variables(self, var_name = None):
        result = {}

        if var_name is not None:
            # Get named variable across all components
            for component in self.components:
                variable = component.get_variable(var_name)
                if variable is not None:
                    result[component.name] = variable
        else:
            # Get All variables across all components
            for component in self.components:
                result[component.name] = component.variables

        return result

    # Properties
    @property
    def name(self):
        return self._name
    @property
    def hardware_address(self):
        """MAC Address of the device"""
        return self._hardware_address
    @property
    def network_interface(self):
        """MAC Address of the EAGLE device""" 
        return self._network_interface
    @property
    def protocol(self):
        return self._protocol
    @property
    def network_address(self):
        return self._network_address
    @property
    def manufacturer(self):
        return self._manufacturer
    @property
    def model_id(self):
        return self._model_id
    @property
    def last_contact(self):
        return self._last_contact
    @property
    def connection_status(self):
        return self._connection_status

    @property
    def components(self) -> List[Component]:
        return self._components


#
# Response model parsers
#

def _date_from_hex(hex_timestamp):
    return datetime.fromtimestamp(int(hex_timestamp, 16))

def _safe_text(variable):
    if variable is not None:
        return variable.text
    return None

def parse_response(response_text):
    root = etree.fromstring(response_text)
    if root.tag == 'DeviceList':
        response = parse_device_list(root)
    elif root.tag == 'Device':
        response = parse_device(root)
    elif root.tag == 'WiFiStatus':
        response = parse_wifi_status(root)
    else:
        response = None
        _LOGGER.error('Unknown tag: %s', root.tag)
    return response

def parse_device_list(device_root):
    """ Parse DeviceList XML block into object """
    devices = [parse_device(device) for device in device_root.findall("Device")]
    return devices

def parse_device(device):
    """Parse Device XML block into object. Supports block with properties as
    both direct children elements, and nested under a DeviceDetails element

    <Name>Power Meter</Name>
    <HardwareAddress>0x0007810000123456</HardwareAddress>
    <NetworkInterface>0xd8d5b90000001234</NetworkInterface>
    <Protocol>Zigbee</Protocol>
    <NetworkAddress>0x0000</NetworkAddress>
    <Manufacturer>Generic</Manufacturer>
    <ModelId>electric_meter</ModelId>
    <LastContact>0x5c4ea428</LastContact>
    <ConnectionStatus>Connected</ConnectionStatus>
    """

    # Elements are either direct children or nested under a DeviceDetails element
    details = device.find("DeviceDetails")
    if details is None:
        details = device

    # Convert tags to property names
    attributes = {inflection.underscore(x.tag):x.text for x in details}
    # Convert last_contact to datetime
    if 'last_contact' in attributes:
        attributes['last_contact'] = _date_from_hex(attributes['last_contact'])

    components = [parse_component(comp) for comp in device.findall("Components/Component")]
    return Device(**attributes, components=components)

def parse_component(component):
    """ Parse Component XML block into object """
    name = component.find('Name').text
    #hardware_id = component.find('HardwareId').text
    #fixed_id = component.find('FixedId').text
    variables = [parse_variable(var) for var in component.findall("Variables/Variable")]
    return Component(name, variables)

def parse_variable(variable):
    """ Parse Variable XML block into object """

    # Handle both types of variables blocks:
    #  Simple (<Variable>VAR_NAME</Variable>), and 
    #  Detailed <Variable><Name>VAR_NAME</Name><Value>VAR_VALUE</Value>...</Variable)
    if variable.find('Name') is None:
        # Simple
        name = variable.text
        value = None
        units = None
        description = None
    else:
        # Detailed
        name = variable.find('Name').text
        value = _safe_text(variable.find('Value'))
        units = _safe_text(variable.find('Units'))
        description = _safe_text(variable.find('Description'))
    return Variable(name, value, units, description)

def parse_wifi_status(wifi_status):
    """ Parse WiFiStatus XML block into object """

    # Convert tags to property names
    attributes = {inflection.underscore(x.tag):x.text for x in wifi_status}
    # Convert enabled to datetime
    if 'enabled' in attributes:
        attributes['enabled'] = (attributes['enabled']  == 'Y')

    return WifiStatus(**attributes)




#
# Local API client
#

class LocalApi(object):
    """
    Eagle-200 Local API client
    """
    def __init__(self, host, username, password, timeout=5):
        self.host = host
        self.url = "http://{0}/cgi-bin/post_manager".format(host)
        self.username = username
        self.password = password
        self.timeout = timeout

    def _call(self, command):
        """ Call service """
        response = requests.post(url=self.url, data=command, headers={'Content-Type':'text/xml'}, 
                                 auth=(self.username, self.password), verify=False, timeout=self.timeout)
        response.raise_for_status()
    
        # with open("response_log.ndxml", "a") as log:
        #     log.write(response.text + "\n")

        return response.text


    def _build_command(self, command_name, hardware_address = '', comp_var_dict = None):
        """ Build command body from parameters """
        # Start command adn set name
        command = "<Command><Name>{command_name}</Name>".format(command_name=command_name)

        if hardware_address:
            command += "<DeviceDetails><HardwareAddress>{hardware_address}</HardwareAddress></DeviceDetails>".format(hardware_address=hardware_address)

        if comp_var_dict is not None:
            comp_keys = comp_var_dict.keys()
            if len(comp_keys) > 0:
                for comp_key in comp_keys:
                    # Build requested variable list
                    command += "<Components><Component><Name>{comp_key}</Name><Variables>".format(comp_key=comp_key)
                    variables = comp_var_dict[comp_key]
                    for var in variables:
                        command += "<Variable><Name>{var}</Name></Variable>".format(var=var)
                    command += "</Variables></Component></Components>"
            else:
                # Request all variables from all components
                command += "<Components><All>Y</All></Components>"

        # Close command
        command += "</Command>"
        
        return command


    def wifi_status(self) -> WifiStatus:
        """
        Get Wi-Fi status
        """
        command = self._build_command("wifi_status")
        response = self._call(command)
        return parse_response(response)


    def device_list(self) -> List[Device]:
        """
        Response from the EAGLE will contain a list of all the devices that are in its \
        device tables – from both the HAN and the Control Network.     
        """
        command = self._build_command("device_list")
        response = self._call(command)
        return parse_response(response)
        

    def device_details(self, hardware_address) -> Device:
        """
        Response from the EAGLE will contain a list of all the devices that are in its \
        device tables – from both the HAN and the Control Network.     
        """
        command = self._build_command("device_details", hardware_address)
        response = self._call(command)
        return parse_response(response)
        

    def device_query(self, hardware_address, comp_var_dict = {}, filter_empty_vars = False):
        """
        Response containing the value of the requested variable (in this case instantaneous 
        demand) that it has stored in its data buffer for this device.
        """
        command = self._build_command("device_query", hardware_address, comp_var_dict)
        response = self._call(command)
        device = parse_response(response)
        if filter_empty_vars:
            for comp in device.components:
                # Iterate over copy of list (to avoid issues when removing items)
                for var in comp.variables[:]:
                    if var.value is None:
                        comp.variables.remove(var)
        return device
                            

    # def device_add(self, network_interface, device_details):
    #     pass

    # def device_control(self hardware_address, comp_var_dict = None):
    #     pass


#
# High-level, simplified API for ease-of-use
#

PriceBlock = collections.namedtuple('PriceBlock', ['price', 'threshold'])

class Meter:
    """
    Represents an individual meter
    """
    @staticmethod
    def get_meters(api):
        """ Fetch a list of electric meters """
        devices = api.device_list()
        return [Meter(api, device.hardware_address) for device in devices if device.model_id == 'electric_meter']


    def __init__(self, api, hardware_address):
        self._api = api
        self._hardware_address = hardware_address
        self.update()
    
    def update(self):
        """ Re-query device for updated values """
        self.device = self._api.device_query(self._hardware_address, {})

    def _safe_value(self, var_name, type_formatter = None):
        """ Get device variable value by name """
        var = self.device.get_variable(var_name)
        if var is not None:
            if type_formatter is not None and var.value is not None:
                return type_formatter(var.value)
            else:
                return var.value
        return None


    @property
    def instantaneous_demand(self):
        """ Instaneous demand (kW) """
        return self._safe_value(VAR_INSTANTANEOUSDEMAND, float)
        
    @property
    def current_summation_delivered(self):
        """ Summation Delivered to Home (kWh) """
        return self._safe_value(VAR_CURRENTSUMMATIONDELIVERED, float)

    @property
    def current_summation_received(self):
        """ Summation Received from Home (kWh) """
        return self._safe_value(VAR_CURRENTSUMMATIONRECEIVED, float)

    @property
    def price(self):
        """ Price of electricity (kW) """
        return self._safe_value(VAR_PRICE, float)

    @property
    def rate_label(self):
        """ Active price rate label """
        return self._safe_value(VAR_RATELABEL, str)

    @property
    def price_tier(self):
        """ The current Price Tier """
        return self._safe_value(VAR_PRICETIER, str)

    @property
    def price_start_time(self): #ISO8601 or timestamp
        """ The time at which the price signal becomes valid """

        try:
            # Devices returns UTC date string (e.g. 'Wed Feb 13 06:32:47 2019')
            dtm_str = self._safe_value(VAR_PRICESTARTTIME)
            # Parse date string
            dtm = datetime.strptime(dtm_str, "%c")
            # Get UTC timestamp
            timestamp = dtm.replace(tzinfo=timezone.utc).timestamp()

            return int(timestamp)
        except ValueError:
            _LOGGER.warning("Error parsing price_start_time value: %s", dtm_str)
            return None

    @property
    def price_duration(self):
        """ Amount of time in minutes after the Start Time during which the price signal is valid (min) """
        return self._safe_value(VAR_PRICEDURATION, int)

    @property
    def block_period_start(self): # ISO8601 or timestamp
        """ The start time of the current block tariff period """
        return self._safe_value(VAR_BLOCKPERIODSTART, int)

    @property
    def block_period_duration(self):
        """ The current block tariff period duration in minutes """
        return self._safe_value(VAR_BLOCKPERIODDURATION, int)

    @property
    def block_period_consumption(self):
        """ The most recent summed value of Energy, Gas or Water delivered and consumed in the premises during the Block Tariff Period (kWh) """
        return self._safe_value(VAR_BLOCKPERIODCONSUMPTION, float)

    @property
    def billing_period_start(self):  # ISO8601 or timestamp
        """ The start time of the current billing period """
        return self._safe_value(VAR_BILLINGPERIODSTART, int)

    @property
    def billing_period_duration(self):
        """ The current billing period duration in minutes (min) """
        return self._safe_value(VAR_BILLINGPERIODDURATION, int)


    @property
    def blocks(self): # (list of size: block_period_number_of_blocks)
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier 
            the block threshold values for a given period (typically the billing cycle)
        """
        blocks = []

        numblocks = self._safe_value(VAR_BLOCKPERIODNUMBEROFBLOCKS, int)
        if numblocks is not None:
            for i in range(1, numblocks + 1):
                price = self._safe_value(VAR_BLOCKNPRICE.format(i), float)
                threshold = self._safe_value(VAR_BLOCKNTHRESHOLD.format(i), float)

                blocks.append(PriceBlock(price, threshold))

        return blocks

    # Explicit block properties as well
    @property
    def block1_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK1PRICE, float)

    @property
    def block1_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK1THRESHOLD, float)

    @property
    def block2_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK2PRICE, float)

    @property
    def block2_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK2THRESHOLD, float)

    @property
    def block3_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK3PRICE, float)

    @property
    def block3_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK3THRESHOLD, float)

    @property
    def block4_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK4PRICE, float)

    @property
    def block4_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK4THRESHOLD, float)

    @property
    def block5_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK5PRICE, float)
    
    @property
    def block5_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK5THRESHOLD, float)

    @property
    def block6_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK6PRICE, float)

    @property
    def block6_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK6THRESHOLD, float)

    @property
    def block7_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK7PRICE, float)

    @property
    def block7_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK7THRESHOLD, float)

    @property
    def block8_price(self):
        """ The price of Energy, Gas, or Water delivered to the premises at a specific price tier  """
        return self._safe_value(VAR_BLOCK8PRICE, float)

    @property
    def block8_threshold(self):
        """ The block threshold values for a given period (typically the billing cycle)  """
        return self._safe_value(VAR_BLOCK8THRESHOLD, float)

