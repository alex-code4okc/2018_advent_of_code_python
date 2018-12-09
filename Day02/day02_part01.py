from collection import Counter

f = open('day02_part01_input.txt').read()

fl = f.split('\n')

fl.remove('')

twos = 0

threes = 0

label_counters = [Counter(item) for item in fl]

for item in label_counters:
    if 2 in item.values():
        twos += 1
    if 3 in item.values():
        threes += 1

answer = twos*threes

print(answer)