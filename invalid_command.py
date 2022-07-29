from formatting import format_invalid_command
import consts

def invalid_command(prefix):
  for i in range(0, len(consts.commands)):
    str = consts.commands[i]
    consts.commands[i] = str[:3] + prefix + str[4:]

  return format_invalid_command(prefix)