#!/usr/bin/env python
import os

from argparse import ArgumentParser

import dbus

import evdev
from evdev import UInput
from evdev.ecodes import EV_KEY, KEY_VOLUMEUP, KEY_VOLUMEDOWN


INPUT_DEVICE_PATH = '/dev/input/by-path/'
INPUT_DEVICE_PREFIX = 'platform-gpio-keys'

GBUS_SENSORS_IFACE = 'net.hadess.SensorProxy'
GBUS_SENSORS_OBJ = '/net/hadess/SensorProxy'
GBUS_SENSOR_PROP_ACCEL = 'AccelerometerOrientation'


def is_gpio_volume_input(dev):
    keys = dev.capabilities().get(EV_KEY)
    if keys is None:
        return False

    return KEY_VOLUMEUP in keys and KEY_VOLUMEDOWN in keys


def find_gpio_volume_input():
    for dev_name in os.listdir(INPUT_DEVICE_PATH):
        if dev_name.startswith(INPUT_DEVICE_PREFIX):
            dev = evdev.InputDevice(INPUT_DEVICE_PATH + dev_name)

            if is_gpio_volume_input(dev):
                return dev

    return None


def translate(ev, iio_props):
    if invert_buttons(iio_props):
        if ev.type == EV_KEY:
            if ev.code == KEY_VOLUMEUP:
                ev.code = KEY_VOLUMEDOWN
            elif ev.code == KEY_VOLUMEDOWN:
                ev.code = KEY_VOLUMEUP

    return ev


def invert_buttons(iio_props):
    orientation = iio_props.Get(GBUS_SENSORS_IFACE, GBUS_SENSOR_PROP_ACCEL)
    return orientation in ['normal', 'right-up']


def handle_events(dev, iio_props):
    ui = UInput()
    dev.grab()
    for ev in dev.read_loop():
        ui.write_event(translate(ev, iio_props))


def main():
    cli = ArgumentParser(description='Remap volume button events based on device orientation.')
    cli.add_argument('-d', '--device', metavar='D', help='input device to use')
    args = cli.parse_args()

    if args.device is None:
        dev = find_gpio_volume_input()
        if dev is None:
            print('error: could not find default volume gpio-keys device')
    else:
        dev = evdev.InputDevice(args.device)

    bus = dbus.SystemBus()
    iio = bus.get_object(GBUS_SENSORS_IFACE, GBUS_SENSORS_OBJ)
    iio_props = dbus.Interface(iio, 'org.freedesktop.DBus.Properties')

    handle_events(dev, iio_props)


if __name__ == '__main__':
    main()
