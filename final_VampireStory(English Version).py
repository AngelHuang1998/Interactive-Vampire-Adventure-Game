import time  # Used for time-related functions such as delays
import sys   # Used for system operations, such as exiting the program or handling command-line arguments
import turtle # Used for drawing graphics and patterns
import os # Used for file and directory operations
import random # Used for generating random numbers
import pygame  # Used for playing music and sound effects
import threading  # Used for multi-threading to play sound effects and run the main program simultaneously
random.seed(time.time())  # Sets the random number generator seed based on the current time for randomness

t = 1.5  # Controls the time interval

def load_file_content(file_name):
    """
    Checks if a file exists and reads its content.
    If the file does not exist, an error is displayed and the program exits.
    """
    if not os.path.exists(file_name):
        print(f"Error: {file_name} is missing. Please add it to the program directory.")
        sys.exit()
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()

def get_input(prompt):
    """
    Exits the program if the user inputs "quit".
    """
    user_input = input(prompt)
    if user_input.lower() == "quit":
        print("Exiting the story. Goodbye!")
        sys.exit()
    return user_input


def play_sound_effect(sound_name):
    """
    Play the specified sound effect file.
    If the sound effect file exists, use the pygame module to play it.
    If the file is missing or an error occurs, output an appropriate message.
    """
    sound_files = {
        "poor": "poor.mp3",
        "rich": "rich.mp3"
    }

    # Check if sound_name is in sound_files and if the corresponding sound file exists
    if sound_name in sound_files and os.path.exists(sound_files[sound_name]):

        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_files[sound_name])  # Load the sound effect file
        
        # If any line inside the try block raises an error, Python will immediately enter the except block without crashing the program.
        except pygame.error as e:  # Handle pygame-related errors
            print(f"Pygame error while loading {sound_files[sound_name]}: {e}")
        except FileNotFoundError:  # Handle file not found errors
            print(f"Error: {sound_files[sound_name]} not found.")
        except Exception as e:  # Handle other unexpected errors
            print(f"Unexpected error: {e}")

        # This part will only execute if no errors occur in the try block
        else:  
            pygame.mixer.music.set_volume(1.0)   # Set the volume
            pygame.mixer.music.play()   # Play the sound effect

            start_time = time.time()     
            while pygame.mixer.music.get_busy():   # Limit playback duration to a maximum of 10 seconds
                if time.time() - start_time > 10:
                    break
                time.sleep(0.1)   # Check if the music is still playing every 0.1 seconds to reduce CPU usage

    else:   # If sound_name is not in sound_files or the corresponding sound file does not exist
        print(f"Error: {sound_files.get(sound_name, 'Unknown')} not found.")



def draw_diamond(layers):
    """
    Draws the outline of a diamond: an inverted triangle-shaped diamond.
    """
    turtle.speed(0)  # Sets the drawing speed
    top_y = 220  # The y-coordinate of the top of the diamond
    turtle.penup()
    turtle.goto(-10 * (layers - 1), top_y)  # Moves to the starting point at the top
    turtle.pendown()

    for layer in range(layers, 0, -1):  # Draws from the top layer to the bottom layer
        start_x = -10 * (layer - 1)  # The x-coordinate of the current layer's start
        start_y = top_y - (layers - layer) * 20  # The y-coordinate of the current layer's start
        turtle.penup()
        turtle.goto(start_x, start_y)
        turtle.pendown()

        for _ in range(layer):  # Draws the inverted triangles of the current layer
            draw_inverted_triangle(20)  # Side length of the inverted triangle is 20
            turtle.penup()
            turtle.forward(20)  # Moves to the position for the next inverted triangle
            turtle.pendown()

    return start_y - 20  # Returns the y-coordinate of the bottom of the diamond

def draw_inverted_triangle(size):
    """
    Draws the inside of the diamond: the diamond consists of multiple inverted triangles.
    Parameter size: The side length of the triangle.
    """
    turtle.fillcolor("blue")  # Diamond color
    turtle.begin_fill()
    for _ in range(3):
        turtle.forward(size)
        turtle.right(120)  # Turns ensure it's an inverted triangle
    turtle.end_fill()

def draw_diamond_with_ring(layers):
    """
    Draws the base ring of a diamond ring.
    Parameter layers: The number of layers in the diamond.
    """
    # Set the starting y-coordinate at the bottom of the diamond
    diamond_bottom_y = draw_diamond(layers)

    # Draw the outer ring
    ring_center_y = diamond_bottom_y - 95
    turtle.penup()
    turtle.goto(10, ring_center_y)
    turtle.pendown()
    turtle.fillcolor("gold")
    turtle.begin_fill()
    turtle.circle(50)  
    turtle.end_fill()

    # Draw the hollow inner part of the ring
    turtle.penup()
    turtle.goto(10, ring_center_y + 10)
    turtle.pendown()
    turtle.fillcolor("white")
    turtle.begin_fill()
    turtle.circle(40)  # Inner circle
    turtle.end_fill()

def display_message(message, x, y, font_size=18):
    """
    Displays a message on the canvas using turtle.
    Parameters:
    - message: The text content to display.
    - x, y: The position to display the text.
    - font_size: The font size.
    """
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.hideturtle()
    turtle.write(message, align="center", font=("Arial", font_size, "bold"))

def play_sound_and_display_message(sound_name, message, x, y, font_size=18):
    """
    Plays a sound effect and displays a message simultaneously.
    Uses multi-threading to handle sound playback without blocking the main program.
    """
    sound_thread = threading.Thread(target=play_sound_effect, args=(sound_name,))
    sound_thread.start()  # Start the sound playback thread

    display_message(message, x, y, font_size)  # Display the message using the main thread
    sound_thread.join()  # Wait for the sound playback to finish

def main():
    """
    Main game flow, including the storyline and interactive logic.
    Users interact with the computer through options that influence the story's progress.
    """
    print("Prompt: You can type \"quit\" to exit the program.")

    # Prompt the user to press Enter to continue
    get_input("(press enter to start)\n")

    # Load the introduction of the story
    intro = load_file_content("Intro_1.txt")
    print(intro)

    get_input("(press enter to start)\n")
    # Ask the user if they want to know about Adam's special identity
    ans1 = get_input("\"Adam actually has a special identity. Do you want to know?\"(yes/no)\n")

    if ans1 in "no":
        # If the user chooses not to know, load and display the corresponding text, then wait for some time
        identity_no = load_file_content("identity_No_2.txt")
        print(identity_no)
        time.sleep(t)

    # Display Adam's secret identity as a vampire
    print("""\"What people don't know is that Adam is actually a vampire, 
hiding among humans with great wealth.\"\n""")
    time.sleep(t)

    # Prompt the user to press Enter to continue
    get_input("(press enter to continue)\n")

    # Display further development of the story, describing the scene where Jenny has an accident
    print("\"One night, after staying late at the school library, Jenny accidentally falls down the stairs\"\n")
    time.sleep(t)

    # Ask Adam if he wants to save Jenny
    ans2 = get_input("\"Adam, do you want to save her? (yes/no)\n")
    time.sleep(t)

    while True:
        if ans2 in "yes":
            # If the user chooses to save, display the corresponding storyline and pause
            save_yes = load_file_content("Save or not_Yes_3.txt")
            print(save_yes)
            get_input("(press enter to continue)\n")
        else:
            # If the user chooses not to save, display a different storyline
            save_no = load_file_content("Save or not_No_4.txt")
            print(save_no)
            time.sleep(2.5)
            print(" ")

            # Ask if Adam wants to change Jenny's perception and pursue her
            ans4 = get_input("\"Adam, do you want to change her perception of you and pursue her? (yes/no)\n")

            if ans4 in "yes":
                # If the user chooses to pursue, go back to the previous question
                ans2 = "yes"
                print("(Yes, I want to save her)\n")
                continue
            else:
                # If the user chooses to give up, the story ends
                print("The two will have no further interaction and become strangers.")
                print("(The story ends.)")
                break

        # Display the conditions set by Jenny's father
        print(" ")
        print("""However, Jenny's father is a very traditional man who could never accept the existence of a \"non-human\" being. 
The financial pressures on her family also make it hard for Jenny to pursue her own happiness.\n""")
        time.sleep(3)

        # Ask if Adam is willing to accept the conditions
        ans3 = get_input("Father: \"Adam, if you want to pursue my daughter, are you willing to agree to one of three conditions?\" (yes/no)\n")
        choices = {
            "1": "(I will give up my chance at immortality and become an ordinary human.)",
            "2": "(I will sever all ties with my family)",
            "3": "(I will become a vegetarian from now on.)"
        }

        if ans3 in "yes":
            # Display the storyline for agreeing to the conditions
            agree_yes = load_file_content("Agree Condition or not_Yes_5.txt")
            print(agree_yes)

            while True:
                # Ask the user to choose a specific condition or let the father choose for them
                ans5 = get_input("Please answer 1, 2, 3, or 4 (Father, please choose for me):\n")
                if ans5 in choices:
                    print(choices[ans5])
                    break
                elif ans5 == "4":
                    # Randomly select a condition
                    random_choice = random.choice(list(choices.keys()))
                    print(choices[random_choice])
                    break
                else:
                    print("Invalid choice. Please try again.")

            time.sleep(t)
        else:
            # Display the storyline for not agreeing to the conditions
            agree_no = load_file_content("Agree Condition or not_No_6.txt")
            print(agree_no)
            break

        # Final diamond ring preparation phase
        print("\nFather: Very well, you've earned the chance to propose to my daughter.\n")

        while True:
            # Ask Adam how large a diamond ring (how many layers) he wants to prepare
            layer = get_input("Adam, how many layers of diamond do you want to prepare for proposing?(At least 4 layers)\n")
            if layer.isdigit() and int(layer) >= 4:
                layer = int(layer)
                print("Diamond loading...\n")
                draw_diamond_with_ring(layer)  # Draw the diamond ring
                if layer >= 7:
                    # If the number of layers is sufficient, play the "rich" sound effect and display the corresponding message
                    play_sound_and_display_message(
                        "rich",
                        "Wow, this diamond is so big! Rich Boy!!\n Wish you two lived happily ever after.",
                        0,
                        -250,
                        18
                    )
                else:
                    # If the number of layers is smaller, play the "poor" sound effect and display the corresponding message
                    play_sound_and_display_message(
                        "poor",
                        "It's too small. Are you poor?\n You may get divorced soon...",
                        0,
                        -250,
                        18
                    )
                turtle.done()
                sys.exit()  # Exit the program
            else:
                print("\nThat's too small!! Please input again!")

# Execute the main program
if __name__ == "__main__":
    main()
