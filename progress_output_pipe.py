from colors import Colors
from command_output_pipe_base import CommandOutputPipeBase
from log import Log

class ProgressOutputPipe(CommandOutputPipeBase):

  def __init__(self):
    CommandOutputPipeBase.__init__(self, False)

  def put_line(self, line):
    CommandOutputPipeBase.put_line(self, line)
    Log.raw("{0}.{1}".format(Colors.GREEN_FG, Colors.NORMAL), new_line = False)

  def start(self):
    Log.print_msg(title = "Progress", msg = "", color = Colors.MAGENTA_FG, new_line = False)

  def stop(self):
    Log.raw(" Done!", new_line = True)


