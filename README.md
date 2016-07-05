# Telegram LED Alerter

LED alerter when there are message received in Telegram group.

The main usage of this alerter is for very important messages, when you work in team for example and if you want to alert other members remotely. To stop the alert, you need to press the button for some seconds or move the switch in the closed state.

Works with RaspberyPi and Pine64 with RPi.GPIO Python libraries in BCM mode.

## Requirements
- Hardware requirements:
  - A RaspberryPi or a Pine64
  - Wires
  - Many LEDs (not RGB) or LED strip ([Tutorial for LED RGB strip](http://popoklopsi.github.io/RaspberryPi-LedStrip))
  - Resistors for LED (from 270Ω to 470Ω, search on the net)
  - A button or switch

- Install requirements:

  ```
  sudo apt-get update
  sudo apt-get install build-essential python3-pip python3-dev git
  pip3.5 install telepot
  ```
  
If the last command fail, you need to compille yourself Pythton 3.5 who is needed for asyncio module.

Python 3.5 is available on Debian testing and Ubuntu 16.04 LTS. To check the Python version installed on system, type ```python3 --version```

- Build Python 3.5:
  
  ```
  sudo apt-get update
  sudo apt-get install libssl-dev openssl libreadline-dev
  cd ~
  wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
  tar zxf Python-3.5.2.tgz
  cd Python-3.5.2
  ./configure
  make
  sudo make install
  pip3.5 install telepot
  ```

- Install [RPi.GPIO for RaspberryPi](https://pypi.python.org/pypi/RPi.GPIO):

  ```
  pip3 install RPi.GPIO
  ```
  
- Or install [RPi.GPIO for Pine64](https://github.com/swkim01/RPi.GPIO-PineA64):

  ```
  git clone https://github.com/swkim01/RPi.GPIO-PineA64.git
  cd RPi.GPIO-PineA64
  sudo python setup.py install
  ```
- [Create your Telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

## How to use

  ```
  cd ~
  git clone https://github.com/Nathanael-Mtd/telegram-led-alerter.git
  cd telegram-led-alerter
  python3 telegramLEDAlert.py -h
  ```

## Script Arguments

  ```
  -l LEDSGPIO [LEDSGPIO ...], --ledsGPIO LEDSGPIO [LEDSGPIO ...]
                        List of GPIO pins used by LEDs, values sparated by commas.
  -b BUTTONGPIO, --buttonGPIO BUTTONGPIO
                        GPIO pin number of button.
  -s SPEED, --speed SPEED
                        Blink speed in seconds. (e.g.: 0.5 for 500ms)
  -t TOKEN, --token TOKEN
                        Telegram bot token
  -g GROUPID, --groupid GROUPID
                        Telegram group ID
  -u USERID, --userid USERID
                        Telegram ID of user sending messages 
                        Optional. If you don't enter userid, alerts going to start 
                        whatever the user who will send a message in the group
  ```
  
## Example
- Simple LEDs version:
 
  ```
  python3 telegramLEDAlert.py -l 17,22,5,12,24,18 -b 26 -s 0.5 -t 2xxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -g -123456789 -u 12345678
  ```
  
- LED strip version:
  
  ```
  python3 telegramLEDstripAlert.py -l 17,22,24 -b 26 -s 0.5 -t 2xxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -g -123456789 -u 12345678
  ```
