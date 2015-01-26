#!/usr/bin/env python

import unittest
from StringIO import StringIO

import sys
sys.path += [
              ".",
              "..",
            ]

from commander import Commander
from command_output_pipe_base import CommandOutputPipeBase, OutputError


class CommanderTester(unittest.TestCase):

# Test run_command

  def test_verbose_output(self):
    saved_stdout = sys.stdout
    try:
      out = StringIO()
      sys.stdout = out
      pipe = CommandOutputPipeBase(True)
      commander = Commander(pipe)
      commander.run_command(["echo", "Hello", "World!"])
      output = out.getvalue().strip()
      assert output == 'Hello World!'
    finally:
      sys.stdout = saved_stdout

  def test_silent_output_nonverbose_out(self):
    saved_stdout = sys.stdout
    try:
      out = StringIO()
      sys.stdout = out
      pipe = CommandOutputPipeBase(False)
      commander = Commander(pipe)
      commander.run_command(["echo", "Hello", "World!"])
      output = out.getvalue().strip()
      assert output == ''
    finally:
      sys.stdout = saved_stdout

  def test_silent_output_no_out(self):
    saved_stdout = sys.stdout
    try:
      out = StringIO()
      sys.stdout = out
      commander = Commander(None)
      commander.run_command(["echo", "Hello", "World!"])
      output = out.getvalue().strip()
      assert output == ''
    finally:
      sys.stdout = saved_stdout

  def test_get_lines(self):
    out = CommandOutputPipeBase(False)
    commander = Commander(out)
    commander.run_command(["echo", "Hello\nWorld"])
    assert out.stdout[0] == "Hello\n" and out.stdout[1] == "World\n"

  def test_unacceptable_output(self):
    out = CommandOutputPipeBase(False, ["unacceptable"])
    commander = Commander(out)
    self.assertRaises(OutputError, commander.run_command, ["echo", "some", "highly", "unacceptable", "message"])

  def test_acceptable_output(self):
    out = CommandOutputPipeBase(False, ["unacceptable"])
    commander = Commander(out)
    try:
      commander.run_command(["echo", "some", "highly", "acceptable", "message"])
    except:
      self.fail("run_command shouldn't have thrown an exception")

  def test_return_code(self):
    commander = Commander()
    assert commander.run_command(["echo", "Hello World!"]) == 0
    assert commander.run_command(["ls", "eaeuohtnuoeahtnouahtn"]) == 1

# Test run_chained_commands

  def test_simple_chained_command(self):
    commander = Commander()
    assert 0 == commander.run_chained_commands([(["echo", "hello world"], []), (["grep", "hello"], [])])

  def test_failing_chained_command(self):
    commander = Commander()
    assert 1 == commander.run_chained_commands([(["echo", "hello world"], []), (["grep", "auohetn"], [])])

  def test_longer_chained_command(self):
    commander = Commander()
    assert 0 == commander.run_chained_commands([(["echo", "hello world"], []), (["sed", "s/hello/mrcat/g"], []), (["sed", "s/mrcat/auohetn/g"], []), (["grep", "auohetn"], [])])

  def test_output_from_chained_command(self):
    out = CommandOutputPipeBase(False)
    commander = Commander(out)
    assert 0 == commander.run_chained_commands([(["echo", "hello world"], []), (["grep", "hello"], [])])
    assert out.stdout[0] == "hello world\n"

if __name__ == "__main__": unittest.main()

