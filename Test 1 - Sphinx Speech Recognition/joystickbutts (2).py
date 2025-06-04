import pygame, json, serial, time, speech_recognition as sr, pyaudio
# speech recognition library to work with speech recognition engines
# import speech_recognition as sr 
# speech recognition = sphinx
# pocketsphinx is installed - pip install pocketsphinx

# To fix the below error
# Error: ModuleNotFoundError: No module named 'distutils' 
# 'distutils' was removed in Python 3.12
# problem fixed by = pip install setuptools

recognizer = sr.Recognizer()


# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for speech...")

        # Capture the audio data
        audio_data = recognizer.listen(source)

        try:
            # Recognize speech using Sphinx
            text = recognizer.recognize_sphinx(audio_data)
            print("You said: " + text)
        except sr.UnknownValueError:
            print("Sphinx could not understand the audio")
        except sr.RequestError as e:
            print(f"Sphinx error; {e}")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

port = 'COM14'
 

class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """ 
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()
throtal = 1000

js_chans = {
    "pitch": 0,
    "roll": 0,
    "yaw": 0,
    "throttle": 0,
    "armed": 0,
    "mode": 0,
    "speed": 0,
}
joystick = pygame.joystick.Joystick(0)

def test(joystick):
 
    vertical = joystick.get_hat(0)[1]
    print(vertical)
    return vertical

# -------- Main Program Loop -----------
with serial.Serial() as ser:
  IS_ARMED = False
  ARMED_LAST = None
  ARMED_INTERVAL_MS = 100
  BUTTON0_DOWN = False
  ser.baudrate = 115200
  ser.port = port
  ser.open()
  print("opening serial port...")
  time.sleep(2)
  print("serial port ready...")
  while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
 
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
            #print(event)
            if event.button == 0:
                
                    IS_ARMED = not IS_ARMED
                    #ARMED_LAST = int(round(time.time()*1000))

        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
   
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()
 
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
 
        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()
 
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))
 
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
 
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
        textPrint.unindent()

        js_chans["roll"] = int((joystick.get_axis(0) * 1000) + 1000)
        js_chans["pitch"] = int((joystick.get_axis(1) * -1000) + 1000)
        js_chans["yaw"] = int((joystick.get_axis(2) * 1000) + 1000)
        js_chans["throttle"] = int((joystick.get_axis(3) * -1000) + 1000)
        #js_chans["armed"] = 1000
        #js_chans["mode"] = 1500
        #js_chans["speed"] = 1500
        if IS_ARMED:
          js_chans["armed"] = 2000
        else:
          js_chans["armed"] = 1000
 


        #print(f'json to send: {js_str}')

        #print("sent to serial port")
        #s = str(ser.readline())
        #print(f'read from serial port: "{s}"')
 
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
 
        NOW = int(round(time.time()*1000))
                
        #   json to send: {"pitch": 1000, "roll": 963, "yaw": 1000, "throttle": 1614, "armed": 1000, "mode": 1500, "speed": 1500}

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {:>2} value: {}".format(i, button))

        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()
 
        for i in range(hats):
            hat = joystick.get_hat(i)[1]
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
            if(hat == 1):
                print("Pushing Up")
                throtal+=20
            elif(hat == -1): 
                print("Pushing Down")
                throtal -= 20
            else:
                throtal = throtal
            if(throtal > 2000):
                throtal = 2000
            elif(throtal < 0):
                throtal = 0
            js_chans["throttle"] = throtal
        textPrint.unindent()
 
        textPrint.unindent()
    
    textPrint.print(screen, "")
    textPrint.print(screen, "========================================")
    textPrint.print(screen, "Armed: {}".format(IS_ARMED))
    textPrint.print(screen, "========================================")
    textPrint.print(screen, "")

    textPrint.print(screen, "========================================")
    textPrint.print(screen, "Channel Data")
    textPrint.print(screen, "========================================")
    textPrint.indent()
    if IS_ARMED:
        js_chans["armed"] = 2000
    else:
        js_chans["armed"] = 1000
    textPrint.print(screen, "[ROLL] : {}".format(js_chans['roll']))
    textPrint.print(screen, "[PITCH] : {}".format(js_chans['pitch']))
    textPrint.print(screen, "[YAW] : {}".format(js_chans['yaw']))
    textPrint.print(screen, "[THROTTLE] : {}".format(js_chans['throttle']))
    textPrint.print(screen, "[ARMED] : {}".format(js_chans['armed']))
    textPrint.print(screen, "========================================")
    textPrint.unindent()
 
    js_str = json.dumps(js_chans) + '\n'
    print(js_str)
    ser.write(bytes(js_str,'utf-8'))

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
# Voice control
voice_command = recognize_speech_from_mic()
if voice_command == "up":
        throtal += 20
        print("Voice command: Up")
elif voice_command == "down":
        throtal -= 20
        print("Voice command: Down")
    
# throttle is within bounds
throtal = min(max(throtal, 0), 2000)
print(f"Throttle: {throtal}")
    
# throttle channel
js_chans = {"throttle": throtal}

# Delay to prevent too frequent voice command checks
pygame.time.wait(1000)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
