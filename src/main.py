import broadlink
import json
import time
import logging
from typing import List
from climate import ClimateDevice
from fan import FanDevice
from device import DeviceType
from tabulate import tabulate
import os


def scanDevices():
    devices = []
    print('Scanning for devices...\n')
    for device in broadlink.xdiscover():
        devices.append(device)

    if len(devices) == 0:
        print('No devices found')
        exit()

    return devices


def showAndSelectDevice(devices: List[broadlink.Device]) -> broadlink.Device:
    tableData = []
    for idx, device in enumerate(devices):
        tableData.append([idx, device.host[0]])

    print(tabulate(tableData, headers=['ID', 'Device IP'], numalign="left"))

    deviceId = int(input('Select by Device ID: '))
    device = devices[deviceId]

    # Currently only support RM4 Pro + RM4 Mini
    if 'rm4' not in device.model.lower():
        print(f'Invalid Device - {device.model} is not supported')
        exit()

    print(f'Selected Device: {device.host[0]}\n\n')
    device.auth()
    return device


def selectDeviceType() -> DeviceType:
    deviceTypes = []
    print('Select the device type')
    for idx, deviceType in enumerate(DeviceType):
        deviceTypes.append([idx, deviceType.name])

    print(tabulate(deviceTypes, headers=['ID', 'Type'], numalign="left"))

    deviceTypeId = -1
    while deviceTypeId < 0 or deviceTypeId >= len(deviceTypes):
        deviceTypeId = int(input('Enter the Device Type ID: '))
        if deviceTypeId < 0 or deviceTypeId >= len(deviceTypes):
            print('Invalid Device Type - Try again')

    return deviceTypes[deviceTypeId][1]


def loadConfig():
    with open('config.json') as f:
        config = json.load(f)
    return config


def saveConfig(config: dict, deviceType: str):
    fileName = f'./out/config_{deviceType}-{time.time()}.json'
    with open(fileName, 'w') as f:
        json.dump(config, f, indent=4)


def getLogger():
    configLogLevel = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=logging._nameToLevel[configLogLevel])
    return logging.getLogger(__name__)


def main():
    config = loadConfig()
    logger = getLogger()
    devices = scanDevices()
    device = showAndSelectDevice(devices)
    deviceType = selectDeviceType()

    # Call the appropriate device class to learn
    if deviceType == DeviceType.CLIMATE.name:
        climate = ClimateDevice(device, config, logger)
        outputConfig = climate.learn()

    if deviceType == DeviceType.FAN.name:
        fan = FanDevice(device, config, logger)
        outputConfig = fan.learn()

    # Save the output file
    saveConfig(outputConfig, deviceType)


main()
