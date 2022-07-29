import consts
from formatting import format_help

def help(prefix):
  for i in range(0, len(consts.commands)):
    str = consts.commands[i]
    consts.commands[i] = str[:3] + prefix + str[4:]

  return format_help(prefix)