"""
  The MIT License (MIT)

  Copyright (C) 2024 Guilherme Bertoldo
  (UTFPR) Federal University of Technology - Parana

  Permission is hereby granted, free of charge, to any person obtaining a 
  copy of this software and associated documentation files (the “Software”), 
  to deal in the Software without restriction, including without limitation 
  the rights to use, copy, modify, merge, publish, distribute, sublicense, 
  and/or sell copies of the Software, and to permit persons to whom the Software 
  is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all 
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial
import serial.tools.list_ports
import threading
import queue

import wx

class FSMessageParser:
    """
    Message parser for PSerial that uses only one character as field separator FS. 
    
    Caution: the method 'parse' must return a list where the first element
    is the remainder of the input text and the second element is a list of
    messages. For instance, for the input text 'a&b&c' and the field 
    separator '&', the return must be ['c',['a','b']]. In this case, 'c' is
    not a new field because the input text may be incomplete.
    """
    def __init__(self, FS):
        self.FS = FS
    def parse(self, text):
        msglist = text.split(self.FS)
        return [msglist[-1],msglist[0:-1]]

class BracketsMessageParser:
    """
    Finds messages enclosed by brackets FSB and FSE  
    """
    def __init__(self, FSB, FSE):
      if FSB==FSE:
        raise(ValueError())
      self.FSB = FSB
      self.FSE = FSE
      return

    def parse(self, text):
      # Removing new line characters
      text = text.replace("\n","")
      text = text.replace("\r","")

      # Creating an empty message list
      msgList = []

      while True:
        # Separates the text in three parts: before the field separator, 
        # the field separator and after the field separator. Uses the end
        # field separator.
        beforeFS, fieldseparator, afterFS = text.partition(self.FSE) 
        
        # If the end field separator was found, may be the first part
        # of the text contains a message. Lets take a look...
        if fieldseparator:

          # Setting the new text to be parsed is the text after the field separator.
          text = afterFS

          try:
            # Search for the rightmost index of the begin field separator.
            # If no error occur, a message was found. Add it to the list.
            idxB = beforeFS.rindex(self.FSB)+1
            msgList.append(beforeFS[idxB:])
          except ValueError:
            pass  
        else:
          # If there is no field separator, just exit the loop
          break

      return [text,msgList]


class wxPSerial(wx.EvtHandler):
    def __init__(self, parent, notificationPeriod=300, parser=BracketsMessageParser("<",">"), port=None, baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=0.1, dsrdtr=False, inter_byte_timeout=None, exclusive=None, **kwargs):
        
        wx.EvtHandler.__init__(self)

        self.ser = PSerial(parser, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr, inter_byte_timeout, exclusive, **kwargs)

        self.parent = parent
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timer)
        self.timer.Start(milliseconds=notificationPeriod, oneShot=wx.TIMER_CONTINUOUS)
        
        # List of observers
        self.observerList = []

        # Adding parent as observer
        self.addObserver(self.parent)

        # Starting the serial communication
        self.ser.start()

    def is_open(self):
        return self.ser.is_open
    
    def timerUpdate(self, event):
        if self.ser != None:
            if self.ser.is_open:
                msgs = []
                while self.ser.hasMessage():
                    msgs.append(self.ser.getMessage())
                if len(msgs) > 0:
                    self.notify(msgs)
            else:
                pass # TODO
        event.Skip()


    def addObserver(self, observer):
        """
            Adds the observer to the list, if still not there
        """
        try:
            idx = self.observerList.index(observer)
        except:
            self.observerList.append(observer)

    def removeObserver(self, observer):
        """
            Removes the observer from the list, if it is there
        """
        try:
            self.observerList.remove(observer)
        except:
            return

    def notify(self, msgs):
        """
            Notify all observers about the news
        """
        for observer in self.observerList:
            try:
                #idx = self.observerList.index(observer)
                observer.wxPSerialUpdate(msgs)
            except:
                pass
                #self.observerList.remove(observer)

    def sendMessage(self, msg):
        self.ser.sendMessage(msg)
            


class PSerial(serial.Serial):
    """
    PSerial extends Serial providing message parsing, and unblocking serial reading via threads. 
    The input data is temporaly stored in a buffer. The buffer is parsed whenever the buffer is
    updated. The new messages are stored in a queue. Once in a while, the user must check the if
    there are messages available. The message parser must be provided during the initialization
    and may be changed during the use.
    """
    def __init__(self, parser, port=None, baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=0.1, dsrdtr=False, inter_byte_timeout=None, exclusive=None, **kwargs):
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr, inter_byte_timeout, exclusive, **kwargs)

        # Setting the input message parser
        self.parser = parser

        # Queue for the input messagens
        self.inputQueue  = queue.Queue()

        # Thread for input data. Only activated when start method is called.
        self.inputThread = None

        # Defines a buffer to store input data
        self.buffer = ""

        # Defines a tag to start/stop input thread
        self.rIsEnable = threading.Event()

        # Clearing the tag (unset)
        self.rIsEnable.clear()

    def setParser(self, parser):
        """
        Defines the message parser.
        """
        if self.rIsEnable.is_set():
            self.rIsEnable.clear()
            self.parser = parser
            self.rIsEnable.set()
        else:
            self.parser = parser
        return

    def __tRead(self):
        try:
            while self.rIsEnable.is_set():
                # Getting the incomming bytes
                inflow = self.read(self.in_waiting or 1)

                # If any byte, adds it to the buffer. Parses the buffer. If there are messages
                # add them to the input queue. 
                if inflow:
                    inflow = inflow.replace(b'\r\n', b'\n')
                    inflow = inflow.decode('UTF-8', 'replace') # replaces bad characters with replacement character (U+FFFD)
                    self.buffer = self.buffer + inflow
                    result = self.parser.parse(self.buffer)
                    self.buffer = result[0]
                    for msg in result[1]:
                        self.inputQueue.put(msg)
        except:          
            # Notify observers about the exception
            #self.notify(EventUnableToRead(self))
            
            # Stopping thread
            self.stop()
            return

    def start(self):
        """
        Starts the reading threads. Returns 1 if the thread is running. Otherwise, returns 0.
        """
        if self.inputThread is None:
            self.rIsEnable.set()
            self.inputThread = threading.Thread(target=self.__tRead, daemon=True)
            self.inputThread.start()
        else:
            return 1

        return 0
    
    def stop(self):
        """
        Stops the reading threads
        """
        self.rIsEnable.clear()

        if self.inputThread:
            self.inputThread.join()
            self.inputThread = None
        return

    def hasMessage(self):
        """
        Returns True if the input queue is not empty
        """
        return not self.inputQueue.empty()

    def getMessage(self):
        """
        Returns the message in the input queue or None
        """
        return self.inputQueue.get()

    def sendMessage(self, msg):
        """
        Sends the message msg. 
        """
        try:
            self.write(msg.encode())
        except:
            #self.notify(EventUnableToRead(self))
            self.stop()
        return


class EventUnableToWrite:
    """
    Event thrown by PSerial when unable to write the serial port. 
    """
    def __init__(self, serial: PSerial) -> None:
        self.serial = serial
        return

class EventUnableToRead:
    """
    Event thrown by PSerial when unable to read the serial port. 
    """
    def __init__(self, serial: PSerial) -> None:
        self.serial = serial
        return
