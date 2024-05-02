# Broadlink CLI Learn

This tool is a replacement for https://github.com/keitetran/BroadlinkIRTools/tree/master or https://github.com/t0mer/broadlinkmanager-docker. It is meant to provide an easy way to learn IR codes for the Broadlink RM4 + RM4 Mini to use with SmartIR in Home Assistant.

This tool was written, as no other tools allow you to easily learn codes, and create the required output file for SmartIR. All other solutions require you to learn codes 1 at a time, and manually add them to a JSON file compatible with Smart IR.

## Installation

```
pip3 install -r requirements.txt
```

## Usage

The `config.json` file is the main entry path to learning IR codes. Here you should setup the basic information that will be used to create the final SmartIR compatible JSON file.

- Modify the `Manufactuer` to the what your device brand is
- Modify the `Supported Models` to your model, and all other models that work
- Modify the `climate` section
  - Set the minimum and maximum temperatures of your device
  - Fill out your devices supported Operations Modes (`cool`, `heat`, `heat_cool`, `fan_only`, `dry`)
  - Fill out your devices supported Fan Modes (These can be named whatever you want. However standard is `auto`, `level1`, `level2`, `level3`, `level5`, `silent`. P.S more can be added)

Now you are ready to run the script and follow the instructions!
```
python src/main.py
```
