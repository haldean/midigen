import sys
import pickle
import random
from sets import Set
import sys
import numpy as np


notes = pickle.load(open(sys.argv[1], 'r'))
k = int(sys.argv[2])

dictionary = {}

#get parameters from normal distribution (tick values)
my_array = []
for element in notes:
  my_array.append(element[0])

tick_standardDev = np.std(my_array)
tick_mean = np.mean(my_array) 
#print tick_mean

#print np.random.normal(tick_mean, tick_standardDev, 1)

for i in range(0, len(notes)):
  this_value = notes[i][2]
  my_set = Set()
  if i < (len(notes) - 1): 
    my_set.add(notes[i+1])
    for j in range((i + 1), len(notes) -1):
      if (notes[j][2] == this_value) and (this_value not in dictionary.keys()):
        my_set.add(notes[j+1])
    dictionary[this_value] = my_set

for element in dictionary:
  dictionary[element] = list(dictionary[element])

start = random.choice(list(dictionary.keys()))
output_list = []

for i in range(0, k):   
  my_tuple = [np.random.normal(tick_mean, tick_standardDev, 1)[0]]
  my_note = random.choice(list(dictionary[start]))
  my_tuple.append(my_note[1:])
  output_list.append(my_tuple)
  start = my_note[2]
  if random.randint(0, 100) < 5:
    start = random.choice(list(dictionary.keys()))
       
pickle.dump(output_list, open('MarkovDisBitch.p', 'wb'))
