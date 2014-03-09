import midi
import sys

def track_name(track):
  for ev in track:
    if isinstance(ev, midi.TrackNameEvent):
      return ''.join(map(chr, ev.data))
  name = 'no name, first 6 events:'
  for ev in track[:6]:
    name += '\n    %s' % ev
  return name

def main(argv):
  if len(argv) < 2:
    print 'usage: track_names.py file.mid'
    return

  mid = midi.read_midifile(argv[1])
  print '%d tracks' % len(mid)
  for i, t in enumerate(mid):
    print '  %03d: %s' % (i, track_name(t))

if __name__ == '__main__':
  main(sys.argv)
