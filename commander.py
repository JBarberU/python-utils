import subprocess
import operator
import sys
from time import sleep
from datetime import datetime

from command_output_pipe_base import CommandOutputPipeBase

class Commander:

  def __init__(self, command_output_pipe = None):
    self.command_output_pipe = command_output_pipe

  def run_command(self, args):
    if self.command_output_pipe:
      self.command_output_pipe.start()

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if self.command_output_pipe:
      while True:
        line = p.stdout.readline()
        if line != '':
          try:
            self.command_output_pipe.put_line(line)
          except RuntimeError as e:
            p.terminate()
            raise e
        else:
          break
    p.wait()
    if self.command_output_pipe:
      self.command_output_pipe.stop()
    return p.returncode

  """ commands is an array of touples with command+args and array with acceptable
  error codes. An example: [(["echo", "Hello World"], []), (["exit", "1"], [1])]"""
  def run_chained_commands(self, commands):
    if self.command_output_pipe:
      self.command_output_pipe.start()
    proc_list = []
    for (args, err_codes) in commands:
      if 0 not in err_codes:
        err_codes.append(0)

      if not proc_list:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      else:
        p = subprocess.Popen(args, stdin=proc_list[-1][0].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc_list[-1][0].stdout.close()
      proc_list.append((p, err_codes))

    if self.command_output_pipe:
      while True:
        line = proc_list[-1][0].stdout.readline()
        if line:
          self.command_output_pipe.put_line(line)
        else:
          break

    for (p, err_codes) in proc_list:
      p.wait()
      if p.returncode not in err_codes:
        if self.command_output_pipe:
          while True:
            line = p.stderr.readline()
            if line:
              self.command_output_pipe.put_error_line(line)
            else:
              break
          self.command_output_pipe.stop()

        return p.returncode

    if self.command_output_pipe:
      self.command_output_pipe.stop()
    return 0

