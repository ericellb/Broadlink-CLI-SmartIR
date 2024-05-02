from enum import Enum
import base64
import codecs
import time
import broadlink
from broadlink.exceptions import ReadError, StorageError


class DeviceType(Enum):
    CLIMATE = 1
    MEDIA = 2
    FAN = 3


def async_learn(device: broadlink.Device):
    device.enter_learning()
    start = time.time()
    TIMEOUT = 600
    while time.time() - start < TIMEOUT:
        time.sleep(1)
        try:
            data = device.check_data()
        except (ReadError, StorageError):
            continue
        else:
            break

    # Format the data properly for SmartIR
    data = ''.join(format(x, '02x') for x in bytearray(data))
    decode_hex = codecs.getdecoder("hex_codec")
    return base64.b64encode(decode_hex(data)[0]).decode('utf-8')


def validateNumber(value):
    if value.isdigit():
        return True
    else:
        return "Please enter a valid number."
