import objc, re, os
from Foundation import *
from AppKit import *

from PyObjCTools import AppHelper, NibClassBuilder
import time

class MyApp(NSObject):
    

    def applicationDidFinishLaunching_(self, notification):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        # self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('Example')
        self.statusitem.setTitle_('Example')

        #make the menu
        self.menubarMenu = NSMenu.alloc().init()

        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Click Me', 'clicked:', '')
        self.menubarMenu.addItem_(self.menuItem)

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)

    def clicked_(self, notification):
        NSLog('clicked!')

# if __name__ == "__main__":
#     app = NSApplication.sharedApplication()
#     AppHelper.runEventLoop()
if __name__ == "__main__":
    # prepare and set our delegate
    app = NSApplication.sharedApplication()
    delegate = MyApp.alloc().init()
    app.setDelegate_(delegate)

    # let her rip!-)
    AppHelper.runEventLoop()

# class TheDelegate(NSObject):
# 
#   statusbar = None
#   state = 'idle'
# 
#   def applicationDidFinishLaunching_(self, notification):
#     statusbar = NSStatusBar.systemStatusBar()
#     self.statusitem = statusbar.statusItemWithLength_(
#         NSVariableStatusItemLength)

# 
#     self.menu = NSMenu.alloc().init()
#     menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
#         'Quit', 'terminate:', '')
#     self.menu.addItem_(menuitem)
#     self.statusitem.setMenu_(self.menu)
# 
#   def writer(self, s):
#     self.badge.setBadgeLabel_(str(s))
# 
# if __name__ == "__main__":
#   # prepare and set our delegate
#   app = NSApplication.sharedApplication()
#   delegate = TheDelegate.alloc().init()
#   app.setDelegate_(delegate)
#   delegate.badge = app.dockTile()
# 
#   # let her rip!-)
#   AppHelper.runEventLoop()