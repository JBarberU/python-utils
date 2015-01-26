#!/usr/bin/env python

import sys
sys.path += [
              ".",
              "..",
            ]

from commander import Commander
from progress_output_pipe import ProgressOutputPipe

def test_run_cmd(sleep_cmd):
  out = ProgressOutputPipe()
  commander = Commander(out)

  commander.run_command(["sh", "-c", "for x in {1..10}; do echo $x; %s done" % sleep_cmd])
  for i in range(1, 10):
    assert i == int(out.stdout[i-1])

def test_run_chained_cmd(sleep_cmd):
  out = ProgressOutputPipe()
  commander = Commander(out)

  commander.run_chained_commands([(["sh", "-c", "for x in {1..5} a b c d e; do echo $x; %s done" % sleep_cmd], []), (["grep", "-e", "\\d"], [])])
  assert len(out.stdout) == 5
  for i in range(1, 5):
    assert i == int(out.stdout[i-1])

def main():
  if "--no-sleep" in sys.argv:
    sleep_cmd = ""
  else:
    sleep_cmd = "python -c \"import time\ntime.sleep(0.1)\"; "

  test_run_cmd(sleep_cmd)
  test_run_chained_cmd(sleep_cmd)

if __name__ == "__main__": main()

