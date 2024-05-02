
from enum import Enum
import json
import broadlink
import logging
from helpers import async_learn
from typing import List, Union
import questionary


class FanOperationModes(Enum):
    OFF = 'off'
    DEFAULT = 'default'
    FORWARD = 'forward'
    REVERSE = 'reverse'


class FanOperationHelper(Enum):
    ONE_DIRECTION = 'one_direction'
    FORWARD_REVERSE = 'forward_reverse'


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
    def __init__(self, device: Union[broadlink.rm4pro, broadlink.rm4mini], manufacturer: str, supportedModels: List[str], logger: logging.Logger):
        self.device = device
        self.operationModes = self._promptOperationModes()
        self.fanModes = self._promptFanModes()
        self.logger = logger
        self.outputConfig = self._buildBaseOutputConfig(manufacturer, supportedModels)

    def _promptOperationModes(self):
        operationModes = [operationMode.value for operationMode in FanOperationHelper]

        selectedOperationModes = questionary.select(
            'Select Operation Modes (Most fans are one direction)',
            choices=operationModes
        ).ask()

        if selectedOperationModes == FanOperationHelper.ONE_DIRECTION.value:
            return [FanOperationModes.DEFAULT.value]
        else:
            return [FanOperationModes.FORWARD.value, FanOperationModes.REVERSE.value]

    def _promptFanModes(self):
        selectedFanModes = questionary.checkbox(
            'Select Fan Modes (Number of speeds supported)',
            choices=[fanMode.value for fanMode in FanSpeedModes]
        ).ask()

        return selectedFanModes

    def _buildBaseOutputConfig(self, manufacturer: str, supportedModels: List[str]):
        # Build the base output config
        outputConfig = {}
        outputConfig['manufacturer'] = manufacturer
        outputConfig['supportedModels'] = supportedModels
        outputConfig['supportedController'] = 'Broadlink'
        outputConfig['commandsEncoding'] = 'Base64'
        outputConfig['speed'] = self.fanModes
        outputConfig['commands'] = {}

        # Build the base config for each operation mode
        for operationMode in self.operationModes:
            outputConfig['commands'][operationMode] = {}
            for fanMode in self.fanModes:
                outputConfig['commands'][operationMode][fanMode] = {}

        return outputConfig

    def _learnCommand(self, operationMode: str, fanMode: str):
        if (operationMode and fanMode):
            if operationMode == FanOperationModes.DEFAULT.value:
                print(f'Learning Speed {fanMode.upper()}')
            else:
                print(f'Learning {operationMode.upper()} Speed {fanMode.upper()}')
        elif (operationMode):
            print(f'Learning {operationMode.upper()}')

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
        print('\nYou will now be prompted to press the corresponding button on the remote for each command\n')

        # Learn the OFF Command
        self._learnCommand(FanOperationModes.OFF.name.lower(), None)
        self.logger.debug(json.dumps(self.outputConfig, indent=4))

        for operationMode in self.operationModes:
            for fanMode in self.fanModes:
                self._learnCommand(operationMode, fanMode)
                self.logger.debug(json.dumps(self.outputConfig, indent=4))

        return self.outputConfig
