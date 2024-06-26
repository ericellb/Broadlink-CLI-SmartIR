
from enum import Enum
import json
import broadlink
import logging
from helpers import async_learn
from typing import List, Union
import questionary


class MediaCommands(Enum):
    OFF = 'off'
    ON = 'on'
    PREVIOUS_CHANNEL = 'previousChannel'
    NEXT_CHANNEL = 'nextChannel'
    VOLUME_UP = 'volumeUp'
    VOLUME_DOWN = 'volumeDown'
    MUTE = 'mute'


class MediaDevice:
    def __init__(self, device: Union[broadlink.rm4pro, broadlink.rm4mini], manufacturer: str, supportedModels: List[str], logger: logging.Logger):
        self.device = device
        self.sources = self._promptMediaSources()
        self.logger = logger
        self.outputConfig = self._buildBaseOutputConfig(manufacturer, supportedModels)

    def _promptMediaSources(self):
        mediaSources = questionary.text('Enter Media Source names (comma separated)').ask()
        if ',' in mediaSources:
            mediaSources = mediaSources.split(',')
        else:
            mediaSources = [mediaSources]

        return mediaSources

    def _buildBaseOutputConfig(self, manufacturer: str, supportedModels: List[str],):
        # Build the base output config
        outputConfig = {}
        outputConfig['manufacturer'] = manufacturer
        outputConfig['supportedModels'] = supportedModels
        outputConfig['supportedController'] = 'Broadlink'
        outputConfig['commandsEncoding'] = 'Base64'
        outputConfig['commands'] = {}
        outputConfig['commands']['sources'] = {}

        # Build the base config for each Media Command
        for command in MediaCommands:
            outputConfig['commands'][command.value] = ""

        # Build the base config for each source
        for source in self.sources:
            outputConfig['commands']['sources'][source] = ""

        return outputConfig

    def _learnCommand(self, key: str, nestedKey: str):
        if key and nestedKey:
            print(f'Learning {key.upper()} {nestedKey.upper()} - Point the remote to the device and press the button')
        elif key:
            print(f'Learning {key.upper()} - Point the remote to the device and press the button')

        command = async_learn(self.device)

        choice = input(f'Press Enter or Y to confirm or N to re-learn Command - {command}\n')

        if choice.lower() == 'y' or choice == '':
            return self._writeCommandToConfig(command, key, nestedKey)
        else:
            return self._learnCommand(key, nestedKey)

    def _writeCommandToConfig(self, command: str, key: str, nestedKey: str):
        if key and nestedKey:
            self.outputConfig['commands'][key][nestedKey] = command
        elif key:
            self.outputConfig['commands'][key] = command

    def learn(self):
        # Learn the media commands
        for command in MediaCommands:
            self._learnCommand(command.value, None)

        # Learn the sources
        for source in self.sources:
            self._learnCommand('sources', source)
            self.logger.debug(json.dumps(self.outputConfig, indent=4))

        return self.outputConfig
