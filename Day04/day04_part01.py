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
# print(sorted_observation_array,sep='\n')

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
#   [ <- using an list(array) might be a mistake
#     # date when shift begins
#     {'1593-11-01': [0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1]},
#     {'1593-11-02': [0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0]}
#    ]
#}
guard_shift_dictionary = {}

# initialize the guard_shift_dictionary with all known guard keys and empty array

for guard in guards:
    # each guard key holds an empty list
    guard_shift_dictionary[guard] = []

# temp_guard_string will have scope over the iteration and will change as a new guard is discovered
temp_guard_string = ''
# shift date should be reset every loop
shift_date = ''
# temp_shift dictionary {'date':array[60]} should persist until all sleep/wake cycles are finished
# the cycle finishes when a new guard is discovered, at that point temp_shift is reset
temp_shift = {}

for observation in sorted_observation_array:
    # finding a guard in the observation denotes the beginning of the guard's shift

    # These variables will hold sleep and wake up minutes as two character strings '00' to '59'
    # they are reset after every iteration (once for every observation)
    falls_asleep_minute = ''    
    wakes_up_minute = ''

    # assumption is GUARD will always be found first regardless of what date they start their shift

    if GUARD in observation[1]:
        # temp_shift dictionary needs to be assigned to the guard (key) previously seen
        
        # guard_id holds the observed previous guard id if a guard has been previously seen
        if (temp_guard_string):
            guard_id = temp_guard_string[1]

        # assign the temp_shift dictionary to the guard_shift_dictionary[#id].append({'date':[shift]})
        # assignment should only be done once, as the list has the potential of allowing duplicate dictionaries
        # this assignment should only be done once all sleep wake cycles have been looped through
        # this happens at the discovery of a new guard, after which the temp_shift dictionary should be reset
        # assignment should only occur when temp_shift is not empty (has been through a previous cycle)
            if(temp_shift):
                guard_shift_dictionary[guard_id].append(temp_shift)

        # the previous guard's shift dictionary has been saved
        # overrides the previous temp_guard_string every time a new guard is seen
        temp_guard_string = observation[1].split(' ')

        # once the {guard_id: [array]} dictionary is appended to the guard_shift_dictionary
        # temp_shift dictionary needs to be cleared for the next guard not by the guard's shift
        temp_shift = {}
        # code assumes the first entry must be a guard starting a shift otherwise this would error as temp_guard_string[1] would be ''
        # assigns a 60 element array to guard '#xxxx' at 'time'

        # it can occur that a guard starts a shift but never falls asleep and therefore never wakes up
        # their key still needs to be in the dictionary? yes/ but maybe not

        #guard_shift_dictionary[ temp_guard_string[1] ] = {shift_date:shift.copy()}

    # obtain 'falls asleep' time
    if FALLS_ASLEEP in observation[1]:
        # create the array that will hold the guard's shift as a datetime string
        # shift_date holds a string for example: '1518-09-12'
        shift_date = observation[0].split(' ')[0]
        # create a dictionary {'datetime': [60 element array]} and assign
        
        # assign only if temp_shift is empty, otherwise the second cycle overwrites the first
        if (temp_shift):
            pass
        else:
            temp_shift[shift_date]= shift.copy()

        # falls_asleep_minute should be the minutes string taken from a string like this -> '1598-11-01 00:49'
        falls_asleep_minute = observation[0].split(' ')[1].split(':')[1]
        for x in range(int(falls_asleep_minute),SIXTY):
            # this pass will start at falls_asleep_minute index and keep assigning 1's to the end of the array
            temp_shift[shift_date][x] = 1
        
        #print(guard_shift_dictionary[temp_guard_string[1]][shift_date])
    
    if WAKES_UP in observation[1]:
        # create the array that will hold the guard shift at that datetime string
        shift_date = observation[0].split(' ')[0]
        #guard_shift_dictionary[ temp_guard_string[1] ] = {shift_date:shift.copy()}
        #wakes_up_minute_minute should be the minutes string taken from a string like this -> '1598-11-01 00:49'
        wakes_up_minute = observation[0].split(' ')[1].split(':')[1]
        for x in range(int(wakes_up_minute),SIXTY):
            # this pass will start a    wakes_up_minute index and keep assigning 0's to the end of the array masking erroneous 1's
            temp_shift[shift_date][x] = 0
            #guard_shift_dictionary[ temp_guard_string[1] ][shift_date][x] = 0
        
        
        #print(guard_shift_dictionary[temp_guard_string[1]][shift_date])

# for guard in guard_shift_dictionary.keys():
#     for date_keys in guard.keys():
#         print(guard, guard_shift_dictionary[guard][date_keys],sep='\n')

# print(guard_shift_dictionary)


# an array that will hold tuples of guard id's and their max sleep value summed from all shifts
guard_sleep_maximum_array = []

for guard_key in guard_shift_dictionary.keys():
    shift_keys = []
    guard_sleep_sum = 0

    for item in guard_shift_dictionary[guard_key]:
        shift_keys += item.keys()
    
    for k in range(len(guard_shift_dictionary[guard_key])):
        #print(guard_shift_dictionary[guard_key][k])
        guard_sleep_sum += sum(guard_shift_dictionary[guard_key][k][shift_keys[k]] )
    
    guard_sleep_maximum_array.append( (guard_key, guard_sleep_sum))

guard_sleep_maximum_array = sorted(guard_sleep_maximum_array, key = lambda item: item[1])

max_guard_id = guard_sleep_maximum_array[-1][0]

# print(max_guard_id)
# print(guard_sleep_maximum_array[-1])
# print(guard_sleep_maximum_array)
# now that we know who the sleepiest guard is we must iterate over every shift and sum the shift arrays together
# then we must find the day in which the guard fell asleep the most

# an array of with sixty 0's, each index represents a minute in a full hour
sleepiest_minute_array= shift.copy()
# shifts is a list of dictionaries of {date:shifts}
# print(guard_shift_dictionary[max_guard_id])

for shift_dictionary in guard_shift_dictionary[max_guard_id]:

    for value in shift_dictionary.values():
        for x in range(SIXTY):
            sleepiest_minute_array[x] += value[x]

print(sleepiest_minute_array)

sleepiest_minute = sleepiest_minute_array.index(max(sleepiest_minute_array))

print(sleepiest_minute)