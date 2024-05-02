
from enum import Enum
import json
import broadlink
import logging
from helpers import async_learn
from typing import Union


class FanOperationModes(Enum):
    OFF = 'off'
    FORWARD = 'forward'
    REVERSE = 'reverse'


class FanSpeedModes(Enum):
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


class FanDevice:
    def __init__(self, device: Union[broadlink.rm4pro, broadlink.rm4mini], config: dict, logger: logging.Logger):
        self.device = device
        self.fanModes = config['fan']['fanModes']
        self.operationModes = config['fan']['operationModes']
        self.logger = logger

        # Validate that the fanOperationModes are part of the enum
        for operationMode in self.operationModes:
            if operationMode not in [mode.value for mode in FanOperationModes]:
                raise ValueError(f'Invalid Operation Mode: {operationMode}')

        # Validate that the fanSpeedmodes are part of the enum
        for fanMode in self.fanModes:
            if fanMode not in [mode.value for mode in FanSpeedModes]:
                raise ValueError(f'Invalid Speed Mode: {fanMode}')

        self.outputConfig = self._buildBaseOutputConfig(config)

    def _buildBaseOutputConfig(self, config: dict):
        # Build the base output config
        outputConfig = {}
        outputConfig['manufacturer'] = config['device']['manufacturer']
        outputConfig['supportedModels'] = config['device']['supportedModels']
        outputConfig['supportedController'] = 'Broadlink'
        outputConfig['commandsEncoding'] = 'Base64'
        outputConfig['speed'] = self.fanModes
        outputConfig['commands'] = {}

        # Forward / Reverse can be set, if not we need to set it to default
        if self.operationModes == []:
            self.operationModes = ['default']

        # Build the base config for each operation mode
        for operationMode in self.operationModes:
            outputConfig['commands'][operationMode] = {}
            for fanMode in self.fanModes:
                outputConfig['commands'][operationMode][fanMode] = {}

        return outputConfig

    def _learnCommand(self, operationMode: str, fanMode: str):
        if (operationMode and fanMode):
            print(f'Learning {operationMode.upper()} {fanMode.upper()} - Point the remote to the device and press the button')
        elif (operationMode):
            print(f'Learning {operationMode.upper()} - Point the remote to the device and press the button')

        command = async_learn(self.device)

        choice = input(f'Press Enter or Y to confirm or N to re-learn Command - {command}\n')

        if choice.lower() == 'y' or choice == '':
            return self._writeCommandToConfig(command, operationMode, fanMode)
        else:
            return self._learnCommand(operationMode, fanMode)

    def _writeCommandToConfig(self, command: str, operationMode: str, fanMode: str):
        if operationMode and fanMode:
            self.outputConfig['commands'][operationMode][fanMode] = command
        elif operationMode:
            self.outputConfig['commands'][operationMode] = command

    def learn(self):
        # Learn the OFF Command
        self._learnCommand(FanOperationModes.OFF.name.lower(), None)
        self.logger.debug(json.dumps(self.outputConfig, indent=4))

        for operationMode in self.operationModes:
            for fanMode in self.fanModes:
                self._learnCommand(operationMode, fanMode)
                self.logger.debug(json.dumps(self.outputConfig, indent=4))

        return self.outputConfig
