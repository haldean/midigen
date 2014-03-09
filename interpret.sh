#!/bin/bash

FILE=$1
TRACKS=$2
if [ -z "$PYTHON" ]; then
  PYTHON='python'
fi

echo generating pickle...
$PYTHON gen.py $FILE $TRACKS dump.pickle && \
  echo running markov chain generator... && \
  $PYTHON markov.py dump.pickle 10000 && \
  echo converting back to midi... && \
  $PYTHON to_midi.py MarkovDisBitch.p $FILE out.mid && \
  echo playing... && \
  aplaymidi --port 129:0 out.mid
