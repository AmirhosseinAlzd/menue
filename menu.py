import machine  
import ssd1306  
import time  

# Initialize I2C for OLED display  
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))   
oled = ssd1306.SSD1306_I2C(128, 64, i2c)  

# Main menu items  
menu_items = ["Speed", "Time", "Exit"]  
# Submenu items  
speed_items = ['Fast', 'Medium', 'Slow']  
time_items = ['3s', '5s', '7s']  

# Global Variables  
selected_index = 0  
sub_index = 0  # For submenu selection  
in_submenu = False  # Track if in a submenu  
default_speed = 650  # Default speed  
selected_time = 5  # Default time  

def draw_menu(selected_index):  
    """Draw the menu with the selected item highlighted."""  
    oled.fill(0)    
    for i, item in enumerate(menu_items):  
        oled.text('> ' + item if i == selected_index else '  ' + item, 0, i * 10)  
    oled.show()  

def draw_submenu(items, selected_index):  
    """Draw the submenu with the selected item highlighted."""  
    oled.fill(0)    
    for i, item in enumerate(items):  
        oled.text('> ' + item if i == selected_index else '  ' + item, 0, i * 10)  
    oled.show()  

def perform_action(selected_option):  
    """Perform an action based on the selected menu option."""  
    global in_submenu, sub_index  
    in_submenu = True  
    sub_index = 0  
    if selected_option == 0:  # Speed  
        draw_submenu(speed_items, sub_index)  
    elif selected_option == 1:  # Time  
        draw_submenu(time_items, sub_index)  
    else:  # Exit  
        oled.fill(0)  
        oled.text("Exiting...", 0, 20)  
        oled.show()  
        time.sleep(2)  
        machine.reset()  # Reset the microcontroller  

# Pin configurations for buttons  
up_button = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)    
down_button = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)   
select_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)  

draw_menu(selected_index)  

while True:  
    time.sleep(0.1)  # Main loop delay  

    if in_submenu:  
        # Handle submenu navigation  
        if not up_button.value():  # If up button is pressed  
            sub_index = (sub_index - 1) % (len(speed_items) if menu_items[selected_index] == "Speed" else len(time_items))  
            draw_submenu(speed_items if menu_items[selected_index] == "Speed" else time_items, sub_index)  
            time.sleep(0.3)  # Simple debouncing  

        if not down_button.value():  # If down button is pressed  
            sub_index = (sub_index + 1) % (len(speed_items) if menu_items[selected_index] == "Speed" else len(time_items))  
            draw_submenu(speed_items if menu_items[selected_index] == "Speed" else time_items, sub_index)  
            time.sleep(0.3)  

        if not select_button.value():  # If select button is pressed  
            # Perform action based on selected submenu  
            selected_value = speed_items[sub_index] if menu_items[selected_index] == "Speed" else time_items[sub_index]  
            oled.fill(0)  
            if menu_items[selected_index] == "Speed":  
                # Map speed string to actual values  
                default_speed = {'Fast': 4000, 'Medium': 650, 'Slow': 300}.get(selected_value, default_speed)  
            else:  
                # Map time string to actual values  
                selected_time = {'3s': 3, '5s': 5, '7s': 7}.get(selected_value, selected_time)    
            oled.text("Set: " + selected_value, 0, 20)  
            oled.show()  
            time.sleep(2)  # Show confirmation  
            in_submenu = False  # Return to main menu  
            selected_index = 0  # Reset selected index  
            draw_menu(selected_index)  

    else:  
        # Handle main menu navigation  
        if not up_button.value():  # If up button is pressed  
            selected_index = (selected_index - 1) % len(menu_items)   
            draw_menu(selected_index)  
            time.sleep(0.3)  

        if not down_button.value():  # If down button is pressed  
            selected_index = (selected_index + 1) % len(menu_items)    
            draw_menu(selected_index)  
            time.sleep(0.3)  

        if not select_button.value():  # If select button is pressed  
            perform_action(selected_index)  
            time.sleep(0.5)  # Slight delay to avoid multiple triggers