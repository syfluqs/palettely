import os

class termcolor:
   __PURPLE = '\033[95m'
   __CYAN = '\033[96m'
   __DARK__CYAN = '\033[36m'
   __BLUE = '\033[94m'
   __GREEN = '\033[92m'
   __YELLOW = '\033[93m'
   __RED = '\033[91m'
   __BOLD = '\033[1m'
   __UNDERLINE = '\033[4m'
   __END = '\033[0m'
   __truecolor = False
   if os.environ['COLORTERM']=='truecolor':
      __truecolor = True

   @staticmethod
   def purple(text):
      return termcolor.__PURPLE+text+termcolor.END

   @staticmethod
   def cyan(text):
      return termcolor.__CYAN+text+termcolor.END

   @staticmethod
   def darkcyan(text):
      return termcolor.__DARKCYAN+text+termcolor.END

   @staticmethod
   def blue(text):
      return termcolor.__BLUE+text+termcolor.END

   @staticmethod
   def green(text):
      return termcolor.__GREEN+text+termcolor.END

   @staticmethod
   def yellow(text):
      return termcolor.__YELLOW+text+termcolor.END

   @staticmethod
   def red(text):
      return termcolor.__RED+text+termcolor.END

   @staticmethod
   def bold(text):
      return termcolor.__BOLD+text+termcolor.END

   @staticmethod
   def underline(text):
      return termcolor.__UNDERLINE+text+termcolor.END

   @staticmethod
   def rgb(text, c=(255,0,0)):
      if termcolor.__truecolor:
         return u"\033[38;2;{};{};{}m{}\x1b[0m".format(c[0],c[1],c[2],text)
      return text

   @staticmethod
   def rgb_box(c=(255,0,0),n=1):
      return termcolor.rgb(u"\u2588"*n,c)

   @staticmethod
   def get_term_size():
      return os.popen('stty size', 'r').read().split()