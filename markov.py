import sys
import pickle
import random
from sets import Set
import sys

notes = pickle.load(open(sys.argv[1], 'r'))
k = int(sys.argv[2])

dictionary = {}

for i in range(0, len(notes)):
  this_value = notes[i][2]
  my_set = Set()
  if i < (len(notes) - 1): 
    my_set.add(notes[i+1])
    for j in range((i + 1), len(notes) -1):
      if (notes[j][2] == this_value) and (this_value not in dictionary.keys()):
        my_set.add(notes[j+1])
    dictionary[this_value] = my_set

print dictionary

start = random.choice(list(dictionary.keys()))
output_list = []

for i in range(0, k):    
  my_note = random.choice(list(dictionary[start]))
  print my_note
  output_list.append(my_note)
  start = my_note[2]
       
print output_list
