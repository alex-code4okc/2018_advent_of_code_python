summed_value = 0

calculated_sum_set = set()

matched_value = None
# adding the initial value to the calculated frequency list
calculated_sum_set.add(summed_value)


input_list = [int(x.strip()) for x in open('day01_part02_input.txt').readlines()]

#print(input_list)
count = 0
while(matched_value == None):

    for item in input_list:
        count += 1
        summed_value += item
        if summed_value in calculated_sum_set:
            matched_value = summed_value
            print(summed_value)
            #print('found it!')
            break
        calculated_sum_set.add(summed_value)

#print(count)
#print(len(calculated_sum_set))