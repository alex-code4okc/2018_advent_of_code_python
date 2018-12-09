file_input = open('day02_part01_input.txt').read()

label_ids = file_input.split('\n')

label_ids.remove('')

index1 = 0
index2 = 0

sum_differences = 0

for label1 in label_ids:
    for label2 in label_ids:
        # print(label1,label2,sep='\n')

        for x in range(len(label1)):
            if( label1[x]==label2[x]):
                # do nothing
                pass
            else:
                # keep summing the occurence of differences in characters
                #print(label1[x])
                sum_differences += 1
        if(sum_differences == 1):
            # only 1 difference in characters was detected between labels
            index1 = label_ids.index(label1)
            index2 = label_ids.index(label2)
            break
        sum_differences = 0



matched_id1 = label_ids[index1]
matched_id2 = label_ids[index2]

matched_id1_set = set(matched_id1)

matched_id2_set = set(matched_id2)

# set_difference is a string
set_difference = list(matched_id1_set.symmetric_difference(matched_id2_set))[0]

if set_difference in matched_id1:
    matched_id1 = matched_id1.replace(set_difference,'')
    print(matched_id1)
elif set_difference in matched_id2:
    matched_id2 = matched_id2.replace(set_difference,'')
    print(matched_id2)