""" This is the scan procedure for collecting
observational data.  Funded via NSF #
Copyright 2009, William Griffin; written for
Brian Vaughn at Auburn University"""

__version__ = 'affectExpression_1.0; 9/09'
__author__ = 'William A Griffin'
__author_email__ = 'william.griffin@asu.edu'

import wx, os, sys, time, csv
import wx.lib.statbmp as statbmp
import  wx.lib.buttons  as  buttons
import  wx.gizmos   as  gizmos
from random import randint
from numpy import *
import time
import AffExpMaps


### for MAC
#if sys.platform == 'darwin':
   #list_dir = "/Users/observer/Documents/AffExp/lists/"
#if sys.platform == 'win32':
   #list_dir = "C://home//atwag//Dropbox//AffExp//lists"
#if sys.platform == 'linux2':
   #list_dir = "/home/atwag/Dropbox/AffExp/lists/"
if sys.platform == 'linux2':
   list_dir = "./lists/"

USE_GENERIC = 0

if USE_GENERIC:
   from wx.lib.stattext import GenStaticText as StaticText
else:
   StaticText = wx.StaticText

class AffExpFrame(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self,
                          None, -1, 'Affect Expression: Interval Data Entry',
                          size=(1100, 781)
                          )
      global maps, errorReview, coderIDlist, activityList, theclass, nearList,\
               childIDList, affectList, taskList,\
               adultList,affectIntListPos, affectIntListNeg

      errorReview = 0

      panel = wx.Panel(self, -1)

      """ Let's make it look good """
      self.SetBackgroundColour( (217, 241 , 255))

      maps = []

      #get configuration file information
      self.global_paramters = self.GetConfiguration()

      self.panel_length = 60 # should be 30 for interaction/near neighbor
      self.maxcount = 60 # should be 30 for interaction/near neighbor
      if self.global_paramters.has_key('panel_length'):
         self.panel_length = self.global_paramters['panel_length']
      if self.global_paramters.has_key('maxcount'):
         self.maxcount = self.global_paramters['maxcount']

      """ Begin data acquistion section """
      """ Mapping Buttons """
   ## Quad 1
      bmpQ11I = AffExpMaps.getbmpQ11IBitmap()
      bQ11 = buttons.GenBitmapButton(panel, -1, bmpQ11I, (0, 0))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton11, bQ11)

      bmpQ12I = AffExpMaps.getbmpQ12IBitmap()
      bQ12 = buttons.GenBitmapButton(panel, -1, bmpQ12I, (193, 0))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton12, bQ12)

      bmpQ13I = AffExpMaps.getbmpQ13IBitmap()
      bQ13 = buttons.GenBitmapButton(panel, -1, bmpQ13I, (0, 105))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton13, bQ13)

      bmpQ14I = AffExpMaps.getbmpQ14IBitmap()
      bQ14 = buttons.GenBitmapButton(panel, -1, bmpQ14I, (193, 105))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton14, bQ14)

      ## Quad 2
      bmpQ21I = AffExpMaps.getbmpQ21IBitmap()
      bQ21 = buttons.GenBitmapButton(panel, -1, bmpQ21I, (386, 0))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton21, bQ21)

      bmpQ22I = AffExpMaps.getbmpQ22IBitmap()
      bQ22 = buttons.GenBitmapButton(panel, -1, bmpQ22I, (579, 0))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton22, bQ22)

      bmpQ23I = AffExpMaps.getbmpQ23IBitmap()
      bQ23 = buttons.GenBitmapButton(panel, -1, bmpQ23I, (386, 105))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton23, bQ23)

      bmpQ24I = AffExpMaps.getbmpQ24IBitmap()
      bQ24 = buttons.GenBitmapButton(panel, -1, bmpQ24I, (579, 105))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton24, bQ24)

      ## Quad 3
      bmpQ31I = AffExpMaps.getbmpQ31IBitmap()
      bQ31 = buttons.GenBitmapButton(panel, -1, bmpQ31I, (0, 210))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton31, bQ31)

      bmpQ32I = AffExpMaps.getbmpQ32IBitmap()
      bQ32 = buttons.GenBitmapButton(panel, -1, bmpQ32I, (193, 210))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton32, bQ32)

      bmpQ33I = AffExpMaps.getbmpQ33IBitmap()
      bQ33 = buttons.GenBitmapButton(panel, -1, bmpQ33I, (0, 315))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton33, bQ33)

      ## Quad 4
      bmpQ41I = AffExpMaps.getbmpQ41IBitmap()
      bQ41 = buttons.GenBitmapButton(panel, -1, bmpQ41I, (386, 210))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton41, bQ41)

      bmpQ42I = AffExpMaps.getbmpQ42IBitmap()
      bQ42 = buttons.GenBitmapButton(panel, -1, bmpQ42I, (579, 210))
      self.Bind(wx.EVT_BUTTON, self.OnMapButton42, bQ42)

      ##__________________________________________________________

      """ Select Random Child """
      wx.StaticText(panel, -1, "Pick Child Randomly", (30,600))
      ranKid = AffExpMaps.getsmall_red_diceBitmap()
      ranKidGet = buttons.GenBitmapButton(panel, -1, ranKid,\
                                            (40, 615), style = 1)
      self.Bind(wx.EVT_BUTTON, self.OnRanButton, ranKidGet)

      """ Data Selection Section """

      self.playLocation = 101
      notice = wx.StaticText(panel, -1,
                               "Classroom: " + str(self.playLocation),
                               (850, 300)
                               )
      notice.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))

      """ Interval List  """
      eventList = []
      for x in range(0,61):
         eventList.append(str(x))
      self.labelInterv = wx.StaticText(panel, -1, "  Interval  ", (960, 150))
      self.event = wx.Choice(panel, -1, (965, 165), choices = eventList)
      self.event.SetSelection(1)

      """ Coder List  """
      coderID = []; coderIDlist = []
      coders = csv.reader(open(list_dir + 'coderList.txt'), delimiter=';')
      for each in coders:
         coderID.append(int(each[0]))
         coderIDlist.append(each[1])
      wx.StaticText(panel, -1, "Coder ID List:", (785, 150))
      self.coderID = wx.Choice(panel, -1, (790, 165), choices = coderIDlist)
      self.coderID.SetSelection(0)

      """ Child List; add new names at the end """
      child = []; childIDList = []
      children = csv.reader(open
                              (list_dir + 'room101List.txt'),
                              delimiter = ';'
                              )
      for each in children:
         child.append(int(each[0]))
         childIDList.append(each[1])
      wx.StaticText(panel, -1, "Child List:", (885, 150))
      self.child = wx.Choice(panel, -1, (890, 165), choices = childIDList)
      self.child.SetSelection(0)

      """ Activity List  """
      activityValue = [];  activityList = []
      activity = csv.reader(open
                              (list_dir + 'activityList.txt'),
                              delimiter = ';'
                              )
      for each in activity:
         activityValue.append(int(each[0]))
         activityList.append(each[1])
      wx.StaticText(panel, -1, "Activity", (785, 200))
      self.playActivity = wx.Choice(panel, -1, (790, 215), choices = activityList)
      self.playActivity.SetSelection(0)

      """ AffectIntListPositive  """
      affectIntensityPos = []; affectIntListPos = []
      affectIntPos = csv.reader(open
                                  (list_dir + "affectIntList.txt"),
                                  delimiter = ';'
                                  )
      for each in affectIntPos:
         affectIntensityPos.append(int(each[0]))
         affectIntListPos.append(each[1])
      wx.StaticText(panel, -1, "Child Affect: Positive", (210, 350))
      self.affectIntensityPos = wx.Choice(panel, -1, (225, 365),
                                            choices = affectIntListPos)
      self.affectIntensityPos.SetSelection(0)

      """ AffectIntListNegative  """
      affectIntensityNeg = []; affectIntListNeg = []
      affectIntNeg = csv.reader(open
                                  (list_dir + "affectIntList.txt"),
                                  delimiter = ';'
                                  )
      for each in affectIntNeg:
         affectIntensityNeg.append(int(each[0]))
         affectIntListNeg.append(each[1])
      wx.StaticText(panel, -1, "Child Affect: Negative", (340, 350))
      self.affectIntensityNeg = wx.Choice(panel, -1, (355, 365),
                                            choices = affectIntListNeg)
      self.affectIntensityNeg.SetSelection(0)

      """ Task List  """
      taskValue = []; taskList = []
      task = csv.reader(open
                          (list_dir + "taskList.txt"),
                          delimiter = ';'
                          )
      for each in task:
         taskValue.append(int(each[0]))
         taskList.append(each[1])

      """ Affective Tone List  """
      affectTone = []; affectList = []
      affect = csv.reader(open
                            (list_dir + "affectList.txt"),
                            delimiter = ';'
                            )
      for each in affect:
         affectTone.append(int(each[0]))
         affectList.append(each[1])

      """ Nearby List  """
      nearValue = []; nearList = []
      near = csv.reader(open
                          (list_dir + "room101List.txt"),
                          delimiter = ';'
                          )
      for each in near:
         nearValue.append(int(each[0]))
         nearList.append(each[1])

      """ Peers """
      """ Initiate 1 """
      wx.StaticText(panel, -1, "Initiate 1", (200, 410))
      self.initiate1 = wx.Choice(panel, -1, (200, 425), choices = childIDList)
      self.initiate1.SetSelection(0)
      """ Initiate 2 """
      wx.StaticText(panel, -1, "Initiate 2", (350, 410))
      self.initiate2 = wx.Choice(panel, -1, (350, 425), choices = childIDList)
      self.initiate2.SetSelection(0)
      """ Receive 1 """
      wx.StaticText(panel, -1, "Receive 1", (500, 410))
      self.receive1 = wx.Choice(panel, -1, (500, 425), choices = childIDList)
      self.receive1.SetSelection(0)
      """ Receive 2 """
      wx.StaticText(panel, -1, "Receive 2", (650, 410))
      self.receive2 = wx.Choice(panel, -1, (650, 425), choices = childIDList)
      self.receive2.SetSelection(0)
      """ Receive 3 """
      wx.StaticText(panel, -1, "Receive 3", (805, 410))
      self.receive3 = wx.Choice(panel, -1, (805, 425), choices = childIDList)
      self.receive3.SetSelection(0)

      """ Initiate Tone """
      """ Initiate 1 """
      wx.StaticText(panel, -1, "Tone", (225, 460))
      self.toneinitiate1 = wx.Choice(panel, -1, (200, 475), choices = affectList)
      self.toneinitiate1.SetSelection(0)
      """ Initiate 2 """
      wx.StaticText(panel, -1, "Tone", (375, 460))
      self.toneinitiate2 = wx.Choice(panel, -1, (350, 475), choices = affectList)
      self.toneinitiate2.SetSelection(0)
      """ Receive 1 """
      wx.StaticText(panel, -1, "Tone", (525, 460))
      self.tonereceive1 = wx.Choice(panel, -1, (500, 475), choices = affectList)
      self.tonereceive1.SetSelection(0)
      """ Receive 2 """
      wx.StaticText(panel, -1, "Tone", (675, 460))
      self.tonereceive2 = wx.Choice(panel, -1, (650, 475), choices = affectList)
      self.tonereceive2.SetSelection(0)
      """ Receive 3 """
      wx.StaticText(panel, -1, "Tone", (830, 460))
      self.tonereceive3 = wx.Choice(panel, -1, (805, 475), choices = affectList)
      self.tonereceive3.SetSelection(0)

      """ Category  """
      """ Category Initiate 1 """
      wx.StaticText(panel, -1, "Category", (200, 510))
      self.categoryinitiate1 = wx.Choice(panel, -1, (188, 525), choices = taskList)
      self.categoryinitiate1.SetSelection(0)
      """ Category Initiate 2 """
      wx.StaticText(panel, -1, "Category", (352, 510))
      self.categoryinitiate2 = wx.Choice(panel, -1, (340, 525), choices = taskList)
      self.categoryinitiate2.SetSelection(0)
      """ Category Receive 1 """
      wx.StaticText(panel, -1, "Category", (504, 510))
      self.categoryreceive1 = wx.Choice(panel, -1, (492, 525), choices = taskList)
      self.categoryreceive1.SetSelection(0)
      """ Category Receive 2 """
      wx.StaticText(panel, -1, "Category", (656, 510))
      self.categoryreceive2 = wx.Choice(panel, -1, (644, 525), choices = taskList)
      self.categoryreceive2.SetSelection(0)
      """ Category Receive 3 """
      wx.StaticText(panel, -1, "Category", (808, 510))
      self.categoryreceive3 = wx.Choice(panel, -1, (796, 525), choices = taskList)
      self.categoryreceive3.SetSelection(0)

      """ Near Persons  """
      """ Near Persons 1 """
      wx.StaticText(panel, -1, "Nearby", (200, 560))
      self.Nearbyinitiate1 = wx.Choice(panel, -1, (188, 575), choices = nearList)
      self.Nearbyinitiate1.SetSelection(0)
      """ Near Persons 2 """
      wx.StaticText(panel, -1, "Nearby", (352, 560))
      self.Nearbyinitiate2 = wx.Choice(panel, -1, (340, 575), choices = nearList)
      self.Nearbyinitiate2.SetSelection(0)
      """ Near Persons 3 """
      wx.StaticText(panel, -1, "Nearby", (504, 560))
      self.Nearbyreceive1 = wx.Choice(panel, -1, (492, 575), choices = nearList)
      self.Nearbyreceive1.SetSelection(0)
      """ Near Persons 4 """
      wx.StaticText(panel, -1, "Nearby", (656, 560))
      self.Nearbyreceive2 = wx.Choice(panel, -1, (644, 575), choices = nearList)
      self.Nearbyreceive2.SetSelection(0)
      """ Near Persons 5 """
      wx.StaticText(panel, -1, "Nearby", (808, 560))
      self.Nearbyreceive3 = wx.Choice(panel, -1, (796, 575), choices = nearList)
      self.Nearbyreceive3.SetSelection(0)

      """ Manipulate Data and Store: Buttons """

      errCheck = wx.Button(panel, -1, "Error Check", (830, 3))
      errCheck.SetDefault()
      self.Bind(wx.EVT_BUTTON, self.OnErrorCheck, errCheck)     # Uses OnErrorCheck
      errCheck.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      errCheck.SetToolTipString("Error Check")
      errCheck.SetSize(errCheck.GetBestSize())

      done = wx.Button(panel, -1, "Submit Data", (830, 53))
      self.Bind(wx.EVT_BUTTON, self.OnComplete, done)     # Uses OnComplete
      done.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      done.SetToolTipString("Compile event data")
      done.SetSize(done.GetBestSize())

      ano = wx.Button(panel, -1, "Another Interval", (810, 106))
      self.Bind(wx.EVT_BUTTON, self.OnAnother, ano)       #Uses OnAnother
      ano.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      ano.SetToolTipString("Refresh entry values")
      ano.SetSize(ano.GetBestSize())

      q = wx.Button(panel, -1, "Quit", (975, 650))
      self.Bind(wx.EVT_BUTTON, self.OnClose, q)           #Uses OnClose
      q.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))
      q.SetToolTipString("This exits the program...")
      q.SetSize(q.GetBestSize())

   ############ gauge #######################
      self.count = 0
      wx.StaticText(panel, -1, "Seconds", (5, 535))
      self.buttonG = wx.Button(panel, -1, "Press to start timer", (25, 550))
      self.buttonG.Bind(wx.EVT_BUTTON, self.buttonGClick)
      self.gauge1 = wx.Gauge(panel, -1, self.panel_length, (5, 500), (165, 35))
      self.gauge1.SetValue(0)
      self.gauge1.SetBezelFace(3)
      self.gauge1.SetShadowWidth(3)
      self.Bind(wx.EVT_TIMER, self.OnTimer)
      self.timerG = wx.Timer(self, -1)
      self.timerG.Start(1000)

   ############### clock ######################

      self.led = gizmos.LEDNumberCtrl(panel, -1, (5,460), (165, 35),
                                        gizmos.LED_ALIGN_CENTER)
      self.led.SetBackgroundColour("red")
      self.red_flag = True
      self.led.SetForegroundColour("black")
      self.OnTimer(None)
      self.timer = wx.Timer(self, -1)
      # update clock digits every second (1000ms)
      self.timer.Start(1000)
      self.Bind(wx.EVT_TIMER, self.OnTimer)

   ############ config file #######################
   def GetConfiguration(self):
      tmpDict = {}
      f = open('config.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip()
         if len(line)> 0:
            if line[0] != '#':
               tmps = line.split('=')
               para_name = tmps[0].strip()
               para_value = float(tmps[1].strip())
               tmpDict[para_name] = para_value
         line = f.readline()
      f.close()
      return tmpDict
   ############ gauge #######################

   def buttonGClick(self, event):
      self.gauge1.SetValue(0)
      self.count = 0
      self.Bind(wx.EVT_TIMER, self.OnTimer)

   ###################################################################

   def OnTimer(self, event):
      ## clock
      # get current time from computer
      current = time.localtime(time.time())
      # time string can have characters 0..9, -, period, or space
      ts = time.strftime("%H %M %S", current)
      self.led.SetValue(ts)
      ##guage
      self.count = self.count + 1
      if self.count >= self.maxcount:
         self.count = 0

      self.gauge1.SetValue(self.count)

#######################################################################
   def OnClose(self, event):
      self.Destroy()

   def OnErrorCheck(self, evt):
      """ data entries; 'None' added to begin with 1 - easier for counting """
      global errorReview
      # use these taskList numbers to construct error rules for taskList
               # None
               #1. Breakfast
               #2. Lunch
               #3. Snack
               #4. Free Choice
               #5. Large Grp (Teacher focus)
               #6. Small Grp (Teacher led )
               #7. Playgrp Free Choice
               #8. Playgrp Group Activity
               #9. Transition
               #10. CRoom Music
               #11. CRoom Movement/Dance
               #12. CRoom Indoor Playgrd
               #13. Nap
               #14. Child Request
               #15. Child Assist/Help Peer
               #16. Other

      retrieveDataEntries = \
           ['None',
                             self.event.GetSelection(),             #1
                             self.coderID.GetSelection(),           #2
                             self.child.GetSelection(),             #3
                             self.playActivity.GetSelection(),      #4
                             self.playLocation,                     #5
                             self.affectIntensityPos.GetSelection(),#6
                             self.affectIntensityNeg.GetSelection(),#7
                             self.initiate1.GetSelection(),         #8
                             self.initiate2.GetSelection(),         #9
                             self.receive1.GetSelection(),          #10
                             self.receive2.GetSelection(),          #11
                             self.receive3.GetSelection(),          #12
                             self.toneinitiate1.GetSelection(),     #13
                             self.toneinitiate2.GetSelection(),     #14
                             self.tonereceive1.GetSelection(),      #15
                             self.tonereceive2.GetSelection(),      #16
                             self.tonereceive3.GetSelection(),      #17
                             self.categoryinitiate1.GetSelection(), #18
                             self.categoryinitiate2.GetSelection(), #19
                             self.categoryreceive1.GetSelection(),  #20
                             self.categoryreceive2.GetSelection(),  #21
                             self.categoryreceive3.GetSelection(),  #22
                             self.Nearbyinitiate1.GetSelection(),   #23
                             self.Nearbyinitiate2.GetSelection(),   #24
                             self.Nearbyreceive1.GetSelection(),    #25
                             self.Nearbyreceive2.GetSelection(),    #26
                             self.Nearbyreceive3.GetSelection()]    #27

      """ Review for errors before sending """
      """for i,v in enumerate(retrieveDataEntries):  #use listingIndex.py to create
            #print i,v"""

      ############## Error Checking  ##############################
      #############################################################

      """ Coder ID Data Error """
      if retrieveDataEntries[2] == 0:
         coderIDMessage = wx.MessageBox(
               'No CoderID Assigned',
                caption = 'CoderID Needed:',
                style = wx.OK, parent = self
            )

      """ Child ID Data Error """
      childN = len(childIDList)
      if retrieveDataEntries[3] < 1 or retrieveDataEntries[3] == childN - 1:
         childMessage = wx.MessageBox(
               'No Child Assigned',
                caption = 'Child Needed:',
                style = wx.OK, parent = self
            )

      """ Child Available Error """
      if retrieveDataEntries[4] == 0:
         childMessage = wx.MessageBox(
               'No Child Activity Assigned',
                caption = 'Child Activity Needed:',
                style = wx.OK, parent = self
            )

      """ Child Classroom Error """
      if retrieveDataEntries[5] == 0:
         childMessage = wx.MessageBox(
               'No Classroom Assigned',
                caption = 'Classroom Needed:',
                style = wx.OK, parent = self
            )
         errorReview = 1
      else:
         if retrieveDataEntries[6] > 0: # == 1: Affect Intensity not 0
            """ Map Assigment Complete Error """
            if len(maps) != 2:
               mapper = str(maps)
               mapInfodlg = wx.MessageBox(
                       mapper,
                        caption = 'Error.  Re-Enter Map Assignment.',
                        style = wx.OK, parent = self
                    )
               for eachItem in range(len(maps)):
                  maps.pop()

            #######################################################################

            p1,p2,p3,p4,p5 = retrieveDataEntries[8],retrieveDataEntries[9],\
                   retrieveDataEntries[10],retrieveDataEntries[11],retrieveDataEntries[12]

            tp1,tp2,tp3,tp4,tp5 = retrieveDataEntries[13],retrieveDataEntries[14],\
                   retrieveDataEntries[15],retrieveDataEntries[16],retrieveDataEntries[17]

            cp11,cp12,cp13,cp14,cp15 = retrieveDataEntries[18],retrieveDataEntries[19],\
                   retrieveDataEntries[20],retrieveDataEntries[21],retrieveDataEntries[22]

            # Entry errors for peer
            initiate = retrieveDataEntries[8]
            pentries = [initiate,p2,p3,p4,p5]

            # Initiate in multiple Initiate slots
            multiEntries =[]
            for entry in range(len(pentries)):
               if pentries[entry] != 0:
                  if pentries.count(pentries[entry]) > 1:
                     multiEntries.append(pentries.count(pentries[entry]))
            if len(multiEntries) > 0:
               subjectListedTwiceMessage = wx.MessageBox(
                       'Initiate Listed - Multiple',
                        caption = 'Double Listing Of Child: ',
                        style = wx.OK, parent = self
                    )
               multiEntries =[]
            #######################################################################
            # target in Initiate slots
            target = retrieveDataEntries[3]
            tentries = [p1,p2,p3,p4,p5]

            for each in range(len(tentries)):
               if tentries[each] == target:
                  subjectListedTwiceMessage = wx.MessageBox(
                           'Target Listed - Multiple',
                            caption = 'Double Listing Of Target: ',
                            style = wx.OK, parent = self
                        )
            #######################################################################

         errorReview = 1

      return errorReview
   ### needed to clean up the 'no entry' for nearby
   def nearbyInitiate1(self):
      if self.Nearbyinitiate1.GetSelection() == 0:
         return self.Nearbyinitiate1.GetSelection()
      else:
         return nearList[self.Nearbyinitiate1.GetSelection()]

   def nearbyInitiate2(self):
      if self.Nearbyinitiate2.GetSelection() == 0:
         return self.Nearbyinitiate2.GetSelection()
      else:
         return nearList[self.Nearbyinitiate2.GetSelection()]

   def nearbyReceive1(self):
      if self.Nearbyreceive1.GetSelection() == 0:
         return self.Nearbyreceive1.GetSelection()
      else:
         return nearList[self.Nearbyreceive1.GetSelection()]

   def nearbyReceive2(self):
      if self.Nearbyreceive2.GetSelection() == 0:
         return self.Nearbyreceive2.GetSelection()
      else:
         return nearList[self.Nearbyreceive2.GetSelection()]

   def nearbyReceive3(self):
      if self.Nearbyreceive3.GetSelection() == 0:
         return self.Nearbyreceive3.GetSelection()
      else:
         return nearList[self.Nearbyreceive3.GetSelection()]

   def OnComplete(self, evt):
      """ Collect data; post to dialog - approve and send """
      global errorReview
      eventVector = []
      if errorReview != 1:
         dataSubdlg = wx.MessageBox('Please Submit Error Checking',
                                       caption = 'Error Status',
                                       style = wx.OK, parent = self
                                       )
      else:
         retrieveDataEntries = [self.event.GetSelection(),

                                   self.coderID.GetSelection(),
                                   coderIDlist[self.coderID.GetSelection()],

                                   self.child.GetSelection(),
                                   childIDList[self.child.GetSelection()],

                                   self.playActivity.GetSelection(),
                                   activityList[self.playActivity.GetSelection()],

                                   self.playLocation,

                                   self.affectIntensityPos.GetSelection(),
                                   affectIntListPos[self.affectIntensityPos.GetSelection()],

                                   self.affectIntensityNeg.GetSelection(),
                                   affectIntListNeg[self.affectIntensityNeg.GetSelection()],

                                   self.initiate1.GetSelection(),
                                   childIDList[self.initiate1.GetSelection()],

                                   self.initiate2.GetSelection(),
                                   childIDList[self.initiate2.GetSelection()],

                                   self.receive1.GetSelection(),
                                   childIDList[self.receive1.GetSelection()],

                                   self.receive2.GetSelection(),
                                   childIDList[self.receive2.GetSelection()],

                                   self.receive3.GetSelection(),
                                   childIDList[self.receive3.GetSelection()],

                                   self.toneinitiate1.GetSelection(),
                                   affectList[self.toneinitiate1.GetSelection()],

                                   self.toneinitiate2.GetSelection(),
                                   affectList[self.toneinitiate2.GetSelection()],

                                   self.tonereceive1.GetSelection(),
                                   affectList[self.tonereceive1.GetSelection()],

                                   self.tonereceive2.GetSelection(),
                                   affectList[self.tonereceive2.GetSelection()],

                                   self.tonereceive3.GetSelection(),
                                   affectList[self.tonereceive3.GetSelection()],

                                   self.categoryinitiate1.GetSelection(),
                                   taskList[self.categoryinitiate1.GetSelection()],

                                   self.categoryinitiate2.GetSelection(),
                                   taskList[self.categoryinitiate2.GetSelection()],

                                   self.categoryreceive1.GetSelection(),
                                   taskList[self.categoryreceive1.GetSelection()],

                                   self.categoryreceive2.GetSelection(),
                                   taskList[self.categoryreceive2.GetSelection()],

                                   self.categoryreceive3.GetSelection(),
                                   taskList[self.categoryreceive3.GetSelection()],

                                   self.Nearbyinitiate1.GetSelection(),
                                   self.nearbyInitiate1(),

                                   self.Nearbyinitiate2.GetSelection(),
                                   self.nearbyInitiate2(),

                                   self.Nearbyreceive1.GetSelection(),
                                   self.nearbyReceive1(),

                                   self.Nearbyreceive2.GetSelection(),
                                   self.nearbyReceive2(),

                                   self.Nearbyreceive3.GetSelection(),
                                   self.nearbyReceive3()]

         """ Pull data sources together """

         eventVector.extend(time.localtime())
         eventVector.extend(retrieveDataEntries)
         eventVector.extend(maps)

         """ Send to File """
         ### use regular expression here to export without braces and brackets
         outputTxt = 'AffectExpressOut.txt'
         if sys.platform == 'darwin':
            os.chdir("/Users/observer/Documents/AffExp/data/")
         if sys.platform == 'win32':
            os.chdir("C:\\AffExp\\data\\")
         txtout = open(outputTxt,'a')
         voutInitial = eventVector
         vout = str(voutInitial[:]).strip('[]').replace(')', '').\
               replace('(', '').replace('True','1').\
                 replace('False','0')
         txtout.write(str(vout))
         txtout.write('\n')
         txtout.close
         """ To Excel """
         outputTxt = 'AffectExpressOut.csv'
         if sys.platform == 'darwin':
            os.chdir("/Users/observer/Documents/AffExp/data/")
         if sys.platform == 'win32':
            os.chdir("C:\\AffExp\\data\\")
         txtout = open(outputTxt,'a')
         txtout.write(str(vout))
         txtout.write('\n')
         txtout.close
         for eachItem in range(len(maps)):
            maps.pop()

         dataSubdlg = wx.MessageBox('Data Successfully Submitted',
                                       caption = 'Data Status',
                                       style = wx.OK, parent = self
                                       )

         """ reset errorCount for next observation """
         errorReview = 0
         return errorReview

   def OnAnother(self, evt):
      """ Refresh all entries; increment event number and keep coder ID the same """
      nxtEvent = self.event.GetSelection()+1
      dataEntries = [self.event.ClearBackground(),
                       self.event.Refresh(),
                       self.event.SetSelection(nxtEvent),

                       self.coderID.ClearBackground(),
                       self.coderID.Refresh(),
                       self.child.ClearBackground,
                       self.child.Refresh(),

                       self.playActivity.ClearBackground(),
                       self.playActivity.Refresh(),
                       self.playActivity.SetSelection(0),
                       self.playActivity.SetFocus(),

                       self.affectIntensityPos.ClearBackground(),
                       self.affectIntensityPos.Refresh(),
                       self.affectIntensityPos.SetSelection(0),

                       self.affectIntensityNeg.ClearBackground(),
                       self.affectIntensityNeg.Refresh(),
                       self.affectIntensityNeg.SetSelection(0),

                       self.initiate1.ClearBackground(),
                       self.initiate1.Refresh(),
                       self.initiate1.SetSelection(0),

                       self.initiate2.ClearBackground(),
                       self.initiate2.Refresh(),
                       self.initiate2.SetSelection(0),

                       self.receive1.ClearBackground(),
                       self.receive1.Refresh(),
                       self.receive1.SetSelection(0),

                       self.receive2.ClearBackground(),
                       self.receive2.Refresh(),
                       self.receive2.SetSelection(0),

                       self.receive3.ClearBackground(),
                       self.receive3.Refresh(),
                       self.receive3.SetSelection(0),

                       self.toneinitiate1.ClearBackground(),
                       self.toneinitiate1.Refresh(),
                       self.toneinitiate1.SetSelection(0),

                       self.toneinitiate2.ClearBackground(),
                       self.toneinitiate2.Refresh(),
                       self.toneinitiate2.SetSelection(0),

                       self.tonereceive1.ClearBackground(),
                       self.tonereceive1.Refresh(),
                       self.tonereceive1.SetSelection(0),

                       self.tonereceive2.ClearBackground(),
                       self.tonereceive2.Refresh(),
                       self.tonereceive2.SetSelection(0),

                       self.tonereceive3.ClearBackground(),
                       self.tonereceive3.Refresh(),
                       self.tonereceive3.SetSelection(0),

                       self.categoryinitiate1.ClearBackground(),
                       self.categoryinitiate1.Refresh(),
                       self.categoryinitiate1.SetSelection(0),

                       self.categoryinitiate2.ClearBackground(),
                       self.categoryinitiate2.Refresh(),
                       self.categoryinitiate2.SetSelection(0),

                       self.categoryreceive1.ClearBackground(),
                       self.categoryreceive1.Refresh(),
                       self.categoryreceive1.SetSelection(0),

                       self.categoryreceive2.ClearBackground(),
                       self.categoryreceive2.Refresh(),
                       self.categoryreceive2.SetSelection(0),

                       self.categoryreceive3.ClearBackground(),
                       self.categoryreceive3.Refresh(),
                       self.categoryreceive3.SetSelection(0),

                       self.Nearbyinitiate1.ClearBackground(),
                       self.Nearbyinitiate1.Refresh(),
                       self.Nearbyinitiate1.SetSelection(0),

                       self.Nearbyinitiate2.ClearBackground(),
                       self.Nearbyinitiate2.Refresh(),
                       self.Nearbyinitiate2.SetSelection(0),

                       self.Nearbyreceive1.ClearBackground(),
                       self.Nearbyreceive1.Refresh(),
                       self.Nearbyreceive1.SetSelection(0),

                       self.Nearbyreceive2.ClearBackground(),
                       self.Nearbyreceive2.Refresh(),
                       self.Nearbyreceive2.SetSelection(0),

                       self.Nearbyreceive3.ClearBackground(),
                       self.Nearbyreceive3.Refresh(),
                       self.Nearbyreceive3.SetSelection(0)]

      for each in range(len(dataEntries)):
         dataEntries[each]
      for eachItem in range(len(maps)):
         maps.pop()

   def OnRanButton(self, evt):
      """ Allow a child to be randomly selected """
      childRandomPull = randint(1,(len(childIDList)-1))
      ranChild = childIDList[childRandomPull]
      dlg = wx.MessageDialog(self,
                               ranChild,'Observe This Child:',wx.OK
                               )
      dlg.ShowModal()
      dlg.Destroy()

      """ GIS Mapping """
   def OnMapButton11(self, evt):
      win = MyMapFrame11()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton12(self, evt):
      win = MyMapFrame12()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton13(self, evt):
      win = MyMapFrame13()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton14(self, evt):
      win = MyMapFrame14()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
      #------------------------------
   def OnMapButton21(self, evt):
      win = MyMapFrame21()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton22(self, evt):
      win = MyMapFrame22()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton23(self, evt):
      win = MyMapFrame23()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton24(self, evt):
      win = MyMapFrame24()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
      #------------------------------
   def OnMapButton31(self, evt):
      win = MyMapFrame31()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton32(self, evt):
      win = MyMapFrame32()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton33(self, evt):
      win = MyMapFrame33()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
      #------------------------------
   def OnMapButton41(self, evt):
      win = MyMapFrame41()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   def OnMapButton42(self, evt):
      win = MyMapFrame42()
      win.SetSize((800, 600))
      win.CenterOnParent(wx.BOTH)
      win.Show(True)
   ##############################

class MyMapFrame11(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #1:1')
      bmp11 = AffExpMaps.getbmp11Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp11)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(11)
      maps.append(event.GetPosition().Get())
      map1Infodlg = wx.MessageBox(
           'Location Recorded', \
            caption = 'Data Status for Quad1subQuad 1 Map', \
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame12(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #1:2')
      bmp12 = AffExpMaps.getbmp12Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp12)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(12)
      maps.append(event.GetPosition().Get())
      map2Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad1subQuad 2 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame13(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #1:3')
      bmp13 = AffExpMaps.getbmp13Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp13)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(13)
      maps.append(event.GetPosition().Get())
      map3Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad1subQuad 3 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame14(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #1:4')
      bmp14 = AffExpMaps.getbmp14Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp14)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(14)
      maps.append(event.GetPosition().Get())
      map4Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad1subQuad 4 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()
#_________________________________________________________________________
class MyMapFrame21(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #2:1')
      bmp21 = AffExpMaps.getbmp21Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp21)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(21)
      maps.append(event.GetPosition().Get())
      map1Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad2subQuad 1 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame22(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #2:2')
      bmp22 = AffExpMaps.getbmp22Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp22)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(22)
      maps.append(event.GetPosition().Get())
      map2Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad2subQuad 2 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame23(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #2:3')
      bmp23 = AffExpMaps.getbmp23Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp23)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(23)
      maps.append(event.GetPosition().Get())
      map3Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad2subQuad 3 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame24(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #2:4')
      bmp24 = AffExpMaps.getbmp24Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp24)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(24)
      maps.append(event.GetPosition().Get())
      map4Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad2subQuad 4 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()
#________________________________________________________________________
class MyMapFrame31(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #3:1')
      bmp31 = AffExpMaps.getbmp31Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp31)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(31)
      maps.append(event.GetPosition().Get())
      map1Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad3subQuad 1 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame32(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #3:2')
      bmp32 = AffExpMaps.getbmp32Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp32)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(32)
      maps.append(event.GetPosition().Get())
      map2Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad3subQuad 2 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame33(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #3:3')
      bmp33 = AffExpMaps.getbmp33Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp33)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(33)
      maps.append(event.GetPosition().Get())
      map3Infodlg = wx.MessageBox(
           'Data Recorded',
            caption = 'Data Status for Quad3subQuad 3 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()
#___________________________________________________________________
class MyMapFrame41(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #4:1')
      bmp41 = AffExpMaps.getbmp41Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp41)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(41)
      maps.append(event.GetPosition().Get())
      map1Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad4subQuad 1 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()

class MyMapFrame42(wx.Frame):
   def __init__(self):
      wx.Frame.__init__(self, None, -1, 'Quad #4:2')
      bmp42 = AffExpMaps.getbmp42Bitmap()
      self.Image = statbmp.GenStaticBitmap(self, -1, bmp42)
      self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
      S = wx.BoxSizer(wx.VERTICAL)
      S.Add(self.Image, 0)
      self.SetSizerAndFit(S)

   def OnClick(self, event):
      maps.append(42)
      maps.append(event.GetPosition().Get())
      map2Infodlg = wx.MessageBox(
           'Location Recorded',
            caption = 'Data Status for Quad4subQuad 2 Map',
            style = wx.OK, parent = self
        )
      self.Destroy()


if __name__ == '__main__':
   app = wx.App(False)
   AffExpFrame().Show()
   app.MainLoop()