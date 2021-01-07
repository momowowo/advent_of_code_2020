import argparse
import sys
import re

#Set up arguments and read them in
parser = argparse.ArgumentParser()
parser.add_argument('file', help="File containing input rules. Required.")
args, unknown = parser.parse_known_args()

file = args.file

#Bag class def'n
"""
Data structure:

Bag
|_ Colour
|_ Contains

e.g.
"light red bags contain 1 bright white bag, 2 muted yellow bags":

Bag
|_ "light red"
|_ [(1, "bright white"), (2, "muted yellow")]

"""

class Bag:

    def __init__(self, colour):
        self.colour = colour
        self.contains = []

    def add_contents(self, colour, number):
        bags = (colour, number)
        self.contains.append(bags)

    def contains_colour(self, colour):
        for bag in self.contains:
            if bag[0] == colour:
                return True

#Parse the rules into a list of bags
all_bags = []

with open(file) as f:
    #Read the file all into one list
    print("Reading in file...")
    rules = f.readlines()
    numbags = len(rules)

    split_pattern = re.compile(r" bags contain ")
    child_pattern = re.compile(r"(\d+) (.*?) bag")
    
    for rule in rules:
        try:
            #Separate the rule into the bag colour and the contents of the bag
            parent_bag, bag_contents = split_pattern.split(rule)
        except ValueError as e:
            sys.exit("The rule: " + rule + "caused an error splitting the string")


        bag = Bag(parent_bag)
        
        #Parse the number and colour of the contents. There can be 0..n matches.
        child_bags = child_pattern.findall(bag_contents)
        if child_bags:
            for child_bag in child_bags:
                bag.add_contents(child_bag[1], child_bag[0])

        all_bags.append(bag)

#Solve part 1 of the problem (find the number of bag colors that can eventually contain at least one shiny gold bag)

num_bag_colours = 0  # Keeps track of the number of bag colours that can contain the specified colour
checked_bag_colours = [] # Keeps track of what colours we've already checked, in case a certain colour can be contained in multiple bag colours (not sure if this case can ever happen but let's handle it anyway)

def checkBag(colour):
    for bag in all_bags:
        if bag.contains_colour(colour):
            global num_bag_colours
            global checked_bag_colours

            if checked_bag_colours.count(bag.colour) == 0: # Check if we've already checked bags of this colour, so we don't double-count
                num_bag_colours += 1
                checkBag(bag.colour) # Now need to check the bags that might contain this new colour bag
            
            checked_bag_colours.append(bag.colour) # Mark this bag colour as checked
#End of checkBag function

checkBag("shiny gold")

print(str(num_bag_colours))

#Solve part 2 of the problem (How many individual bags are required inside your single shiny gold bag?)

#Returns the number of bags contained in "bag" + all the bags contained in "bag"
def countContents(bag):
    count = 0
    global all_bags # Just required so we can access the list containing all the Bag objects
    for inner_bag in bag.contains:  # For each coloured bag inside the current bag
        # Add the number of bags of this colour
        count += int(inner_bag[1])
        # Then find the Bag and recurse
        for b in all_bags: 
            if b.colour == inner_bag[0]: # Finding the correct bag by colour
                count += int(inner_bag[1]) * countContents(b) # Need to multiply by the number of inner_bags to get the accurate count!!
    
    return count
#End of countContents function

#Find the shiny gold bag and count it's contents recursively
count = 0

for bag in all_bags:
    if bag.colour == "shiny gold":
        count += countContents(bag)

print(str(count))
