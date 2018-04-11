from Core.Singelton import Singelton
from threading import Thread, Lock, Condition
import curses
import Core.Utility as Core

'Single stroke Keyboard -> New event, meaning of the key is unknown - enter as a different meaning than a simple letter, and tab for instance.' \
'An event is created, the event is transformed from the keyboard agent to reactor (maybe a big word for a single source) polling service, the polling' \
'will transfer the event to the processing.' \
'Buffer with in each producer and an event representing which one is ready, a general event will be signaled and then questioning each source' \
'Event type - KeyStroke, keyboard input agent with in the Terminal will produce it' \
'Command validator, Terminal (for rendering) will be the consumers.' \
'Enter pressed - Command validator will be the consumer' \
'Command validator Invalid command/Valid command event - Terminal (rendering), GRPC client will be the consumers.' \
'Tab pressed - Command validator will be the consumer.' \
'Auto complete - Terminal (rendering) will be the consumer' \
'Each subscriber of an event need to provide a clouser (lambda for example) acting as a callback' \

class CursesConfigure:
    def __enter__(self):
        mainWindow = curses.initscr()
        curses.start_color() #Allow color
        curses.use_default_colors() # Allows the usage of default color
        curses.noecho() #Don't echo back keystroke
        curses.cbreak() #React to keys instantly, no enter is required
        mainWindow.border()
        mainWindow.refresh()
    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.endwin()

class Window(object):
    def __init__(self, yBegin, xBegin, height, width):
        self.__running = True
        self.__thread = None
        self.__window = curses.newwin(height, width, yBegin, xBegin)
        self.__window.border()
        self.__window.refresh()

class TextWindow(Window):
    def __init__(self, yBegin, xBegin, height, width):
        super(TextWindow, self).__init__(yBegin, xBegin, height, width)
        self.__textWindow = self._Window__window.subwin(height - 2, width - 2, yBegin + 1, xBegin + 1)
        self.__textWindow.scrollok(True)
        self.__lock = Lock()
        self.__thread = None
        self.__running = False
        self.__textWindowHeight, self.__textWindowWidth = self.__textWindow.getmaxyx()
        self.__backSpaceLocation = [0]*self.__textWindowHeight

        self.__inputSubscribers = {127 : [lambda y, x : self.handleBackSpace(y, x)],
                                   10  : [lambda y, x  : self.handleEnter(y, x)]}

    def __del__(self):
        self.__running = False
        self.__thread.join()

    def start(self):
        self.__running = True
        self.__thread = Thread(None, self.readLoop, 'TextWindow event loop', (), {})
        self.__thread.start()

    def stop(self):
        self.__running = False

    def subscribe(self, key, callback):
        if not hasattr(callback, '__call__'):
            raise AttributeError('callback is not callable')
        with Core.LockGuard(self.__lock):
            self.__inputSubscribers[key].append(callback)

    def readLoop(self):
        while self.__running == True:
            key = self.__textWindow.getch()
            (y, x) = self.__textWindow.getyx()

            if self.__inputSubscribers.has_key(key):
                for handler in self.__inputSubscribers[key]:
                    handler(y, x)
            else:
                self.__textWindow.addch(key)
                self.__backSpaceLocation[y]+=1

            self.__textWindow.refresh()

    def handleBackSpace(self, y, x):
        if y == 0 and x == 0:
            return
        if x == 0:
            self.__textWindow.move(y - 1, max(self.__backSpaceLocation[y - 1] - 1, 0))
            if self.__backSpaceLocation[y - 1] > 0:
                self.__backSpaceLocation[y - 1] = max(self.__backSpaceLocation[y - 1] - 1, 0)
        else:
            self.__textWindow.move(y, x - 1)
            self.__backSpaceLocation[y]-=1

        self.__textWindow.delch()

    def handleEnter(self, y, x):
        if y + 1 == self.__textWindowHeight:
            self.__textWindow.scroll()
            self.__textWindow.move(y, 0)
            del self.__backSpaceLocation[0]
        else:
            self.__textWindow.move(y + 1, 0)

class Terminal:
    __metaclass__ = Singelton
    def __init__(self):
        self.__completeCv = Condition()
        self.__textWindow = TextWindow(0, 0, 8, 30)

    def start(self):
        self.__textWindow.start()

    def notifyCompletion(self):
        self.__completeCv.acquire()
        self.__completeCv.notify()
        self.__completeCv.release()


    def waitForCompletion(self):
        self.__completeCv.acquire()
        self.__completeCv.wait()
        self.__completeCv.release()


