# This is an example setup.py file
# run it from the windows command line like so:
# > C:\Python2.4\python.exe setup.py py2exe
 
from distutils.core import setup
 
import py2exe, glob
import pygame.mixer
 
opts = { 
 "py2exe": { 
   # if you import .py files from subfolders of your project, then those are
   # submodules.  You'll want to declare those in the "includes"
   'includes':['pygame.mixer.music']
   #            'data.glarf',
   #            'data.glarf.chardef',
   #           ],
 } 
} 
 
setup(
 
  #this is the file that is run when you start the game from the command line.  
  console=['main.py'],
 
  #options as defined above
#  options=opts,
options = {'py2exe': {'optimize': 2, 'bundle_files':1}}, 
  #data files - these are the non-python files, like images and sounds
  #the glob module comes in handy here.
  data_files = [
    ("img", glob.glob("img\\*.png")),
    ("fonts", glob.glob("fonts\\*.*")),
    ("sounds", glob.glob("snd\\*.*")),
    ("maps", glob.glob("maps\\*.*")),
    ("choons", glob.glob("choons\\*.*")),
  ],
 
)
