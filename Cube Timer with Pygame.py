"""Name: Philips Xu
   Date: June 2, 2018
   Description: Rubik's Cube Timer. Generates scramble and saves times in a file.
   Times can be deleted.
"""

import pygame, cubeTimerSprites, random, math
pygame.init()
pygame.mixer.init()


def generate_random_scramble(moves, scramble_text):
    '''Generates a random scramble.'''

    scramble = []
    prev_index = -1
    while len(scramble) < 21:
        index = random.randrange(len(moves))
        # Ensures that same type of move won't be adjacent
        if (index/3) != (prev_index/3):
            scramble.append(moves[index])
            prev_index = index

    # Set scramble text
    scramble_text.set_scramble(scramble)

def add_time(times, timer):
    '''Adds time to file and display.'''
    times_file = open("times.txt", "a")
    times.add_text(str(timer.get_time()))
    times_file.write(str(timer.get_time()) + "\n")
    times_file.close()

def clear_everything(time_list, times, best_time, avg_time):
    '''Clears times.'''

    # Clear times file
    open("times.txt", "w").truncate()

    # Clear times list
    del time_list[:]

    # Clear displays to 0, except for best time
    times.set_text("")
    avg_time.set_text("Avg time: 0")

def start_inspection(inspection):
    '''Begin inspection stage (15 seconds).'''

    inspection.show()
    inspection.start_countdown()

def retrieve_current_best(best_time):
    pass
    # Use string splicing to get current best time
    #print(best_time.get_message()[11:])
    #current_best = float(best_time.get_message()[11:])

def update_stat_times(timer, time_list, best_time_text, avg_time_text):
    '''Update time stats.'''

    # Add time to list
    if timer.get_time():
        time_list.append(timer.get_time())

    if time_list:

        # Update best time
        best_time = min(time_list)
        #if best_time < retrieve_current_best(best_time_text):
        retrieve_current_best(best_time_text)
        best_time_text.set_text("Best time: " + str(best_time))

        # Update avg time
        avg = float(sum(time_list))/len(time_list)
        avg_time_text.set_text("Avg. time: %.3f" % avg)

def main():
    '''This function defines the mainline logic for the Cube Timer.'''

    # Display
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Cube Timer")

    background = pygame.image.load("cube_background.png")
    screen.blit(background, (0,0))


    # Entities

    # Open times file
    times_file = open("times.txt", "r")

    # List of possible moves
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", \
                     "D'", "D2", "B", "B'", "B2", "F", "F'", "F2"]



    # Colour
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0,191,255)
    GREEN = (0, 255, 0)
    ROYAL_BLUE = (65,105,225)
    ORANGE = (255,69,0)
    FUCHSIA = (255, 0, 128)
    LIGHT_BLUE = (0, 255, 255)
    YELLOW = (255,255,0)


    # Displayed Text
    title = cubeTimerSprites.TextLabel(70, screen.get_width()/2, \
                                       40, LIGHT_BLUE, screen)
    times = cubeTimerSprites.TextLabel(20, screen.get_width()/2, \
                                       525, WHITE, screen)
    best_time_text = cubeTimerSprites.TextLabel(20, 150, screen.get_height()/2, \
                                           GREEN, screen)
    avg_time_text = cubeTimerSprites.TextLabel(20, 150, screen.get_height()/2 + 50, \
                                               GREEN, screen)
    instructions = cubeTimerSprites.TextLabel(20, screen.get_width()/2, \
                                              140, ORANGE, screen)
    instructions_2 = cubeTimerSprites.TextLabel(20, screen.get_width()/2, \
                                                  600, ORANGE, screen)
    timer = cubeTimerSprites.Timer(50, screen.get_width()/2, \
                                       screen.get_height()/2, WHITE, screen)
    scramble_text = cubeTimerSprites.TextLabel(30, screen.get_width()/2, \
                                               200, WHITE, screen)
    inspection = cubeTimerSprites.Timer(50, screen.get_width()/2, \
                                        -100, BLUE, screen)
    DNF = cubeTimerSprites.TextLabel(50, screen.get_width()/2, \
                                     -100, RED, screen)
    session_display = cubeTimerSprites.TextLabel(25, screen.get_width()/2, \
                                                 475, YELLOW, screen)
    allSprites = pygame.sprite.Group(timer, scramble_text, title, instructions, \
                                     times, best_time_text, avg_time_text, \
                                     session_display, inspection, DNF, \
                                     instructions_2)

    # Generate random scramble
    scramble = generate_random_scramble(moves, scramble_text)

    # Set title and instructions
    title.set_text("CUBE TIMER")
    instructions.set_text("Press R to rescramble, Spacebar to start/stop timer")
    instructions_2.set_text("Press C to clear times, B to reset best time")

    # Set times
    time_list = []
    try:
        for line in times_file:
            time_list.append(float(line.strip()))

    except ValueError:
        pass

    # Display Session title
    session_display.set_text("Current Session")

    # Display DNF
    DNF.set_text("DNF")

    # Update best time and avg time
    update_stat_times(timer, time_list, best_time_text, avg_time_text)

    # Don't display existing times
    times.set_text("")
    times_file.close()

    # Assign values
    clock = pygame.time.Clock()
    keepGoing = True
    initial_time = 0
    counting_down = False

    # Loop
    while keepGoing:

        # Time
        clock.tick(30)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:

                # Inspection stage
                if event.key == pygame.K_SPACE and not timer.get_timing() \
                   and not counting_down:
                    start_inspection(inspection)
                    DNF.hide()
                    timer.hide()
                    counting_down = True

                # Begin stopwatch
                elif event.key == pygame.K_SPACE and counting_down:
                    timer.start_timer()
                    timer.show()
                    inspection.hide()
                    inspection.stop()
                    counting_down = False

                # Stop stopwatch
                elif event.key == pygame.K_SPACE and timer.get_timing():
                    timer.stop()
                    add_time(times, timer)
                    update_stat_times(timer, time_list, best_time_text, avg_time_text)
                    generate_random_scramble(moves, scramble_text)

                # Get new scramble
                elif event.key == pygame.K_r:
                    generate_random_scramble(moves, scramble_text)

                # Clear stuff
                elif event.key == pygame.K_c:
                    clear_everything(time_list, times, best_time_text, avg_time_text)

                # Clear best time
                elif event.key == pygame.K_b:
                    best_time_text.set_text("Best time: 0")

        # Display DNF (Did Not Finish) if 15 seconds is up for inspection
        if not (15 - inspection.get_time()):
            inspection.hide()
            DNF.show()
            counting_down = False

        # Refresh Screen
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

main()
