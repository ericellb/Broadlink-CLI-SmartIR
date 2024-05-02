import broadlink
import json
import time
import logging
from tabulate import tabulate
from typing import List
from climate import ClimateDevice
from fan import FanDevice
from media import MediaDevice
from helpers import DeviceType
import questionary
import os


def getLogger():
    configLogLevel = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=logging._nameToLevel[configLogLevel])
    return logging.getLogger(__name__)


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
    # Build hashmap of deviceIp to device
    deviceIpToDevice = {}
    deviceHosts = []
    for device in devices:
        deviceIpToDevice[device.host[0]] = device
        deviceHosts.append(device.host[0])

    selectedDeviceIp = questionary.select('Select Device', choices=deviceHosts).ask()

    # Fetch the device from the hashmap
    device = deviceIpToDevice[selectedDeviceIp]

    # Currently only support RM4 Pro + RM4 Mini
    if 'rm4' not in device.model.lower():
        print(f'Invalid Device - {device.model} is not supported')
        exit()

    device.auth()
    return device


def selectDeviceType() -> DeviceType:
    selectedDeviceType = questionary.select('Select Device Type', choices=[deviceType.name for deviceType in DeviceType]).ask()
    return selectedDeviceType


def promptManufacturer():
    manufacturer = questionary.text('Enter Manufacturer').ask()
    return manufacturer


def promptSupportedModels():
    supportedModels = questionary.text('Enter Supported Models Number / Names (comma separated)').ask()
    if ',' in supportedModels:
        supportedModels = supportedModels.split(',')
    else:
        supportedModels = [supportedModels]

    return supportedModels


def saveConfig(config: dict, deviceType: str):
    fileName = f'./out/config_{deviceType}-{time.time()}.json'
    with open(fileName, 'w') as f:
        json.dump(config, f, indent=4)


def main():
    logger = getLogger()
    devices = scanDevices()
    device = showAndSelectDevice(devices)
    deviceType = selectDeviceType()

    manufacturer = promptManufacturer()
    supportedModels = promptSupportedModels()

    # Call the appropriate device class to learn
    if deviceType == DeviceType.CLIMATE.name:
        climate = ClimateDevice(device, manufacturer, supportedModels, logger)
        outputConfig = climate.learn()

    if deviceType == DeviceType.FAN.name:
        fan = FanDevice(device, manufacturer, supportedModels, logger)
        outputConfig = fan.learn()

    if deviceType == DeviceType.MEDIA.name:
        media = MediaDevice(device, manufacturer, supportedModels, logger)
        outputConfig = media.learn()

    # Save the output file
    saveConfig(outputConfig, deviceType)
    print('Finished - Config saved to ./out/ folder\n')


main()
