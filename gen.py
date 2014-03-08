import midi
import sys

def merge_tracks(track1, track2):
  merged = []
  i1, i2 = 0, 0
  next_event_1, next_event_2 = track1[0].tick, track2[0].tick

  while i1 < len(track1) and i2 < len(track2):
    if next_event_1 < next_event_2:
      forward_by = track1[i1].tick
      track1[i1].tick = next_event_1
      merged.append(track1[i1])

      next_event_1 = track1[i1+1].tick
      next_event_2 -= forward_by
      i1 += 1

    else:
      forward_by = track2[i2].tick
      track2[i2].tick = next_event_2
      merged.append(track2[i2])

      next_event_1 -= forward_by
      next_event_2 = track2[i2+1].tick
      i2 += 1

  if i1 < len(track1):
    merged.extend(track1[i1:])
  elif i2 < len(track2):
    merged.extend(track2[i2:])
  return merged

def main(argv):
  if len(argv) < 2:
    print 'usage: gen.py file.mid'
    return
  mid = midi.read_midifile(argv[1])
  print mid

if __name__ == '__main__':
  main(sys.argv)
