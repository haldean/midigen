import midi
import sys

def main(argv):
  if len(argv) < 2:
    print 'usage: dump_midi.py file.mid'
    return
  print midi.read_midifile(argv[1])

if __name__ == '__main__':
  main(sys.argv)
