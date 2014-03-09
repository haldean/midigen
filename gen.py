import midi
import pickle
import pprint
import sys

class ev(object):
  def __init__(self, tick, off_tick=None, note=None, velocity=None, tempo=None):
    self.tick = tick
    self.off_tick = off_tick
    self.note = note
    self.velocity = velocity
    self.tempo = tempo

  @property
  def is_tempo(self):
    return self.tempo is not None

def track_to_ev(track):
  evs = []
  for i in range(len(track)):
    n = track[i]
    if isinstance(n, midi.NoteOnEvent):
      tick = n.tick
      note_val = n.data[0]
      velocity = n.data[1]
      off_tick = 0
      for j in range(i+1, len(track)):
        n_ = track[j]
        off_tick += n_.tick
        if isinstance(n_, midi.NoteOffEvent):
          if n_.data[0] == note_val:
            break
      evs.append(ev(n.tick, off_tick, note=note_val, velocity=velocity))
    if isinstance(n, midi.SetTempoEvent):
      tempo = 0
      for d in n.data:
        tempo = tempo << 8 | d
      evs.append(ev(n.tick, tempo=tempo))
  return evs

def ev_times(evs):
  t = 0
  res = []
  for ev in evs:
    res.append((t, ev))
    t += ev.tick
  return res

def merge_evs(tracks):
  merged = []
  for t in tracks:
    merged.extend(t)
  merged = sorted(merged)
  last_t = 0
  for ev in merged:
    ev[1].tick = ev[0] - last_t
    last_t = ev[0]
  return merged

def dump(merged_evs):
  filtered = []
  last_t = 0
  for t, ev in merged_evs:
    if ev.is_tempo:
      continue
    filtered.append((t - last_t, ev.off_tick, ev.note, ev.velocity))
    last_t = t
  return filtered

def main(argv):
  if len(argv) < 4:
    print 'usage: gen.py file.mid tracks dump_to'
    return
  mid = midi.read_midifile(argv[1])
  tracks_to_keep = map(int, argv[2].split(','))
  tracks = []
  for t in tracks_to_keep:
    tracks.append(mid[t])
  tracks = merge_evs(map(ev_times, map(track_to_ev, tracks)))
  with open(argv[3], 'w') as f:
    pickle.dump(dump(tracks), f)

if __name__ == '__main__':
  main(sys.argv)
