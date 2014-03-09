#!/bin/bash

FILE=$1
TRACKS=$2
python gen.py $FILE $TRACKS dump.pickle && \
  python markov.py dump.pickle 10000 && \
  python to_midi.py MarkovDisBitch.p $FILE out.mid && \
  aplaymidi --port 129:0 out.mid
