import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font_size = 24  # (TK) Adjust the font size as needed.

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

#(TK) added buttons as input
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

#(TK) Images
image1 = Image.open("images/image1.jpg")
image1 = image1.resize((width, height))
image2 = Image.open("images/image2.jpg")
image2 = image2.resize((width, height))
pika = Image.open("images/pikachu3.jpg")
pika = pika.resize((width, height))

while True:
    # Draw a black filled box to clear the image.
    #draw.rectangle((0, 0, width, height), outline=0, fill=5000)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 

    # Get the current date.
    current_date = time.strftime("%m/ %d/ %Y")
    current_time = time.strftime("%H:%M:%S")
    
    # Get the current time.
    current_weekday = time.strftime("%A")
    current_hours = time.strftime('%H: hours')
    current_minutes = time.strftime('%M: mins')
    current_seconds = time.strftime('%S seconds')
    
    #draw.text((40, 10), current_date, fill=(255, 255, 255), font=font)
    #draw.text((40, 35), current_hours, fill=(255, 255, 255), font=font)
    #draw.text((40, 60), current_minutes, fill=(255, 255, 255), font=font)
    #draw.text((40, 85), current_seconds, fill=(255, 255, 255), font=font)
        
    if not buttonA.value:
        display_image = image1.copy()
        draw_on_image = ImageDraw.Draw(display_image)
        draw_on_image.text((50, 50), current_weekday, font=font, fill="#FFFFFF")        
        # Display the modified images with the time on the screen
        disp.image(display_image, rotation)
        continue       

    elif not buttonB.value:
        display_image = image2.copy()
        draw_on_image = ImageDraw.Draw(display_image)
        draw_on_image.text((40, 10), current_date, font=font, fill="#FFFFFF")
        draw_on_image.text((40, 35), current_hours, font=font, fill="#FFFFFF")
        draw_on_image.text((40, 60), current_minutes, font=font, fill="#FFFFFF")
        draw_on_image.text((40, 85), current_seconds, font=font, fill="#FFFFFF")
    
        # Display the modified images with the time on the screen
        disp.image(display_image, rotation)
        continue
        
    else:
        display_image = pika.copy()
        draw_on_image = ImageDraw.Draw(display_image)
        disp.image(display_image, rotation)
        continue


    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)
