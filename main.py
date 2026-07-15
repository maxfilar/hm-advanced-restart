import pydirectinput as keyinput
import pygetwindow as window
import keyboard
import time
import sys
import os

WINDOW_NAME = "Hotline Miami"
GAME_MASKS = [
    "Richard", "Rasmus", "Tony", "Aubrey", "Don Juan", "Graham", 
    "Dennis", "George", "Ted", "Rufus", "Rami", "Willem", 
    "Peter", "Zack", "Oscar", "Rick", "Brandon", "Charlie", 
    "Louie", "Phil", "Nigel", "Earl", "Jones", "Carl", 
    "Jake", "Richter"
]
MASK_PICK = -1

def main():
    global MASK_PICK

    keyinput.PAUSE = 0.025
    keyboard.add_hotkey("R", game_restart)
 
    MASKS = set_masks_general(get_masks_save(),GAME_MASKS)

    try:
        print("\n\n * HMAR is working, press \"R\" to restart a level \n * Ctrl + C to stop the HMAR. " \
        "\n ! Warning №1: After releasing the button don't press anything until it won't pick a mask" \
        "\n ! Warning №2: HMAR supports only updated HM's version, see more in README.md\n")
        show_masks(MASKS)
        MASK_PICK = choose_mask(MASKS)
        keyboard.wait()
    except KeyboardInterrupt:
        sys.exit("\n * HMAR is stopped \n")


def game_restart():
    if MASK_PICK != -1:
        time.sleep(1)
        for key in ["esc", "s", "s", "enter", ["s"] * (MASK_PICK - 1), "enter"]:
            if window.getActiveWindow().title == WINDOW_NAME:
                keyinput.press(key) 
            else:
                print(" !!! THE GAME IS NOT OPENED")
                return
        time.sleep(1)
    
        

def get_masks_save():
    path = os.path.expanduser('~/Documents/My Games/HotlineMiami/SaveData.sav')
    file = open(path, "rb")
    lines = file.readlines()
    file.close()

    for line in lines:
        d_line = line.decode("utf-8", errors = 'ignore')
        if "saves.dat" in d_line:
            return d_line.split("saves.dat")[1].strip().replace("\x01", "").replace("\x00", "")

def set_masks_general(unlocked, all):
    array = []
    for i in range( len(all) ):
        array.append(
            {
                "name": all[i],
                "unlocked": unlocked[i]
            }
        )
    return array

def show_masks(list):
    print("* Masks avaliable: ")
    for i in range( len(list) ):
        print(f"  - {i+1}. {list[i]["name"]} ({"Unlocked" if list[i]["unlocked"] else "Locked"})")

def choose_mask(list):
    while True:
        try:
            num = int(input(" * Choose a number of your mask: "))
            
            if num < 1 or num > len(list):
                raise ValueError

            if not list[num - 1]["unlocked"]:
                print(" ! This mask is not unlocked \n")
                continue
            
            print(f" * You picked {list[num-1]["name"]}'s mask")
            return num
        except ValueError:
            print(" ! Write a correct number \n")
            continue

if __name__ == "__main__":
    main()