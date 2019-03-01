from unittest import mock

import eagle
from eagle.localapi import Meter, Device, Component, Variable
from eagle.const import VAR_INSTANTANEOUSDEMAND


def api_mock_all_variables():
    device = Device(components=[
        Component('NAME', variables=[
        Variable('zigbee:BillingPeriodDuration', '87840', 'min', 'The current billing period duration in minutes'),
        Variable('zigbee:BillingPeriodStart', '1548316764', None, 'The start time of the current billing period'), 
        Variable('zigbee:Block1Price', '0.088400', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
        Variable('zigbee:Block1Threshold', '1354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
        Variable('zigbee:Block2Price', '0.132600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
        Variable('zigbee:BlockPeriodConsumption', '852.180000', 'kWh', 'The most recent summed value of Energy, Gas or Water delivered and consumed in the premises during the Block Tariff Period'), 
        Variable('zigbee:BlockPeriodDuration', '62860', 'min', 'The current block tariff period duration in minutes'), 
        Variable('zigbee:BlockPeriodNumberOfBlocks', '2', None, None), 
        Variable('zigbee:BlockPeriodStart', '1548316764', None, 'The start time of the current block tariff period'), 
        Variable('zigbee:BlockThresholdDivisor', '1', None, 'Provides a value to divide the result of applying the threshold multiplier attribute to Block Threshold values'), 
        Variable('zigbee:BlockThresholdMultiplier', '1', None, 'Provides a value to be multiplied against Threshold attributes'), 
        Variable('zigbee:Currency', 'USD', None, 'The local unit of currency used in the price field'), 
        Variable('zigbee:CurrentSummationDelivered', '92257.761000', 'kWh', 'Summation Delivered to Home'), 
        Variable('zigbee:CurrentSummationReceived', '0.000000', 'kWh', 'Summation Received from Home'), 
        Variable('zigbee:Divisor', '1000', None, 'Divisor applied to demand and summation values'), 
        Variable('zigbee:InstantaneousDemand', '2.478000', 'kW', 'Instantaneous Demand'), 
        Variable('zigbee:MessageConfirmationRequired', 'N', None, 'Indicates if the message requires user confirmation'), 
        Variable('zigbee:MessageConfirmed', 'N', None, 'Indicates if the message has received user confirmation'), 
        Variable('zigbee:Multiplier', '1', None, 'Multiplier applied to demand and summation values'), 
        Variable('zigbee:Price', '0.088400', None, 'Price of electricity'), 
        Variable('zigbee:PriceDuration', '-1', 'min', 'Amount of time in minutes after the Start Time during which the price signal is valid'), 
        Variable('zigbee:PriceStartTime', 'Wed Feb 13 06:32:47 2019', None, 'The time at which the price signal becomes valid'), 
        Variable('zigbee:PriceTier', '0', None, 'The current Price Tier'), 
        Variable('zigbee:RateLabel', 'Block 1', None, 'Active priuce rate label'), 
        Variable('zigbee:TrailingDigits', '4', None, 'Indicates the number of digits to the right of the decimal point'), 
        ])
    ])

    mock_api = mock.Mock()
    mock_api.device_query.return_value = device
    return mock_api


def test_meter_properties():
    mock_api = api_mock_all_variables()

    meter = Meter(mock_api, 'address')

    assert meter.billing_period_duration == 87840
    assert meter.billing_period_start == 1548316764
    assert meter.block_period_consumption == 852.180000
    assert meter.block_period_duration == 62860
    assert meter.block_period_start == 1548316764
    assert meter.blocks == [(0.0884, 1354.0), (0.1326, None)]
    assert meter.current_summation_delivered == 92257.761000
    assert meter.current_summation_received == 0.000000
    assert meter.instantaneous_demand == 2.478000
    assert meter.price == 0.088400
    assert meter.price_duration == -1
    #assert meter.price_start_time == 'Wed Feb 13 06:32:47 2019'
    assert meter.price_tier == '0'
    assert meter.rate_label == 'Block 1'


def test_meter_price_start_time_parsing_valid():
    device = Device(components=[
        Component('NAME', variables=[
            Variable('zigbee:PriceStartTime', 'Wed Feb 13 06:32:47 2019', None, 'The time at which the price signal becomes valid'), 
        ])
    ])
    mock_api = mock.Mock()
    mock_api.device_query.return_value = device

    meter = Meter(mock_api, 'address')

    assert meter.price_start_time == 1550039567


def test_meter_price_start_time_parsing_invalid():
    device = Device(components=[
        Component('NAME', variables=[
            Variable('zigbee:PriceStartTime', 'Feb 13, 2019 06:32:47'), 
        ])
    ])
    mock_api = mock.Mock()
    mock_api.device_query.return_value = device

    meter = Meter(mock_api, 'address')

    assert meter.price_start_time is None


def test_meter_8_blocks():
    device = Device(components=[
        Component('NAME', variables=[
            Variable('zigbee:BlockPeriodNumberOfBlocks', '8', None, None), 
            Variable('zigbee:Block1Price', '0.088400', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block1Threshold', '1354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block2Price', '0.132600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block2Threshold', '2354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block3Price', '0.182600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block3Threshold', '3354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block4Price', '0.212600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block4Threshold', '4354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block5Price', '0.232600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block5Threshold', '5354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block6Price', '0.252600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block6Threshold', '6354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block7Price', '0.282600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
            Variable('zigbee:Block7Threshold', '7354.000000', 'kWh', 'the block threshold values for a given period (typically the billing cycle)'), 
            Variable('zigbee:Block8Price', '0.312600', 'USD/kWh', 'The price of Energy, Gas, or Water delivered to the premises at a specific price tier'), 
        ])
    ])
    mock_api = mock.Mock()
    mock_api.device_query.return_value = device

    meter = Meter(mock_api, 'address')

    assert len(meter.blocks) == 8
    assert meter.blocks == [
        (0.0884,   1354.0), 
        (0.132600, 2354.0), 
        (0.182600, 3354.0), 
        (0.212600, 4354.0), 
        (0.232600, 5354.0), 
        (0.252600, 6354.0), 
        (0.282600, 7354.0), 
        (0.312600, None), 
    ]
    # Access via named tuple fields
    assert meter.blocks[1].price == 0.132600
    assert meter.blocks[1].threshold == 2354.0
    assert meter.block2_price == 0.132600
    assert meter.block2_threshold == 2354.0

