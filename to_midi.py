import midi
import pickle
import pprint
import random
import sys

GEN_TRACK_NAME = map(ord, list('Generated track'))

def gen_tempo_track(deets, end_tick):
  time_sig = None
  key_sig = None
  tempos = []
  for track in deets:
    for ev in track:
      if isinstance(ev, midi.TimeSignatureEvent):
        time_sig = ev
      elif isinstance(ev, midi.KeySignatureEvent):
        key_sig = ev
      elif isinstance(ev, midi.SetTempoEvent):
        tempos.append(ev)

  track = midi.Track()
  if time_sig is not None:
    time_sig.tick = 0
    track.append(time_sig)
  if key_sig is not None:
    key_sig.tick = 0
    track.append(key_sig)

  if tempos:
    t = 0
    while t < end_tick:
      tick = random.randint(0, 10000)
      tempo = random.choice(tempos)
      tempo.tick = tick
      track.append(tempo)
      t += tick

  track.append(midi.EndOfTrackEvent(tick=end_tick))
  return track

def gen_track(deets, evs, initial_tick=5):
  name_ev = midi.TrackNameEvent(data=GEN_TRACK_NAME)
  track = midi.Track()
  track.append(name_ev)

  events = []
  t = initial_tick
  for ev in evs:
    tick, off_tick, note, velocity = ev
    on = midi.NoteOnEvent()
    on.data = [note, velocity]
    off = midi.NoteOffEvent()
    off.data = [note, 0]

    t += tick
    events.append((t, on))
    events.append((t + off_tick, off))

  events = sorted(events)
  last_t = 0
  for t, ev in events:
    ev.tick = t - last_t
    last_t = t
    track.append(ev)

  track.append(midi.EndOfTrackEvent())
  return track, last_t

def main(argv):
  if len(argv) < 4:
    print 'usage: pickled copy_deets_from out_file'
    return
  pickled, copy_deets_from, out_file = argv[1:4]
  with open(pickled) as f:
    evs = pickle.load(f)
  deets_mid = midi.read_midifile(copy_deets_from)

  track, last_t = gen_track(deets_mid, evs)
  gen_mid = midi.Pattern()
  gen_mid.append(gen_tempo_track(deets_mid, last_t))
  gen_mid.append(track)
  midi.write_midifile(out_file, gen_mid)

if __name__ == '__main__':
  main(sys.argv)
