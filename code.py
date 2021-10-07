# Daniel Flores
# Pokemon Project - Stage and Pokemon
import board
import neopixel
import time
import digitalio
import touchio
import pwmio
import random


from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.color import (
    AMBER,  # (255, 100, 0)
    AQUA,  # (50, 255, 255)
    BLACK,  # OFF (0, 0, 0)
    BLUE,  # (0, 0, 255)
    CYAN,  # (0, 255, 255)
    GOLD,  # (255, 222, 30)
    GREEN,  # (0, 255, 0)
    JADE,  # (0, 255, 40)
    MAGENTA,  # (255, 0, 20)
    OLD_LACE,  # (253, 245, 230)
    ORANGE,  # (255, 40, 0)
    PINK,  # (242, 90, 255)
    PURPLE,  # (180, 0, 255)
    RED,  # (255, 0, 0)
    TEAL,  # (0, 255, 120)
    WHITE,  # (255, 255, 255)
    YELLOW,  # (255, 150, 0)
    RAINBOW,  # a list of colors to cycle through
    # RAINBOW is RED, ORANGE, YELLOW, GREEN, BLUE, and PURPLE ((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255))
)

from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile
from adafruit_motor import servo


audio = AudioOut(board.AUDIO)

path = "drumSounds/"

pixels_pin = board.NEOPIXEL
pixels_num_of_lights = 10
pixels = neopixel.NeoPixel(
    pixels_pin, pixels_num_of_lights, brightness=0.5, auto_write=True
)

strip_pin = board.A1
strip_num_of_lights = 30
strip = neopixel.NeoPixel(
    strip_pin, strip_num_of_lights, brightness=0.5, auto_write=True
)

INDIGO = (75, 0, 130)
VIOLET = (127, 0, 255)
colors = [
    RED,
    MAGENTA,
    ORANGE,
    YELLOW,
    GREEN,
    JADE,
    BLUE,
    INDIGO,
    VIOLET,
    PURPLE,
    BLACK,
]

# initialize animation
# Pikachu
comet = Comet(pixels, speed=0.05, color=YELLOW, tail_length=10, bounce=True)
comet_strip = Comet(
    strip,
    speed=0.05,
    color=YELLOW,
    tail_length=int(strip_num_of_lights / 4),
    bounce=True,
)
# Charmander
blink = Blink(pixels, speed=0.5, color=RED)
blink_strip = Blink(strip, speed=0.5, color=RED)
# Squirtle
pulse = Pulse(pixels, speed=0.05, color=BLUE, period=2)
pulse_strip = Pulse(strip, speed=0.05, color=BLUE, period=2)
# Eevee
sparkle_pulse = SparklePulse(pixels, speed=0.05, period=5, color=WHITE)
sparkle_pulse_strip = SparklePulse(strip, speed=0.05, period=5, color=WHITE)
# Bulbasaur
chase = Chase(pixels, speed=0.1, color=JADE, size=3, spacing=6)
chase_strip = Chase(strip, speed=0.1, color=JADE, size=1, spacing=1)


# capacitive touch for each pokemon
touchpad_A2 = touchio.TouchIn(board.A2)
touchpad_A3 = touchio.TouchIn(board.A3)
touchpad_A4 = touchio.TouchIn(board.A4)
touchpad_A5 = touchio.TouchIn(board.A5)
touchpad_A6 = touchio.TouchIn(board.A6)

# initialize servo motor
pwm = pwmio.PWMOut(board.TX, frequency=50)
servo_1 = servo.Servo(pwm, max_pulse=2370)


def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

def sound_board(filename):
    wave_file = open(path + filename, "rb")
    wave = WaveFile(wave_file)
    return wave

bulbasaur_sound = sound_board("bulb.wav")
eevee_sound = sound_board("eevee.wav")
char_sound = sound_board("char.wav")
pikachu = sound_board("pika.wav")
squirtle = sound_board("squirtle.wav")

touched = False

while True:
    touch_count = 0
    servo_1.angle = 120
    x = random.randint(0,4)
    if touchpad_A2.value:
        touched = True
        if x == 0:
            touched = True
            #play_sound("char.wav")
            audio.play(char_sound)
            servo_1.angle = 90
            while audio.playing:
                blink_strip.animate()
            strip.fill(BLACK)
        elif x == 1:
            # eevee
            #play_sound("eevee.wav")
            audio.play(eevee_sound)
            servo_1.angle = 60
            while audio.playing:
                sparkle_pulse_strip.animate()
            strip.fill(BLACK)
        elif x == 2:
            # squirtle
            #play_sound("squirtle.wav")
            audio.play(squirtle)
            servo_1.angle = 165
            while audio.playing:
                pulse_strip.animate()
            strip.fill(BLACK)
        elif x == 3:
            # bulbasaur
            #play_sound("bulb.wav")
            audio.play(bulbasaur_sound)
            servo_1.angle = 145
            while audio.playing:
                chase_strip.animate()
            strip.fill(BLACK)
        elif x == 4:
            # pikachu
            #play_sound("pika.wav")
            audio.play(pikachu)
            servo_1.angle = 120
            while audio.playing:
                comet_strip.animate()
            strip.fill(BLACK)
    else:
        strip.fill(BLACK)
