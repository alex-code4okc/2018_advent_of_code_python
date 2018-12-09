GUARD = 'Guard'
FALLS_ASLEEP = 'falls asleep'
WAKES_UP = 'wakes up'

SIXTY = 60

# create a shift array of length 60, each index representing a minute (i.e. '01' is minute 1) of that shift
# this shift array will be the template for all shifts and will be initiated to 0 for all minutes

shift = []
for x in range(SIXTY):
    shift.append(0)

f = open('day04_part01_input.txt')

f_lines = f.read().replace('[','').replace(']','').split('\n')

observation_array = [[item[:16],item[17:]] for item in f_lines]

# sort by dates
sorted_observation_array = sorted(observation_array,key= lambda item: item[0])
#print(sorted_observation_array,sep='\n')

# sorted_observation_array has a the following structure:
# [ ['1518-08-17 00:38', 'falls asleep'], 
# '1518-10-07 00:02', 'Guard #2969 begins shift' ... ]

# a set containing all known guards
guards = set()

for observation in sorted_observation_array:
    if GUARD in observation[1]:
        temp_guard_string = observation[1].split(' ')
        guards.add(temp_guard_string[1])

# print(guards)
# print(len(guards))


# guard_shift_dictionary will hold a structure similar to the following:
# dictionary needs to be created for the guard, and a list of dictionaries for the date the shift occurs
# the actual shift will be a 60 element array, if the guard is asleep the index at that minute will have
# a value of 1, if awake the value of the array at that index (minute) will be 0

# {'#199':
#   [
#     # date when shift begins
#     {'1593-11-01': [0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1]},
#     {'1593-11-02': [0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0]}
#    ]
#}
guard_shift_dictionary = {}

# initialize the guard_shift_dictionary with all known guard keys

for guard in guards:
    # each guard key holds an empty list
    guard_shift_dictionary[guard] = []

# temp_guard_string will have scope over the iteration and will change as a new guard is discovered
temp_guard_string = ''
shift_date = ''
temp_shift = {}
for observation in sorted_observation_array:
    # finding a guard in the observation denotes the beginning of the guard's shift

    # These variables will hold sleep and wake up minutes as two character strings '00' to '59'
    falls_asleep = ''
    wakes_up = ''

    # assumption is GUARD will always be found first regardless of what date they start
    if GUARD in observation[1]:
        # subsequent observations need to be assigned to the guard previously seen
        # overrides temp_guard_string every time a new guard is seen
        temp_guard_string = observation[1].split(' ')
        
        # once assigned to the {guard_id: [array]} dictionary (guard_shift_dictionary)
        # temp_shift dictionary needs to be cleared for the next guard, not shift
        temp_shift = {}
        # code assumes the first entry must be a guard starting a shift otherwise this would error as temp_guard_string[1] would be ''
        # assigns a 60 element array to guard '#xxxx' at 'time'

        # it can occur that a guard starts a shift but never falls asleep and therefore never wakes up
        # their key still needs to be in the dictionary? yes/ but maybe not
        #guard_shift_dictionary[ temp_guard_string[1] ] = {shift_date:shift.copy()}

    # obtain 'falls asleep' time
    if FALLS_ASLEEP in observation[1]:
        # create the array that will hold the guard shift as a datetime string
        shift_date = observation[0].split(' ')[0]
        # create a dictionary {'datetime': [60 element array]} and assign
        temp_shift[shift_date]= shift.copy()

        # falls_asleep should be the minutes string taken from a string like this -> '1598-11-01 00:49'
        falls_asleep = observation[0].split(' ')[1].split(':')[1]
        for x in range(int(falls_asleep),SIXTY):
            # this pass will start at falls_asleep index and keep assigning 1's to the end of the array
            temp_shift[shift_date][x] = 1
        
        #print(guard_shift_dictionary[temp_guard_string[1]][shift_date])
    
    if WAKES_UP in observation[1]:
        # create the array that will hold the guard shift at that datetime string
        shift_date = observation[0].split(' ')[0]
        #guard_shift_dictionary[ temp_guard_string[1] ] = {shift_date:shift.copy()}
        # falls_asleep should be the minutes string taken from a string like this -> '1598-11-01 00:49'
        wakes_up = observation[0].split(' ')[1].split(':')[1]
        for x in range(int(wakes_up),SIXTY):
            # this pass will start at wakes_up index and keep assigning 0's to the end of the array masking erroneous 1's
            temp_shift[shift_date][x] = 0
            #guard_shift_dictionary[ temp_guard_string[1] ][shift_date][x] = 0
        #assign the temp_shift dictionary to the guard_shift_dictionary[#id].append({'date':[shift]})
        guard_shift_dictionary[temp_guard_string[1]].append(temp_shift)
        
        #print(guard_shift_dictionary[temp_guard_string[1]][shift_date])

# for guard in guard_shift_dictionary.keys():
#     for date_keys in guard.keys():
#         print(guard, guard_shift_dictionary[guard][date_keys],sep='\n')

#print(guard_shift_dictionary)

# an array that will hold tuples of guard id's and their max sleep value summed from all shifts
guard_sleep_maximum_array = []

for guard_key in guard_shift_dictionary.keys():
    keys = []
    guard_sleep_sum = 0

    for item in guard_shift_dictionary[guard_key]:
        keys += item.keys()
    
    for k in range(len(guard_shift_dictionary[guard_key])):
        
        guard_sleep_sum += sum(guard_shift_dictionary[guard_key][k][keys[k]] )
    
    guard_sleep_maximum_array.append( (guard_key, guard_sleep_sum))

guard_sleep_maximum_array = sorted(guard_sleep_maximum_array, key = lambda item: item[1])

max_guard_id = guard_sleep_maximum_array[-1][0]

#print(max_guard_id)
# now that we know who the sleepiest guard is we must iterate over every shift and sum the shift arrays together
# then we must find the day in which the guard fell asleep the most

# an array of with sixty 0's, each index represents a minute in a full hour
sleepiest_day = shift.copy()
# shifts is a list of dictionaries of {date:shifts}
print(guard_shift_dictionary[max_guard_id])

# for shifts in guard_shift_dictionary[max_guard_id]:
#     print(len(shifts))
#     # temporary store for dictionary keys inside list
#     keys = []
#     print(shifts)
#     # shifts is an array of dictionaries {'date': 'array'}
#     for item in shifts:
#         keys += item
#     print(keys)
#     for k in range(len(shifts)):
#         s_dict = shifts[k]
#         s_array = s_dict[keys[k]]
#         for x in range(SIXTY):
#             sleepiest_day[x] += s_array[x]

# print(sleepiest_day) 