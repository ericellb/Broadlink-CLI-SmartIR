# Broadlink CLI - SmartIR

The goal of this tool was to provide an easy way to learn ALL codes for a suitable device to use with [SmartIR](https://github.com/smartHomeHub/SmartIR) and [Home Assistant](https://www.home-assistant.io/). Check out the demo, you'll see how easy it is.

https://github.com/ericellb/Broadlink-CLI-SmartIR/assets/6540524/9cc76cf1-067a-4d1a-b1a2-269df2b7ded0

## Motivation

This tool is a replacement for [BroadlinkIRTools](https://github.com/keitetran/BroadlinkIRTools) or [broadlinkmanager-docker](https://github.com/t0mer/broadlinkmanager-docker) 

The first tool `BroadlinkIRTools` was broken at the time of creating this, as it would attempt to use `broadlink.learn` via Home Assistant to learn the codes. This has been deprecated and replaced with `remote.learn` this broke the tool completely, sad because it did exactly what I sought out to do here along with a UI...

The second tool is great, however you must learn one code at a time, then you must manually copy them to a json file and fill out a ton more info to make it compatible with SmartIR.


## Installation

```
pip3 install -r requirements.txt
```

## Usage

Run the following and follow along, I swear to you its easy!

```
python src/main.py
```

## Inspiration

Inspiration to make this came from the following
- https://github.com/mjg59/python-broadlink
- https://github.com/smartHomeHub/SmartIR
- https://github.com/keitetran/BroadlinkIRTools
- https://github.com/t0mer/broadlinkmanager-docker
