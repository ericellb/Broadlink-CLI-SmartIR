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


def loadConfig():
    with open('config.json') as f:
        config = json.load(f)
    return config


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


def saveConfig(config: dict, deviceType: str):
    fileName = f'./out/config_{deviceType}-{time.time()}.json'
    with open(fileName, 'w') as f:
        json.dump(config, f, indent=4)


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

    if deviceType == DeviceType.MEDIA.name:
        media = MediaDevice(device, config, logger)
        outputConfig = media.learn()

    # Save the output file
    saveConfig(outputConfig, deviceType)


main()
