import time
import numpy as np
import pandas as pd

#calories, carbs, protein, total_fat, sat_fat, trans_fat, sodium, sugar, fiber
meal_stats = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]).astype(float)

#extras, like misc
toppings_there = False

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
        restaurant = input('\nOut of ChickfilA, Chipotle, FiveGuys, and Fuddruckers, where are you eating today?:\n').lower().replace(" ", "")
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
    repeat(restaurant_type)

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

def read(filename): #this function returns 4 things, the first two are lists as numpy arrays (they are the broad categories and subcategories), the second two are dictionaries (for finding the menu items in the numpy arrays)
    df = pd.read_csv(f"{filename}.csv")
    counter = 0 #counter for the menu dictionary, to map the values
    subcounter = 0 #counter for the submenu dictionary, to map the values
    first = True
    list = [] #larger list for the sublists
    sublist = [] #list of the nutritional facts of each menu item
    menu_list = [] #larger list for the menu_sublists
    menu_sublist = [] #list of the item name
    menu_dict = {} #this is the menu dictionary that we will return, this is the big categories (burgers, fries, sandwiches)
    submenu_dict = {} #this is the submenu dictionary that we will return, it is 2d
    subsubmenu_dict = {} #this is the subcategories (hamburger, salad)
    for row in df.itertuples(name=None): #iterates over each row as a tuple
        if(pd.isna(row[2])): #determines if the second column of a row, in this case, calories, is an empty field, if it is an empty field, it adds the previous sublist
            if first:
                first = False
                menu_dict[row[1].lower()] = counter
                counter += 1
            elif row[1] == 'Toppings':
                global toppings_there
                toppings_there = True
            else:
                list.append(sublist)
                menu_list.append(menu_sublist)
                sublist = []
                menu_sublist = []
                menu_dict[row[1].lower()] = counter
                counter += 1
            subcounter = 0
        else:
            submenu_dict[row[1].lower()] = subcounter
            menu_sublist.append(row[1].lower())
            row = pd.to_numeric(row, errors='coerce')
            new_row = row[2:] #takes off all values from the front except for the nutritional facts, we have to do it like this since it is a tuple
            sublist.append(new_row)
            subcounter += 1
    return np.array(list), np.array(menu_list), menu_dict, submenu_dict

def options(list, type): #puts the items in a nice line
    options_string = ""
    size = len(list)
    counter = 0
    first = True
    for elements in list:
        if first:
            options_string += elements
            first = False
        elif counter == size - 1:
            options_string = options_string + f", {type} " + elements
        elif elements == "":
            options_string = options_string
        else:
            options_string = options_string + ", " + elements
        counter += 1
    return options_string

def format_list(list):
    new_list = []
    for element in list:
        new_list.append(element.replace(" ", ""))
    return new_list

def fastfood(restaurant):
    restaurant_facts, restaurant_menu, restaurant_menu_dict, restaurant_submenu_dict = read(restaurant)
    while True:
        global meal_stats
        food = input(f"\nWhat're you tryna eat?  Please state whether you want a {options(list(restaurant_menu_dict.keys()), 'or')}, f a t t y:\n").lower().replace(" ", "")
        if food in format_list(list(restaurant_menu_dict.keys())):
            restaurant_menu_dict =  {k.replace(" ", ""): v for k, v in restaurant_menu_dict.items()}
            while True:
                food_type = input(f"\nOut of a {options(restaurant_menu[restaurant_menu_dict[food]], 'or')}, which one do you want?:\n").lower().replace(" ", "")
                if food_type in format_list(restaurant_menu[restaurant_menu_dict[food]]):
                    restaurant_submenu_dict =  {k.replace(" ", ""): v for k, v in restaurant_submenu_dict.items()}
                    print_message("\nMhm, delicious.")
                    meal_stats += restaurant_facts[restaurant_menu_dict[food]][restaurant_submenu_dict[food_type]]
                    break
                else:
                    print_message("Didn\'t understand, try again.")
                    continue
        else:
            print_message("Try again.")
            continue
        if toppings_there:
            toppings(food, restaurant)
        print_message("Calculating nutritional info...\n\n")
        print_message("So ...\n\n")
        print_message("Much ...\n\n")
        print_message("Obesity!!!!!\n\n ")
        print_message(f"\n\nYour meal contains:\n{meal_stats[0]} calories \n{meal_stats[1]} grams of carbs \n{meal_stats[2]} grams of protein \n{meal_stats[3]} grams of total fat \n{meal_stats[4]} grams of saturated fat \n{meal_stats[5]} grams of trans fat \n{meal_stats[6]} milligrams of sodium \n{meal_stats[7]} grams of sugar \n{meal_stats[8]} grams of fiber\n")
        print_message("Whew! That's a lot of calories.")
        #remove this from function, add it after intro at the bottom
        break

def toppings(food, restaurant):
    toppings_facts, toppings_menu, toppings_menu_dict, toppings_submenu_dict = read(restaurant + "Toppings")
    #A1 Sauce, barbeque, green peppers, grilled mushrooms, hot sauce, jalapenos, ketchup, lettuce, mayo, mustard, onions, pickles, relish, tomatoes
    food_type = food + "toppings"
    toppings_list = []
    other_submenu_dict = toppings_submenu_dict
    other_submenu_dict = {k.replace(" ", ""): v for k, v in other_submenu_dict.items()}
    toppings_menu_dict =  {k.replace(" ", ""): v for k, v in toppings_menu_dict.items()}
    toppings_submenu_dict = {v: k for k, v in toppings_submenu_dict.items()}
    menu_list = toppings_menu[toppings_menu_dict[food_type]]
    global meal_stats
    if food_type in list(toppings_menu_dict.keys()):
        while True:
            toppings_input = input(f"\nThe toppings available are:\n\n{options(menu_list, 'or')}\n\nWhat toppings do you want? \nIf you don't want toppings or are finished, leave the response blank and presss enter:\n\n").lower().replace(" ", "")
            if not toppings_input:
                return
            elif toppings_input not in format_list(toppings_menu[toppings_menu_dict[food_type]]) and (toppings_input in toppings_list):
                print_message(f"\nYou already added that topping in your {food_type}.")
                continue
            elif toppings_input not in format_list(toppings_menu[toppings_menu_dict[food_type]]):
                print_message(f"\n{toppings_input.capitalize()} is not one of the options!")
                continue
            meal_stats += toppings_facts[toppings_menu_dict[food_type]][other_submenu_dict[toppings_input]]
            toppings_list.append(toppings_input)
            print(other_submenu_dict)
            print(toppings_submenu_dict)
            print(toppings_submenu_dict[other_submenu_dict[toppings_input]])
            menu_list[menu_list == toppings_submenu_dict[other_submenu_dict[toppings_input]]]
            print_message(f"\nIn your {food_type}, you have {options(toppings_list, 'and')}.")

main()
