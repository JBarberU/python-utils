import sys
import re

class OutputError(RuntimeError):
  pass

class CommandOutputPipeBase:

# unacceptable_output is usful for failing based on command output, rather than
# exitcode
  def __init__(self, verbose = True, unacceptable_output=[]):
    self.verbose = verbose
    self.unacceptable_output = unacceptable_output
    self.stdout = []
    self.stderr = []

  def put_line(self, line):
    self.stdout.append(line)

    if self.verbose:
      sys.stdout.write(line)

    for uo in self.unacceptable_output:
      if re.compile(uo).search(line):
        raise OutputError(line)

  def put_error_line(self, line):
    self.stderr.append(line)

    if self.verbose:
      sys.stderr.write(line)

    for uo in self.unacceptable_output:
      if re.compile(uo).search(line):
        raise OutputException(line)

  def start(self):
    pass

  def stop(self):
    pass

