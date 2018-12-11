f = open('day05_part01_input.txt')

polymer = f.read()

polymer_lower_set = set(polymer.lower())

polymer_matching_characters_list = []

for item in polymer_lower_set:
    polymer_matching_characters_list.append(item+item.upper())
    polymer_matching_characters_list.append(item.upper()+item)

polymer_length = 0

while( polymer_length != len(polymer)):
    polymer_length = len(polymer)
    for item in polymer_matching_characters_list:
        if item in polymer:
            polymer =  polymer.replace(item,'')

print(len(polymer))