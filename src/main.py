import pygame
import vgamepad as vg

# map player to pygame controller instance_ids 
RIGHT_PLAYER = 0  
LEFT_PLAYER = 1

# Define the button mappings
BUTTON_MAPPING = {
    RIGHT_PLAYER: {
        pygame.CONTROLLER_BUTTON_A: vg.DS4_BUTTONS.DS4_BUTTON_CROSS,
        pygame.CONTROLLER_BUTTON_B: vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,
        pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,
        pygame.CONTROLLER_BUTTON_START: vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS,
        pygame.CONTROLLER_BUTTON_RIGHTSTICK: vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,
        pygame.CONTROLLER_BUTTON_DPAD_UP: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
        pygame.CONTROLLER_BUTTON_DPAD_LEFT: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
    },
    LEFT_PLAYER: {
        pygame.CONTROLLER_BUTTON_X: vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,
        pygame.CONTROLLER_BUTTON_Y: vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,
        pygame.CONTROLLER_BUTTON_LEFTSHOULDER: vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,
        pygame.CONTROLLER_BUTTON_LEFTSTICK: vg.DS4_BUTTONS.DS4_BUTTON_THUMB_LEFT,
        pygame.CONTROLLER_BUTTON_DPAD_DOWN: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
        pygame.CONTROLLER_BUTTON_DPAD_RIGHT: vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
    }
}

# use this to look up whether or not a button mapping should use the direction system
DPAD_IDS = [
        vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH,
        vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST,
        vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH,
        vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST,
]

def initialize_gamepad():
    pygame.init()
    pygame.joystick.init()
    
    # Check the number of available gamepads
    num_joysticks = pygame.joystick.get_count()
    if num_joysticks < 2:
        print("Connect at least two gamepads.")
        pygame.quit()
        exit()

    # Initialize the first two gamepads
    joystick1 = pygame.joystick.Joystick(0)
    joystick2 = pygame.joystick.Joystick(1)

    joystick1.init()
    joystick2.init()

    return joystick1, joystick2

def map_gamepad_inputs(virtual):
    leftStickX = 0
    leftStickY = 0
    rightStickX = 0
    rightStickY = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
                try:
                    mapping = BUTTON_MAPPING[event.instance_id][event.button]
                    if mapping in DPAD_IDS:
                        virtual.directional_pad(direction=mapping)
                    else:
                        virtual.press_button(button = mapping)
                except:
                    pass
                pass

            if event.type == pygame.JOYBUTTONUP:
                try:
                    mapping = BUTTON_MAPPING[event.instance_id][event.button]
                    if mapping in DPAD_IDS:
                        virtual.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE)
                    else:
                        virtual.release_button(button = mapping)
                except:
                    pass
                pass

            # Handle axis motion events
            if event.type == pygame.JOYAXISMOTION:
                # Map axis motion events to the virtual gamepad
                if event.instance_id == LEFT_PLAYER:
                    if event.axis == pygame.CONTROLLER_AXIS_TRIGGERLEFT:
                        virtual.left_trigger_float(value_float = event.value)
                    if event.axis == pygame.CONTROLLER_AXIS_LEFTX:
                        leftStickX = event.value
                    if event.axis == pygame.CONTROLLER_AXIS_LEFTY:
                        leftStickY = event.value
                if event.instance_id == RIGHT_PLAYER:
                    if event.axis == pygame.CONTROLLER_AXIS_TRIGGERRIGHT:
                        virtual.right_trigger_float(value_float = event.value)
                    if event.axis == pygame.CONTROLLER_AXIS_RIGHTX:
                        rightStickX = event.value
                    if event.axis == pygame.CONTROLLER_AXIS_RIGHTY:
                        rightStickY = event.value
                pass  # Add your logic here
        
        virtual.left_joystick_float(x_value_float=leftStickX, y_value_float=leftStickY)
        virtual.right_joystick_float(x_value_float=rightStickX, y_value_float=rightStickY)
        virtual.update()

def main():
    # need to hold onto these to keep them alive
    joystick1, joystick2 = initialize_gamepad()
    virtual_gamepad = vg.VDS4Gamepad()
    map_gamepad_inputs(virtual_gamepad)

if __name__ == "__main__":
    main()
