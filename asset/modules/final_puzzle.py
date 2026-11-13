from clues import get_clues



radio_fixed = False
border = "+------------------------------------------------------------+"


def new_screen():
    print("\n" * 25)


def wait_continue():
    input("\nPress Enter to continue")


def popup(lines, one_by_one=False, typing=False):
    import os
    import sys
    from time import sleep

    def enter_pressed():
        if not sys.stdin.isatty():
            return False
        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getwch() == "\r"
        else:
            import select
            if select.select([sys.stdin], [], [], 0)[0]:
                return sys.stdin.readline() != ""
        return False

    new_screen()
    show_all = False
    for line in lines:
        if one_by_one:
            new_screen()
            show_all = False
        if typing:
            for character in line:
                if not show_all and enter_pressed():
                    show_all = True
                print(character, end="", flush=True)
                if not show_all:
                    sleep(0.025)
            print()
        else:
            print(line)
        if one_by_one:
            wait_continue()
    if not one_by_one:
        wait_continue()

def row(text=""):
    print("| " + text + " " * (58 - len(text)) + " |")


def battery_display(battery):
    row("BATTERY  [" + "#" * (battery // 5) + "." * (20 - battery // 5) + "]  " + str(battery) + "%")


def panel(title, battery):
    new_screen()
    print(border)
    row(title)
    print(border)
    battery_display(battery)
    print(border)


def notebook():
    new_screen()
    print("COLLECTED NOTES\n")

    saved_clues = get_clues()
    
    if len(saved_clues) == 0:
        print("No relevant notes collected.")
    else:
        for clue_name, clue_text in saved_clues.items():
            print(clue_name + ": " + clue_text)

    wait_continue()


def message(text):
    popup([text])


def frequency_text(value):
    decimal = str(value % 100)
    if value % 100 < 10:
        decimal = "0" + decimal
    return str(value // 100) + "." + decimal


def final_puzzle(clues=None):
    # Keep this parameter so existing main.py calls do not need to change.
    # Collected notes are now read from clues.py instead.
    global radio_fixed
    radio_fixed = False
    battery = 100
    temperatures = [80, 85, 80]
    selected = 0
    effects = [(5, -5, 0), (0, 5, -5), (-5, 0, 10)]

    popup([
        "The radio has been abandoned underground for a long time.",
        "The vacuum tubes are severely worn out.",
        "Try to keep them at a stable temperature to prevent the fragile components from burning out."
    ], one_by_one=True)

    while temperatures != [85, 85, 85]:
        panel("VACUUM TUBE CONTROL SYSTEM", battery)
        for i in range(3):
            marker = " "
            if i == selected:
                marker = ">"
            bar = "#" * (temperatures[i] // 5) + "." * (20 - temperatures[i] // 5)
            row(marker + " Tube " + "ABC"[i] + "  [" + bar + "]  " + str(temperatures[i]) + " C")
        print(border)
        print("\nTarget: ALL tubes exactly 85 C. Burnout: 100 C.")
        print("\nHeating effects:   A     B     C")
        print("Tube A:           +5    -5     0")
        print("Tube B:            0    +5    -5")
        print("Tube C:           -5     0   +10")
        print("\nA/D: cool/heat (-5%)   W/S: select tube")
        print("Q: quit")
        move = input("Control: ").strip().lower()
        if move == "q":
            return False
        if move in ("w", "s"):
            if move == "s":
                selected = (selected + 1) % 3
            else:
                selected = (selected - 1) % 3
        elif move in ("a", "d"):
            change = -1
            if move == "d":
                change = 1
            next_temperatures = []
            for i in range(3):
                next_temperatures.append(temperatures[i] + effects[selected][i] * change)
            if min(next_temperatures) < 0:
                message("Control rejected: temperature would fall below 0 C.")
                continue
            temperatures = next_temperatures
            battery -= 5
            if max(temperatures) >= 100:
                message("A tube burns out. Tonight's attempt has failed.")
                return False
            if battery == 0:
                break

    if battery < 10:
        message("Not enough battery to power the receiver. Tonight ends.")
        return False
    popup(["Vacuum tube control system repaired", "The radio is now operational"])
    frequency = 1200
    steps = [100, 10, 1]
    selected = 0
    locked = False

    while battery >= 10:
        panel("FREQUENCY DIAL", battery)
        row("DIAL: " + frequency_text(frequency) + " MHz")
        row()
        position = (frequency - 1200) * 40 // 1800
        row("12.00 |" + "-" * position + "^" + "-" * (40 - position) + "| 30.00")
        print(border)
        row("STEP: " + frequency_text(steps[selected]) + " MHz")
        print(border)
        print("\nA/D: lower/raise   W/S: larger/smaller step")
        print("E: receive (-10%)   N: notes   Q: quit")
        print("Moving the dial is free. Only receiving uses battery.")
        move = input("Control: ").strip().lower()
        if move == "q":
            return False
        if move == "n":
            notebook()
        elif move == "w":
            selected = max(0, selected - 1)
        elif move == "s":
            selected = min(2, selected + 1)
        elif move in ("a", "d"):
            change = -steps[selected]
            if move == "d":
                change = steps[selected]
            frequency = max(1200, min(3000, frequency + change))
        elif move == "e":
            battery -= 10
            if frequency == 1701:
                locked = True
                break
            message("DEFENCE LOCK: reception blocked. 10% battery consumed.")

    if not locked:
        message("Not enough battery for another reception attempt. Tonight ends.")
        return False

    popup([
        "This is Sta… tion E-zero…",
        "We are glad you…",
        "This is a trap…",
        "The government...",
        "It’s the harvest date…"
    ], typing=True)
    message("You: Come on, hold the signal... I can't catch a single word over this static!")
    knocks = 0
    while True:
        new_screen()
        print("A. Fix the squelch system")
        print("B. Knock on the radio")
        choice = input("Choice: ").strip().lower()
        if choice == "a":
            break
        if choice == "b":
            knocks += 1
            if knocks == 3:
                radio_fixed = True
                break
            message("The voice is still muffled and unclear.")

    feedback = ""
    while not radio_fixed and battery >= 10:
        new_screen()
        print(border)
        battery_display(battery)
        print(border)
        print("### WARNING: ILLEGAL RADIO USAGE VIOLATES WARTIME ACT ARTICLE 13. ###")
        print("### WARNING: DISCONNECT YOUR EQUIPMENT. AWAIT RESCUE TEAM. ###")
        print("\nSignal: ... identify ... reply ...")
        print("Enter the reply word to open the fictional signal filter.")
        print("Each reply costs 10%.   N: notes   Q: quit")
        print(feedback)
        reply = input("Reply: ").strip().upper()
        if reply == "Q":
            return False
        if reply == "N":
            notebook()
            continue
        if not reply:
            continue
        battery -= 10
        if reply == "READY":
            radio_fixed = True
        else:
            feedback = "Reply rejected. The warning loop continues."

    if not radio_fixed:
        message("Not enough battery for another reply. Tonight ends.")
        return False

    message("Radio repaired successfully.")
    popup([
        "Radio: This is Station E01.",
        "We are glad you managed to escape this deception using the clues we left behind —",
        "— the radiation and the nuclear … nuclear war are fake!",
        "There’s no such war or crisis. This is a trap, an experiment from the government.",
        "The government is actually suffering from a slow-burning genetic crisis on the surface.\nThey used the nuclear panic to trick thousands of genetically compatible civilians into locking themselves in pristine isolators.",
        "Day 7 isn’t an evacuation – it’s the harvest date when ‘specimens’ who maintained high health/suit integrity\nare selected for involuntary organ/tissue harvesting or gene-therapy research for the elite.",
        "We sincerely hope you will join us in exposing the government's deception. We are waiting for you at The … of H … !",
        "(audio interrupted)"
    ], one_by_one=True, typing=True)
    popup([
        "You: … If this is real, there’s no way I should wait for the ‘rescue team’ to come tomorrow. I have to find out what’s the truth.",
        "(You walked out of the shelter, taking off the Hazmat suit, exposing yourself to the air without any protective gear.)",
        "(10 minutes passed, nothing happened, you didn’t die because of the radiation.\nThe person from the radio was right, this is a lie. You know you shouldn’t stay here any longer.)",
        "You: I have to leave, I have to escape from this deception. The … H … place —\n— I don't know where it is, but I know I have to get out of this city as soon as possible.",
        "(You packed all the stuff u left in your bag.\nYou left the Hazmat suit in the shelter and started the wandering journey…)",
        "GAME OVER - SURVIVED",
        "HIDDEN ENDING - THE LAMB PREVENTS FROM SLAUGHTERING"
    ], one_by_one=True)
    new_screen()
    return True


if __name__ == "__main__":
    import pyfiglet
    from time import sleep
    rendertext = pyfiglet.figlet_format("WARNING", font="slant")
    print(rendertext)
    print("This module is for developer test only")
    sleep(1)
    final_puzzle()