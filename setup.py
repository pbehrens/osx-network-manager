from distutils.core import setup
import py2app

NAME = 'myapp'
SCRIPT = 'main.py'
VERSION = '0.1'
ID = 'myapp'

plist = dict(
     CFBundleName                = NAME,
     CFBundleShortVersionString  = ' '.join([NAME, VERSION]),
     CFBundleGetInfoString       = NAME,
     CFBundleExecutable          = NAME,
     CFBundleIdentifier          = 'com.yourdn.%s' % ID,
     LSUIElement                 = '1', #makes it not appear in cmd-tab task list etc.
)


app_data = dict(script=SCRIPT, plist=plist)

setup(
   app = [app_data],
   options = {
       'py2app':{
           'resources':[
               ],
           'excludes':[
               ]
           }
       }
)