#!/usr/bin/env python3
# Author: Nathanaël Mautard
import argparse
import time
import asyncio
import telepot
import telepot.aio
import RPi.GPIO as GPIO


def get_args():
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description="Telegram LED alerting script - GPIO work in BCM mode",
        usage='use "./%(prog)s --help" for more information')
    # Add arguments
    parser.add_argument(
        '-l', '--ledsGPIO', type=str, help='List of GPIO pins used by LEDs, values sparated by commas.',
        required=True, nargs='+')
    parser.add_argument(
        '-b', '--buttonGPIO', type=int, help='GPIO pin number of button.', required=True)
    parser.add_argument(
        '-s', '--speed', type=float, help='Blink speed in seconds. (e.g.: 0.5 for 500ms) ', required=True)
    parser.add_argument(
        '-t', '--token', type=str, help='Telegram bot token', required=True)
    parser.add_argument(
        '-g', '--groupid', type=int, help='Telegram group ID', required=True)
    parser.add_argument(
        '-u', '--userid', type=int,
        help='Telegram ID of user sending messages - Optional. If you don\'t enter userid'
             ', alerts going to start whatever '
             'the user who will send a message in the group ', required=False)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    l = [int(x) for x in args.ledsGPIO[0].split(",")]
    b = args.buttonGPIO
    s = args.speed
    t = args.token
    g = args.groupid
    u = args.userid
    # Return all variable values
    return l, b, s, t, g, u


class TheBot(telepot.aio.Bot):
    @asyncio.coroutine
    async def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(chat_type, chat_id, msg.get('text'), msg.get('from')['id'])
        input_state = 1
        if GPIO.input(buttonGPIO) == 1 and chat_id == groupid and (msg.get('from')['id'] == userid
                                                                   if userid is not None else 1):
            try:
                await bot.sendMessage(chat_id, "Alert started !")
                start = time.time()
                while input_state == 1:
                    input_state = GPIO.input(buttonGPIO)
                    for x in range(len(ledsGPIO)):
                        GPIO.output(ledsGPIO[x], GPIO.HIGH)
                    time.sleep(blinkSpeed)
                    for y in range(len(ledsGPIO)):
                        GPIO.output(ledsGPIO[y], GPIO.LOW)
                    time.sleep(blinkSpeed)
                    elapsed = int(time.time() - start)
                    if elapsed % 60 == 0 and elapsed is not 0:
                        minutes = str(int(elapsed / 60))
                        str_minutes = " minute" if minutes == "1" else " minutes"
                        await bot.sendMessage(chat_id, "The alert is active for " + minutes + str_minutes)
            except KeyboardInterrupt:
                for y in range(len(ledsGPIO)):
                    GPIO.output(ledsGPIO[y], GPIO.LOW)
                GPIO.cleanup()
            if input_state == 0:
                for y in range(len(ledsGPIO)):
                    GPIO.output(ledsGPIO[y], GPIO.LOW)
                await bot.sendMessage(chat_id, "Alert stopped !")


ledsGPIO, buttonGPIO, blinkSpeed, token, groupid, userid = get_args()

print(get_args())
# Prepare GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for led in range(len(ledsGPIO)):
    GPIO.setup(ledsGPIO[led], GPIO.OUT)
    GPIO.output(ledsGPIO[led], GPIO.LOW)
GPIO.setup(buttonGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

bot = TheBot(token)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())
print('Listening...')

loop.run_forever()

