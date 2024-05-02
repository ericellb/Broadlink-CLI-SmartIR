# Broadlink CLI Learn

This tool is a replacement for https://github.com/keitetran/BroadlinkIRTools/tree/master or https://github.com/t0mer/broadlinkmanager-docker. It is meant to provide an easy way to learn IR codes for the Broadlink RM4 + RM4 Mini to use with SmartIR in Home Assistant.

This tool was written, as no other tools allow you to easily learn codes, and create the required output file for SmartIR. All other solutions require you to learn codes 1 at a time, and manually add them to a JSON file compatible with Smart IR.

## Installation

```
pip3 install -r requirements.txt
```

## Usage

The `config.json` file is the main entry path to learning IR codes. A default configuration is included, and you should modify the component that you are interested in using. (`CLIMATE`, `FAN`, `MEDIA`, `OTHER`)

### Climate Setup

- Modify the `Manufacturer` to the what your device brand is
- Modify the `Supported Models` to your model, and all other models that work
- Modify the `climate` section
  - Set the `minTemperature` and `maxTemperature` of your device
  - Set the `Operations Modes` of what your device supports (`cool`, `heat`, `heat_cool`, `fan_only`, `dry`)
  - Set the Fan Modes that your device supports. (Standard naming is `auto`, `level1`, `level2`, `level3`, `level5`, `silent`) (P.S. You can add up to `level10`)

### Fan Setup

- Modify the `Manufacturer` to the what your device brand is
- Modify the `Supported Models` to your model, and all other models that work
- Modify the `fan` section
  - Set the `Operations Modes` of what your device supports. Leave this blank unless your fan supports forward + reverse, if so fill it with [`forward`, `reverse`]
  - Set the `Fan Modes` that your device supports. (Standard naming is `auto`, `level1`, `level2`, `level3`, `level5`, `silent`) (P.S. You can add up to `level10`)
