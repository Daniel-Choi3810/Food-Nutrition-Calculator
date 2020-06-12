import time
import numpy as np
import pandas as pd

#calories, carbs, protein, total_fat, sat_fat, trans_fat, sodium, sugar, fiber
meal_stats = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]).astype(float)

#extras, like misc
toppings = False


fastfood_menu = {}
fastfood_submenu = {}
toppings_menu = {}

def main():
    print_message("\nWhat's up fatass!")
    print_message("\nYou ready to grub you pig?!")
    intro()


def print_message(string):  # Delays each print statement by .7 seconds.
    # Parameter is any string.
    print(string)
    time.sleep(.7)


def intro():
    while True:
        restaurant_type = ""
        restaurant = input('\nOut of ChickfilA, Chipotle, FiveGuys, and Fuddruckers, where are you eating today?:\n')
        if 'five' in restaurant:
            print_message("\nFiveGuys, that's tuff.")
            restaurant_type = "FiveGuys"
            break
        elif 'chick' in restaurant:
            print_message("\nChick-Fil-A, that's tuff.")
            restaurant_type = "ChickFilA"
            break
        elif 'chipotle' in restaurant:
            print_message("\nChipotle, that's tuff.")
            restaurant_type = "Chipotle"
            break
        elif 'fud' in restaurant:
            print_message("\nFuddruckers, that's tuff.")
            restaurant_type = "Fuddruckers"
            break
        else:
            print_message("Learn to spell, holy shit. Try again.")
            continue
    fastfood(restaurant_type)

def repeat(restaurant):
    while True:
        more_food = input('\nAre you eating more food?  Please type yes or no: \n').lower()
        if more_food == 'yes':
            print_message("Christ you fatass, alright.")
            fastfood(restaurant)
        elif more_food == 'no':
            print_message("\nThank god, go exercise.")
            break
        else:
            print_message("\nDidn't get that, try again.")

def read(filename): #reads a file and populates the fastfood_menu and fastfood_submenu
    df = pd.read_csv(f"{filename}.csv")
    counter = 0 #counter for the fastfood_menu dictionary, to map the values
    subcounter = 0 #counter for the fastfood_submenu dictionary, to map the values
    first = True
    list = [] #larger list for the sublists
    sublist = [] #list of the nutritional facts of each menu item
    menu_list = [] #larger list for the menu_sublists
    menu_sublist = [] #list of the item name
    global fastfood_menu
    for row in df.itertuples(name=None): #iterates over each row
        if(pd.isna(row[2])): #determines if the second column of a row, in this case, calories, is an empty field, if it is an empty field, it adds the previous sublist
            if first:
                first = False
                fastfood_menu[row[1].lower()] = counter
                counter += 1
            elif row[1] == 'Toppings':
                global toppings
                toppings = True
            else:
                list.append(sublist)
                menu_list.append(menu_sublist)
                sublist = []
                menu_sublist = []
                fastfood_menu[row[1].lower()] = counter
                counter += 1
            subcounter = 0
        else:
            global fastfood_submenu
            fastfood_submenu[row[1].lower()] = subcounter
            menu_sublist.append(row[1].lower())
            row = pd.to_numeric(row, errors='coerce')
            new_row = row[2:] #takes off all values from the front except for the nutritional facts
            sublist.append(new_row)
            subcounter += 1
    return np.array(list), np.array(menu_list)

def options(list):
    options_string = ""
    size = len(list)
    counter = 0
    first = True
    for elements in list:
        if first:
            options_string += elements
            first = False
        elif counter == size - 1:
            options_string = options_string + ", or " + elements
        else:
            options_string = options_string + ", " + elements
        counter += 1
    return options_string

def fastfood(restaurant):
    restaurant_facts, restaurant_menu = read(restaurant)
    while True:
        global meal_stats
        food = input(f"\nWhat're you tryna eat?  Please state whether you want a {options(list(fastfood_menu.keys()))}, f a t t y:\n").lower()
        if food in list(fastfood_menu.keys()):
            while True:
                food_type = input(f'\nOut of a {options(restaurant_menu[fastfood_menu[food]])}, which one do you want?:\n').lower()
                if food_type in restaurant_menu[fastfood_menu[food]]:
                    print_message("\nMhm, delicious.")
                    meal_stats += restaurant_facts[fastfood_menu[food]][fastfood_submenu[food_type]]
                    break
                else:
                    print_message('Didn\'t understand, try again.')
                    continue
        else:
            print_message("Try again.")
            fastfood(restaurant)
        #toppings(food)
        print_message("Calculating nutritional info...\n\n")
        print_message("So ...\n\n")
        print_message("Much ...\n\n")
        print_message("Obesity!!!!!\n\n ")
        print_message(f"\n\nYour meal contains:\n{meal_stats[0]} calories \n{meal_stats[1]} grams of carbs \n{meal_stats[2]} grams of protein \n{meal_stats[3]} grams of total fat \n{meal_stats[4]} grams of saturated fat \n{meal_stats[5]} grams of trans fat \n{meal_stats[6]} milligrams of sodium \n{meal_stats[7]} grams of sugar \n{meal_stats[8]} grams of fiber\n")
        print_message("Whew! That's a lot of calories.")
        #remove this from function, add it after intro at the bottom
        break

def toppings(food):
    #A1 Sauce, barbeque, green peppers, grilled mushrooms, hot sauce, jalapenos, ketchup, lettuce, mayo, mustard, onions, pickles, relish, tomatoes
    fiveguys_toppings = np.array()
    your_fb_toppings = []
    your_ff_toppings = []
    global meal_stats
    toppings_dict = {'A1 Sauce': 0, 'barbeque': 1, 'green peppers': 2, 'grilled mushrooms': 3, 'hot sauce': 4, 'jalapenos': 5, 'ketchup': 6, 'lettuce': 7, 'mayo': 8, 'mustard': 9, 'onions': 10, 'pickles': 11, 'relish': 12, 'tomatoes': 13}
    if 'burger' in food:
        while True:
            burger_toppings = input(f"\nThe toppings available are:\n\n{toppings_list}\n\nWhat toppings do you want? Please be specific to the spelling listed. \nIf you don't want toppings or are finished, leave the response blank and presss enter:\n\n")
            if not burger_toppings:
                return
            elif burger_toppings not in toppings_list and (burger_toppings in fiveguys_toppings):
                print_message('\nYou already added that topping in your burger.')
                continue
            elif burger_toppings not in toppings_list:
                print_message(f"\n{burger_toppings.capitalize()} is not one of the options!")
                continue
            meal_stats += fiveguys_toppings[toppings_dict[burger_toppings]]
            toppings_list.remove(burger_toppings)
            your_fb_toppings.append(burger_toppings)
            print_message(f'\nIn your burger, you have {your_fb_toppings}.')
    elif 'fries' in food:
        while True:
            fries_sauce = input(f"\nThe toppings available are:\n\n{ff_list}\n\nWhat sauces do you want? Please be specific to the spelling listed. \nIf you don't want sauces or are finished, leave the response blank and press enter: \n\n")
            if not fries_sauce:
                return
            elif fries_sauce in fiveguys_toppings and fries_sauce not in ff_list:
                print_message('\nYou already added that topping in your burger.')
                continue
            elif fries_sauce not in ff_list:
                print(f"\n{fries_sauce.capitalize()} is not one of the options!")
                continue
            meal_stats += fiveguys_toppings[toppings_dict[fries_sauce]]
            ff_list.remove(fries_sauce)
            your_ff_toppings.append(fries_sauce)
            print_message(f'\nFor your fries, you have {your_ff_toppings}')

main()
