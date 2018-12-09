from collections import Counter

file_input = open('day03_part01_input.txt').read()

file_input = file_input.replace('@',';') # replace @ with ;
file_input = file_input.replace(':',';') # replace : with ;
file_input = file_input.replace(' ','') # remove white space

newline_list = file_input.split('\n')
# new_list will contain each 'claim' of fabric
new_list = []

for item in newline_list:
    # delimeter is now ;
    new_list.append(item.split(';'))

for x in range(len(new_list)):
    new_list[x][1] = new_list[x][1].split(',')
    new_list[x][2] = new_list[x][2].split('x')

for item in new_list:
    item[1][0] = int(item[1][0])
    item[1][1] = int(item[1][1])
    item[2][0] = int(item[2][0])
    item[2][1] = int(item[2][1])

#print(new_list)

xCoord_list = [item[1][0] for item in new_list]
yCoord_list = [item[1][1] for item in new_list]

width_span = [item[2][0] for item in new_list]
height_span = [item[2][1] for item in new_list]

max_xCoord = max(xCoord_list)
max_yCoord = max(yCoord_list)

x_index = xCoord_list.index(max_xCoord)
y_index = yCoord_list.index(max_yCoord)

maxGrid_x = max_xCoord + width_span[x_index]-1
maxGrid_y = max_yCoord + height_span[y_index]-1

print('Max grid size is {0} by {1}'.format(maxGrid_x,maxGrid_y))

grid_dictionary = {}

# item in new list looks like this -> ['#100',[200,200],[20,30]]
# grid_dictionary must be iterated over and initialized with a value of 0
for item in new_list:
    for x in range(1,item[2][0]+1):
        for y in range(1, item[2][1]+1):
            grid_dictionary[ (str(item[1][0]+x),str(item[1][1]+y)) ] = 0

# generate a set of all claims
all_claims_set = set()
for item in new_list:
    all_claims_set.add(item[0])
    for x in range(1, item[2][0]+1):
        for y in range(1, item[2][1]+1):
            grid_dictionary[ (str(item[1][0]+x),str(item[1][1]+y)) ] += 1

#print(grid_dictionary.keys())#,grid_dictionary.values())
c = Counter(grid_dictionary.values())
c.pop(1)

print(sum(c.values()))
#print(grid_dictionary)

# add overlapping keys to a set
overlapping_claims_set = set()

for item in new_list:
    for x in range(1, item[2][0]+1):
        for y in range(1, item[2][1]+1):
            if( grid_dictionary[ (str(item[1][0]+x),str(item[1][1]+y)) ] != 1 ):
                overlapping_claims_set.add(item[0])

print('all claims length ',len(all_claims_set))
print('overlapping claims length ',len(overlapping_claims_set))

print(all_claims_set.difference(overlapping_claims_set))