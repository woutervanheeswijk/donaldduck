# -*- coding: utf-8 -*-
"""
A Monte Carlo Simulation for the Donald Duck Holiday Game
Author: W.J.A. van Heeswijk
Date: 4-2-2020
This code was used to analyze Donald Duck's Vakantiespel,
which was published in Donald Duck Weekblad in 1996.
Game copyright belongs to De Geïllustreerde Pers (1996).
This code is supplemental to the following publication:
'Donald Duck Holiday Game: A numerical analysis of a
Game of the Goose role-playing variant'
Board Game Studies Journal (2020)
This code has been published under the GNU GPLv3 license
"""
import random
import sys

NUMBER_OF_SIMULATION_RUNS = 10 # at least 1 simulation run
NUMBER_OF_PLAYERS = 5 # between 2 and 5 players

# Game metrics
class GamePerformanceMetrics():
    """Define performance metrics"""
    def __init__(self, number_of_route_maps, number_of_cameras, \
                 number_of_postcards, number_of_coffees, \
                 number_of_dishes_washed, number_of_tunnels, \
                 number_of_camping_cards, number_event_squares_visited_hdl, \
                 number_event_squares_visited_goofy, \
                 number_event_squares_visited_donald, \
                 number_event_squares_visited_horace, \
                 number_event_squares_visited_clarabelle, \
                 number_event_cards_drawn_hdl, \
                 number_event_cards_drawn_goofy, \
                 number_event_cards_drawn_donald, \
                 number_event_cards_drawn_horace, \
                 number_event_cards_drawn_clarabelle, \
                 number_squares_random_hdl, \
                 number_squares_random_goofy, number_squares_random_donald, \
                 number_squares_random_horace, \
                 number_squares_random_clarabelle):
        self.number_of_route_maps = number_of_route_maps
        self.number_of_cameras = number_of_cameras
        self.number_of_postcards = number_of_postcards
        self.number_of_coffees = number_of_coffees
        self.number_of_dishes_washed = number_of_dishes_washed
        self.number_of_tunnels = number_of_tunnels
        self.number_of_camping_cards = number_of_camping_cards
        self.number_event_squares_visited_hdl = number_event_squares_visited_hdl
        self.number_event_squares_visited_goofy = number_event_squares_visited_goofy
        self.number_event_squares_visited_donald = number_event_squares_visited_donald
        self.number_event_squares_visited_horace = number_event_squares_visited_horace
        self.number_event_squares_visited_clarabelle = number_event_squares_visited_clarabelle
        self.number_event_cards_drawn_hdl = number_event_cards_drawn_hdl
        self.number_event_cards_drawn_goofy = number_event_cards_drawn_goofy
        self.number_event_cards_drawn_donald = number_event_cards_drawn_donald
        self.number_event_cards_drawn_horace = number_event_cards_drawn_horace
        self.number_event_cards_drawn_clarabelle = number_event_cards_drawn_clarabelle
        self.number_squares_random_hdl = number_squares_random_hdl
        self.number_squares_random_goofy = number_squares_random_goofy
        self.number_squares_random_donald = number_squares_random_donald
        self.number_squares_random_horace = number_squares_random_horace
        self.number_squares_random_clarabelle = number_squares_random_clarabelle

def dicethrow():
    """Throw die"""
    simulated_dice_value = random.randrange(1, 7)
    return int(simulated_dice_value)

def draweventcard(active_card_deck, active_player, active_characters, \
                  event_card_id, gpm, event_card_squares, event_squares):
    """Draw event card from deck"""
    if event_card_id < 10:
        event_card_id += 1
    elif event_card_id == 10:
        event_card_id = 0

    event_card_number = 0
    event_card_number = active_card_deck[event_card_id]

    # 1. Forgot route map, return to start
    if event_card_number == 1 and active_player.number_maps_collected == 0:
        gpm.number_of_route_maps += 1
        active_player.number_of_random_squares -= active_player.position_on_board
        active_player.position_on_board = 0
        active_player.number_of_event_cards_drawn += 1
        active_player.number_maps_collected += 1

    # 2. Forgot camera at saloon
    if event_card_number == 2 and active_player.position_on_board >= 26:
        gpm.number_of_cameras += 1
        active_player.number_of_random_squares += (37 - active_player.position_on_board)
        active_player.position_on_board = 37
        active_player.number_of_event_cards_drawn += 1

        # Necessary to draw new card (new square is 37)
        if active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id, \
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # 3. Post card in mailboxe (move might also be forward, no restriction)
    if event_card_number == 3:
        gpm.number_of_postcards += 1
        active_player.number_of_event_cards_drawn += 1
        active_player.number_of_random_squares += (32 - active_player.position_on_board)
        active_player.position_on_board = 32

    # 4. Walker has blister
    if event_card_number == 4 and active_player.transport_mode == "Walk":
        active_player.number_of_turns_waiting = 2
        active_player.number_of_event_cards_drawn += 1

    # 5. Walker gets ride (until next event card square)
    next_position = -1000 # initialize
    if event_card_number == 5 and active_player.transport_mode == "Walk":
        for next_position in event_card_squares:
            if next_position > active_player.position_on_board:
               # exit loop when next square with circle is determined
                break

        active_player.number_of_random_squares += \
        (next_position - active_player.position_on_board)
        active_player.position_on_board = next_position
        active_player.number_of_event_cards_drawn += 1

        # Necessary to draw new card
        if active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id,\
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # 6. Tailwind (cast die again to move forward)
    if event_card_number == 6 and active_player.transport_mode in ("Walk", "Bike", "Motor"):
        dice_value = dicethrow()
        active_player.number_of_random_squares += dice_value
        active_player.position_on_board += dice_value
        active_player.number_of_event_cards_drawn += 1

        # Draw new card
        if active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id, \
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # 7. Head wind (cast die again to move backwards)
    if event_card_number == 7 and \
    active_player.transport_mode in ("Walk", "Bike", "Motor"):
        dice_value = dicethrow()
        active_player.number_of_random_squares -= dice_value
        active_player.position_on_board = \
        max(0, active_player.position_on_board - dice_value)
        active_player.number_of_event_cards_drawn += 1

        # Draw new card
        if active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id, \
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # 8. Flat tire  (skip 1 turn)
    if event_card_number == 8 and \
    active_player.transport_mode in ("Motor", "Bike", "Car", "Bus"):
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_cards_drawn += 1

    # 9. Rain: every player moves back three squares (except for car and bus)
    if event_card_number == 9:
        active_player.number_of_event_cards_drawn += 1

        copy_active_player = active_player
        for active_player in active_characters:
            if active_player.transport_mode in ("Walk", "Bike", "Motor"):
                active_player.position_on_board = \
                max(active_player.position_on_board - 3, 0)

                active_player.number_of_random_squares -= 3
                if active_player.position_on_board in \
                event_squares:
                    # Update based on new event square
                    active_card_deck, active_player, active_characters, \
                    event_card_id, gpm, event_card_squares, event_squares = \
                    eventsquare(active_card_deck, active_player, \
                    active_characters, event_card_id, gpm, event_card_squares, \
                    event_squares)

                    # Correction in counter
                    if active_player.position_on_board == 92:
                        gpm.number_of_dishes_washed -= 1

                    if active_player.position_on_board == 98:
                        gpm.number_of_tunnels -= 1

                if active_player.position_on_board not in \
                event_squares:
                    active_player.number_of_turns_waiting = 0
                    #End waiting when moved from event square

        # Restore active player
        active_player = copy_active_player

        # Draw card (assumption: only for active player only)
        if active_player.transport_mode in ("Walk", "Bike", "Motor") and \
        active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id, \
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # 10. Engine failure, wait for roadside assistance
    if event_card_number == 10 and \
    active_player.transport_mode in ("Car", "Bus", "Motor"):
        turns_waiting = 2
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_cards_drawn += 1

    # 11. Road maintenance
    if event_card_number == 11:
        turns_waiting = 3
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_cards_drawn += 1

    return active_card_deck, active_player, active_characters, event_card_id, \
           gpm, event_card_squares, event_squares


def eventsquare(active_card_deck, active_player, active_characters, \
                event_card_id, gpm, event_card_squares, event_squares):
    """Visit event square"""
    # (9) Have a coffee
    if active_player.position_on_board == 9 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        gpm.number_of_coffees += 1
        active_player.number_of_event_squares_visited += 1

    # (13) Trash on the road
    if active_player.position_on_board == 13 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (17,18,19) Takeover forbidden
    if active_player.position_on_board in (17, 18, 19) and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (24) Picnic
    if active_player.position_on_board == 24 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (29) Money exchange
    if active_player.position_on_board == 29 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 2
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (39,40,41) Dangerous turn
    if active_player.position_on_board in (39, 40, 41) and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 2
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (50) Take a break
    if active_player.position_on_board == 50 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 2
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (56) Fill up gas tank
    if active_player.position_on_board == 56 and \
       active_player.number_of_turns_waiting == 0 and \
       active_player.transport_mode in ("Motor", "Car", "Bus"):
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (63,64,65) Slow down
    if active_player.position_on_board in (63, 64, 65) and \
       active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (71) Chased away from money bin
    if active_player.position_on_board == 71:
        active_player.position_on_board = active_player.position_on_board + 3
        active_player.number_of_event_squares_visited += 1

        # Necessary to draw new card (square 74 is a random event square)
        if active_player.position_on_board in event_card_squares:
            active_card_deck, active_player, active_characters, event_card_id, \
            gpm, event_card_squares, event_squares = \
            draweventcard(active_card_deck, active_player, active_characters, \
                          event_card_id, gpm, event_card_squares, event_squares)

    # (81) Nice spot
    if active_player.position_on_board == 81 and \
       active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (83) Sick, nauseous, go to first aid
    if active_player.position_on_board == 83 and \
       active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (90) Eat a bite
    if active_player.position_on_board == 90 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (91) Have a drink
    if active_player.position_on_board == 91 and \
    active_player.number_of_turns_waiting == 0:
        turns_waiting = 1
        active_player.number_of_turns_waiting = 1 + turns_waiting
        active_player.number_of_event_squares_visited += 1

    # (92) Wash dishes (continue only when throwing 6)
    if active_player.position_on_board == 92:
        gpm.number_of_dishes_washed += 1
        active_player.number_of_turns_waiting = sys.maxsize
        active_player.number_of_event_squares_visited += 1

    # (98) Lost in dark tunnel (continue only when throwing 2)
    if active_player.position_on_board == 98:
        gpm.number_of_tunnels += 1
        active_player.number_of_turns_waiting = sys.maxsize
        active_player.number_of_event_squares_visited += 1

    # (105) Speed control
    if active_player.position_on_board == 105 and \
    active_player.number_of_turns_waiting == 0 \
    and active_player.transport_mode in ("Bus", "Car", "Motor"):
        turns_waiting = 1
        active_player.number_of_turns_waiting = 2
        active_player.number_of_event_squares_visited += 1

    # (112) Forgot camping card, back to start
    if active_player.position_on_board == 112 and \
    active_player.number_camping_cards_collected == 0:
        gpm.number_of_camping_cards += 1
        active_player.number_camping_cards_collected += 1
        active_player.position_on_board = 0
        active_player.number_of_event_squares_visited += 1

    return active_card_deck, active_player, active_characters, event_card_id, \
    gpm, event_card_squares, event_squares

class Character:
    """Define character attributes"""
    def __init__(self, character_name, transport_mode, position_on_board, \
                 allowed_to_start, number_of_turns_waiting, shortcut_position, \
                 number_of_turns_leading, player_has_led, \
                 number_of_shortcuts_taken, number_of_event_squares_visited, \
                 number_of_event_cards_drawn, \
                 number_of_random_squares, number_camping_cards_collected, \
                 number_maps_collected):
        self.character_name = character_name
        self.transport_mode = transport_mode
        self.position_on_board = position_on_board
        self.allowed_to_start = allowed_to_start
        self.number_of_turns_waiting = number_of_turns_waiting
        self.shortcut_position = shortcut_position
        self.number_of_turns_leading = number_of_turns_leading
        self.player_has_led = player_has_led
        self.number_of_shortcuts_taken = number_of_shortcuts_taken
        self.number_of_event_squares_visited = number_of_event_squares_visited
        self.number_of_event_cards_drawn = number_of_event_cards_drawn
        self.number_of_random_squares = number_of_random_squares
        self.number_camping_cards_collected = number_camping_cards_collected
        self.number_maps_collected = number_maps_collected

# START OF MAIN GAME CODE
# Define number of active players
if NUMBER_OF_PLAYERS < 1 or NUMBER_OF_PLAYERS > 5:
    print("Please select a number of players between 2 and 5")
    sys.exit()

# Set number of simulation runs
if NUMBER_OF_SIMULATION_RUNS < 1:
    print("Please select a positve number of simulation runs")
    sys.exit()

# Initialize outer loop game metrics
WINNERGOOFY = 0
WINNERDONALD = 0
WINNERHORACE = 0
WINNERCLARABELLE = 0
WINNERHDL = 0

# Initialize text file with game results
GAMERESULTS = open("GAMERESULTS.txt", "w")
GAMERESULTS.write("SimulationRunID")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfRoundsPlayed")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerName")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("WinnerClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsWaitingHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsWaitingGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsWaitingDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsWaitingHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsWaitingClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfCampingCards")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfRouteMaps")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfCameras")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfPostcards")
GAMERESULTS.write(";")
GAMERESULTS.write("TurnsLedWinner")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfLeaders")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfShortcutsHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfShortcutsGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfShortcutsDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfShortcutsHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfShortcutsClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("StartingPositionHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("StartingPositionGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("StartingPositionDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("StartingPositionHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("StartingPositionClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventSquaresVisitedHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventSquaresVisitedGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventSquaresVisitedDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventSquaresVisitedHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventSquaresVisitedClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventCardsDrawnHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventCardsDrawnGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventCardsDrawnDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventCardsDrawnHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberOfEventCardsDrawnClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberSquaresRandomHDL")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberSquaresRandomGoofy")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberSquaresRandomDonald")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberSquaresRandomHorace")
GAMERESULTS.write(";")
GAMERESULTS.write("NumberSquaresRandomClarabelle")
GAMERESULTS.write(";")
GAMERESULTS.write(";\n")
GAMERESULTS.close()

for simulation_run in range(0, NUMBER_OF_SIMULATION_RUNS):
    # Define characters
    Donald = Character("Donald", "Car", 0, bool(False), \
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    Goofy = Character("Goofy", "Bus", 0, bool(False), \
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    Clarabelle = Character("Clarabelle", "Bike", 0, bool(False), \
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    Horace = Character("Horace", "Motor", 0, bool(False), \
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    HueyDeweyLouie = Character("Huey, Dewey & Louie", "Walk", 0, bool(False), \
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    all_characters = [Donald, Goofy, Clarabelle, Horace, HueyDeweyLouie]
    active_characters = []

    # Define sets of random event squares and event card squares
    event_card_squares = (5, 11, 15, 22, 33, 37, 47, 60, 74, 75, \
                          79, 86, 87, 88, 95, 102, 107)
    event_squares = (9, 13, 17, 18, 19, 24, 29, 39, 40, 41, 50, 56,\
                     63, 64, 65, 71, 81, 83, 90, 91, 92, 98, 105, 112)

    #Create random set of active players (random starting order)
    players_added = len(active_characters)
    while players_added < NUMBER_OF_PLAYERS:
        random_character_id = random.randrange(0, len(all_characters))
        random_character = all_characters[random_character_id]
        active_characters.append(random_character)
        all_characters.remove(random_character)
        players_added += 1

    #Initialize sequence of random event cards
    standard_card_deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    active_card_deck = []

    while standard_card_deck:
        card_id = random.randrange(0, len(standard_card_deck))
        card_number = standard_card_deck[card_id]
        active_card_deck.append(card_number)
        standard_card_deck.remove(card_number)

    event_card_id = 0

    gpm = GamePerformanceMetrics(0, 0, 0, \
                 0, 0, 0, 0, \
                 0, 0, 0, \
                 0, 0, 0, \
                 0, 0, 0, \
                 0, 0, 0, 0, 0, 0)

    #Initialize game metrics
    round_id = 0
    turns_waiting_goofy = 0
    turns_waiting_donald = 0
    turns_waiting_horace = 0
    turns_waiting_clarabelle = 0
    turns_waiting_hdl = 0
    number_of_shortcuts_hdl = 0
    number_of_shortcuts_goofy = 0
    number_of_shortcuts_donald = 0
    number_of_shortcuts_horace = 0
    number_of_shortcuts_clarabelle = 0
    starting_position_hdl = 0
    starting_position_goofy = 0
    starting_position_donald = 0
    starting_position_horace = 0
    starting_position_clarabelle = 0
    gpm.number_of_dishes_washed = 0
    gpm.number_of_tunnels = 0
    gpm.number_of_camping_cards = 0
    gpm.number_of_route_maps = 0
    gpm.number_of_cameras = 0
    gpm.number_of_postcards = 0
    gpm.number_of_coffees = 0
    gpm.number_of_event_cards_hdl = 0
    gpm.number_of_event_cards_goofy = 0
    gpm.number_of_event_cards_donald = 0
    gpm.number_of_event_cards_horace = 0
    gpm.number_of_event_cards_clarabelle = 0

    player_positions = open("player_positions.txt", "w")
    for active_player in active_characters:
        player_positions.write(active_player.character_name)
        player_positions.write(";")

    player_positions.close()

    #Game runs until first player reaches the camping (square 115)
    game_finished = bool(False)

    while game_finished == bool(False):
        overall_starting_position = 0
        round_id += 1
        print("---Round", round_id, "has started---")

        with open('player_positions.txt', 'a') as player_positions:
            player_positions.write("\n")
            player_positions.close()

        for active_player in active_characters:
            if active_player.character_name == "Huey, Dewey & Louie" and \
            active_player.allowed_to_start:
                overall_starting_position += 1
                starting_position_hdl = overall_starting_position
            if active_player.character_name == "Goofy" and \
            active_player.allowed_to_start:
                overall_starting_position += 1
                starting_position_goofy = overall_starting_position
            if active_player.character_name == "Donald" and \
            active_player.allowed_to_start:
                overall_starting_position += 1
                starting_position_donald = overall_starting_position
            if active_player.character_name == "Horace" and \
            active_player.allowed_to_start:
                overall_starting_position += 1
                starting_position_horace = overall_starting_position
            if active_player.character_name == "Clarabelle" and \
            active_player.allowed_to_start:
                overall_starting_position += 1
                starting_position_clarabelle = overall_starting_position

            if not active_player.allowed_to_start:
                Startdice_value = dicethrow()

                if Startdice_value == 6:
                     # Store active player
                    copy_active_player = active_player

                    if active_player.character_name == "Huey, Dewey & Louie":
                        starting_position_hdl = 1
                    if active_player.character_name == "Goofy":
                        starting_position_goofy = 1
                    if active_player.character_name == "Donald":
                        starting_position_donald = 1
                    if active_player.character_name == "Horace":
                        starting_position_horace = 1
                    if active_player.character_name == "Clarabelle":
                        starting_position_clarabelle = 1

                    overall_starting_position = 1

                    for active_player in active_characters:
                        active_player.allowed_to_start = True

                    # Restore active player
                    active_player = copy_active_player

            dice_value = 0
            if active_player.allowed_to_start and \
            active_player.number_of_turns_waiting == 0:
                dice_value = dicethrow()

            # Check if character can take short-cut via bike lane
            if (active_player.position_on_board == 45) and   \
            (active_player.shortcut_position == 0) and \
            active_player.transport_mode in ("Walk", "Bike"):

                if active_player.character_name == "Huey, Dewey & Louie":
                    number_of_shortcuts_hdl += 1
                if active_player.character_name == "Clarabelle":
                    number_of_shortcuts_clarabelle += 1

                if active_player.position_on_board + dice_value < 48:
                    active_player.shortcut_position = \
                    ((active_player.position_on_board + dice_value) - 45)
                    active_player.position_on_board = 45
                else:
                    active_player.position_on_board = 55 + dice_value - 3
                    active_player.shortcut_position = 0

            # If character is in located the bikelane shortcut
            elif active_player.position_on_board == 45 and \
            active_player.shortcut_position > 0:
                if dice_value <= 2 - active_player.shortcut_position:
                    active_player.shortcut_position = \
                    active_player.shortcut_position + dice_value #can only be 1
                else:
                    active_player.position_on_board = 55 - \
                    (3 - active_player.shortcut_position) + dice_value
                    active_player.shortcut_position = 0

            # Check if character can take short-cut via highway
            # If player would land on Square 116 (back to start), then take a detour
            elif (active_player.position_on_board == 100) and \
            (active_player.shortcut_position == 0) and \
            active_player.position_on_board+dice_value != 112 and \
            active_player.transport_mode in ("Car", "Bus", "Motor"):
                if active_player.character_name == "Donald":
                    number_of_shortcuts_donald += 1
                if active_player.character_name == "Goofy":
                    number_of_shortcuts_goofy += 1
                if active_player.character_name == "Horace":
                    number_of_shortcuts_horace += 1

                if active_player.position_on_board+dice_value < 103:
                    active_player.shortcut_position = \
                    ((active_player.position_on_board+dice_value) - 100)
                    active_player.position_on_board = 100
                else:
                    active_player.position_on_board = 109 + dice_value - 3
                    active_player.shortcut_position = 0

            # If character is in located the highway shortcut
            elif active_player.position_on_board == 100 and \
            active_player.shortcut_position > 0:
                if dice_value <= 2-active_player.shortcut_position:
                    active_player.shortcut_position = \
                    active_player.shortcut_position + dice_value #can only be 1
                else:
                    active_player.position_on_board = 109 - \
                    (3 - active_player.shortcut_position) + dice_value
                    active_player.shortcut_position = 0

            # If not ending exactly at 115
            elif active_player.position_on_board + dice_value > 115:
                active_player.position_on_board = 115 - \
                (dice_value - (115 - active_player.position_on_board))

            # END OF GAME, STORE METRICS
            elif active_player.position_on_board + dice_value == 115:
                active_player.position_on_board += dice_value
                game_finished = bool(True)
                print("Game finished: ", active_player.character_name, "won.")
                if active_player.character_name == "Goofy":
                    WINNERGOOFY += 1
                    gpm.number_event_cards_drawn_goofy = \
                    active_player.number_of_event_cards_drawn
                    gpm.number_event_squares_visited_goofy = \
                    active_player.number_of_event_squares_visited
                if active_player.character_name == "Donald":
                    WINNERDONALD += 1
                    gpm.number_event_cards_drawn_donald = \
                    active_player.number_of_event_cards_drawn
                    gpm.number_event_squares_visited_donald = \
                    active_player.number_of_event_squares_visited
                if active_player.character_name == "Horace":
                    WINNERHORACE += 1
                    gpm.number_event_cards_drawn_horace = \
                    active_player.number_of_event_cards_drawn
                    gpm.number_event_squares_visited_horace = \
                    active_player.number_of_event_squares_visited
                if active_player.character_name == "Clarabelle":
                    WINNERCLARABELLE += 1
                    gpm.number_event_cards_drawn_clarabelle = \
                    active_player.number_of_event_cards_drawn
                    gpm.number_event_squares_visited_clarabelle = \
                    active_player.number_of_event_squares_visited
                if active_player.character_name == "Huey, Dewey & Louie":
                    WINNERHDL += 1

                # Store winner
                copy_active_player = active_player

                number_of_leaders_during_game = 0
                for active_player in active_characters:
                    number_of_leaders_during_game += active_player.player_has_led

                    if active_player.character_name == "Goofy":
                        gpm.number_event_cards_drawn_goofy = \
                        active_player.number_of_event_cards_drawn
                        gpm.number_event_squares_visited_goofy = \
                        active_player.number_of_event_squares_visited
                        gpm.number_squares_random_goofy = \
                        active_player.number_of_random_squares

                    if active_player.character_name == "Donald":
                        gpm.number_event_cards_drawn_donald = \
                        active_player.number_of_event_cards_drawn
                        gpm.number_event_squares_visited_donald = \
                        active_player.number_of_event_squares_visited
                        gpm.number_squares_random_donald = \
                        active_player.number_of_random_squares

                    if active_player.character_name == "Horace":
                        gpm.number_event_cards_drawn_horace = \
                        active_player.number_of_event_cards_drawn
                        gpm.number_event_squares_visited_horace = \
                        active_player.number_of_event_squares_visited
                        gpm.number_squares_random_horace = \
                        active_player.number_of_random_squares

                    if active_player.character_name == "Clarabelle":
                        gpm.number_event_cards_drawn_clarabelle = \
                        active_player.number_of_event_cards_drawn
                        gpm.number_event_squares_visited_clarabelle = \
                        active_player.number_of_event_squares_visited
                        gpm.number_squares_random_clarabelle = \
                        active_player.number_of_random_squares

                    if active_player.character_name == "Huey, Dewey & Louie":
                        gpm.number_event_cards_drawn_hdl = \
                        active_player.number_of_event_cards_drawn
                        gpm.number_event_squares_visited_hdl = \
                        active_player.number_of_event_squares_visited
                        gpm.number_squares_random_hdl = \
                        active_player.number_of_random_squares

                active_player = copy_active_player

                with open('player_positions.txt', 'a') as player_positions:
                    player_positions.write(str(active_player.position_on_board))
                    player_positions.close()

                with open('GAMERESULTS.txt', 'a') as GAMERESULTS:
                    GAMERESULTS.write(str(simulation_run + 1))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(round_id))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(active_player.character_name))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(WINNERHDL))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(WINNERGOOFY))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(WINNERDONALD))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(WINNERHORACE))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(WINNERCLARABELLE))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(turns_waiting_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(turns_waiting_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(turns_waiting_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(turns_waiting_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(turns_waiting_clarabelle))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_of_camping_cards))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_of_route_maps))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_of_cameras))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_of_postcards))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(active_player.number_of_turns_leading))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_leaders_during_game))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_shortcuts_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_shortcuts_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_shortcuts_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_shortcuts_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(number_of_shortcuts_clarabelle))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(starting_position_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(starting_position_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(starting_position_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(starting_position_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(starting_position_clarabelle))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_squares_visited_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_squares_visited_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_squares_visited_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_squares_visited_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_squares_visited_clarabelle))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_cards_drawn_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_cards_drawn_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_cards_drawn_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_cards_drawn_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_event_cards_drawn_clarabelle))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_squares_random_hdl))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_squares_random_goofy))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_squares_random_donald))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_squares_random_horace))
                    GAMERESULTS.write(";")
                    GAMERESULTS.write(str(gpm.number_squares_random_clarabelle))
                    GAMERESULTS.write(";\n")
                    GAMERESULTS.close()

                print("Simulation run", simulation_run+1)

                #EXIT GAME
                break

            #Regular board movement
            else:
                active_player.position_on_board = \
                active_player.position_on_board + dice_value

            # RANDOM EVENT CARDS
            if active_player.position_on_board in event_card_squares \
            and active_player.number_of_turns_waiting == 0:
                active_card_deck, active_player, active_characters, \
                event_card_id, gpm, event_card_squares, event_squares =\
                draweventcard(active_card_deck, active_player, \
                active_characters, event_card_id, \
                gpm, event_card_squares, event_squares)

            # EVENT SQUARES
            if active_player.position_on_board in \
                event_squares:
                active_card_deck, active_player, active_characters, \
                event_card_id, gpm, event_card_squares, event_squares = \
                eventsquare(active_card_deck, active_player, \
                active_characters, event_card_id, gpm, event_card_squares,\
                event_squares)

                if active_player.position_on_board == 92:
                    Dishesdice_value = dicethrow()
                    if Dishesdice_value == 6:
                        active_player.number_of_turns_waiting = 0
                        dice_value = dicethrow()
                        active_player.position_on_board = \
                        active_player.position_on_board + dice_value

                if active_player.position_on_board == 98:
                    Tunneldice_value = dicethrow()
                    if Tunneldice_value == 2:
                        active_player.number_of_turns_waiting = 0
                        active_player.position_on_board = 99

            # Reduce waiting time
            if active_player.number_of_turns_waiting > 0:
                active_player.number_of_turns_waiting = \
                active_player.number_of_turns_waiting - 1

            # Update game metrics
            if active_player.character_name == "Goofy" and \
            active_player.number_of_turns_waiting > 0:
                turns_waiting_goofy += 1
            if active_player.character_name == "Donald" and \
            active_player.number_of_turns_waiting > 0:
                turns_waiting_donald += 1
            if active_player.character_name == "Horace" and \
            active_player.number_of_turns_waiting > 0:
                turns_waiting_horace += 1
            if active_player.character_name == "Clarabelle" and \
            active_player.number_of_turns_waiting > 0:
                turns_waiting_clarabelle += 1
            if active_player.character_name == "Huey, Dewey & Louie" and \
            active_player.number_of_turns_waiting > 0:
                turns_waiting_hdl += 1

            with open('player_positions.txt', 'a') as player_positions:
                player_positions.write(str(active_player.position_on_board))
                player_positions.write(";")
                player_positions.close()

            # Check if player is currently in the lead
            copy_active_player = active_player
            active_player.number_of_turns_leading += 1
            for active_player in active_characters:
                if copy_active_player.position_on_board <= \
                active_player.position_on_board and \
                copy_active_player.character_name != \
                active_player.character_name:
                    copy_active_player.number_of_turns_leading = 0
                    break

            active_player = copy_active_player

            if active_player.number_of_turns_leading > 0:
                active_player.player_has_led = 1
