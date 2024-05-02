
from enum import Enum
import json
import broadlink
import logging
from device import async_learn
from typing import Union


class ClimateOperationModes(Enum):
    OFF = 'off'
    COOL = 'cool'
    HEAT = 'heat'
    HEAT_COOL = 'heat_cool'
    FAN = 'fan_only'
    DRY = 'dry'


class ClimateFanModes(Enum):
    AUTO = 'auto'
    LEVEL1 = 'level1'
    LEVEL2 = 'level2'
    LEVEL3 = 'level3'
    LEVEL4 = 'level4'
    LEVEL5 = 'level5'
    LEVEL6 = 'level6'
    LEVEL7 = 'level7'
    LEVEL8 = 'level8'
    LEVEL9 = 'level9'
    LEVEL10 = 'level10'


class ClimateDevice:
    def __init__(self, device: Union[broadlink.rm4pro, broadlink.rm4mini], config: dict, logger: logging.Logger):
        self.device = device
        self.tempMin = config['climate']['minTemperature']
        self.tempMax = config['climate']['maxTemperature']
        self.fanModes = config['climate']['fanModes']
        self.operationModes = config['climate']['operationModes']
        self.precision = config['climate']['precision']
        self.logger = logger

        # Validate that the fanModes are part of the enum
        for fanMode in self.fanModes:
            if fanMode not in [mode.value for mode in ClimateFanModes]:
                raise ValueError(f'Invalid Fan Mode: {fanMode}')

        # Validate that the operationModes are part of the enum
        for operationMode in self.operationModes:
            if operationMode not in [mode.value for mode in ClimateOperationModes]:
                raise ValueError(f'Invalid Operation Mode: {operationMode}')

        self.outputConfig = self._buildBaseOutputConfig(config)

    def _buildBaseOutputConfig(self, config: dict):
        # Build the base output config
        outputConfig = {}
        outputConfig['manufacturer'] = config['device']['manufacturer']
        outputConfig['supportedModels'] = config['device']['supportedModels']
        outputConfig['supportedController'] = 'Broadlink'
        outputConfig['commandsEncoding'] = 'Base64'
        outputConfig['minTemperature'] = self.tempMin
        outputConfig['maxTemperature'] = self.tempMax
        outputConfig['precision'] = self.precision
        outputConfig['operationModes'] = self.operationModes
        outputConfig['fanModes'] = self.fanModes
        outputConfig['commands'] = {}

        # Build the base config for each operation mode
        for operationMode in self.operationModes:
            outputConfig['commands'][operationMode] = {}
            for fanMode in self.fanModes:
                outputConfig['commands'][operationMode][fanMode] = {}
                for temp in range(self.tempMin, self.tempMax + 1):
                    outputConfig['commands'][operationMode][fanMode][str(temp)] = ''

        return outputConfig

    def _learnCommand(self, operationMode: str, fanMode: str, temp: int):
        if (operationMode and fanMode and temp):
            print(f'Learning {operationMode.upper()} {fanMode.upper()} {str(temp).upper()}° - Point the remote to the device and press the button')
        elif (operationMode and fanMode):
            print(f'Learning {operationMode.upper()} {fanMode.upper()} - Point the remote to the device and press the button')
        elif (operationMode):
            print(f'Learning {operationMode.upper()} - Point the remote to the device and press the button')

        command = async_learn(self.device)

        choice = input(f'Press Enter or Y to confirm or N to re-learn Command - {command}\n')

        if choice.lower() == 'y' or choice == '':
            return self._writeCommandToConfig(command, operationMode, fanMode, temp)
        else:
            return self._learnCommand(operationMode, fanMode, temp)

    def _writeCommandToConfig(self, command: str, operationMode: str, fanMode: str, temp: int):
        if operationMode and fanMode and temp:
            self.outputConfig['commands'][operationMode][fanMode][str(temp)] = command
        elif operationMode and fanMode:
            self.outputConfig['commands'][operationMode][fanMode] = command
        elif operationMode:
            self.outputConfig['commands'][operationMode] = command

    def learn(self):
        # Learn the OFF Command
        self._learnCommand(ClimateOperationModes.OFF.name.lower(), None, None)
        self.logger.debug(json.dumps(self.outputConfig, indent=4))

        # Learn each temperature at each fanMode and operationMode
        for operationMode in self.operationModes:
            for fanMode in self.fanModes:
                for temp in range(self.tempMin, self.tempMax + 1):
                    self._learnCommand(operationMode, fanMode, temp)
                    self.logger.debug(json.dumps(self.outputConfig, indent=4))

        return self.outputConfig
