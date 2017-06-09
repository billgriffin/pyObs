""" This is the visual attention scan for collecting
observational data.  Funded via NSF #
Copyright 2010, Xun Li; William Griffin; written for
Brian Vaughn at Auburn University"""

__version__ = 'visualattention_2.0; 8/10'
__author__ = 'William A Griffin; Xun Li'
__author_email__ = 'william.griffin@asu.edu'


import wx
import  wx.gizmos   as  gizmos
import  wx.lib.buttons  as  buttons
import time,copy,os, sys
from datetime import datetime, timedelta, date
from random import randint
import bitRedDice

#### System Selection
#if sys.platform == 'darwin':
   #list_dir = "./lists/"
#if sys.platform == 'win32':
   #list_dir = ".//lists"
#if sys.platform == 'linux2':
   #list_dir = "./lists/"


class VARecord():
   def __init__(self):
      self.classId = ''
      self.childId = ''
      self.targetId1 = '?'
      self.targetId2 = ''
      self.targetId3 = ''
      self.targetId4 = ''
      self.VR_1 = '0' #0-2
      self.affect_1 = '0' # 0-4
      self.VR_2 = '0' #0-2
      self.affect_2 = '0' # 0-4
      self.VR_3 = '0' #0-2
      self.affect_3 = '0' # 0-4
      self.VR_4 = '0' #0-2
      self.affect_4 = '0' # 0-4

class VAFrame(wx.Frame):
   def __init__(self, *args, **kwds):
      if len(args) == 0:
         dlg = wx.MessageDialog(self, 'Parameters setting error','Error',wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return False

      self.recordFileName = args[0][0] #args[0][3]

      # global variables
      self.global_paramters = self.GetConfiguration()
      self.siteList = self.GetSiteList()
      self.kidList, self.presentList = self.GetKidList()
      self.adultList = self.GetAdultList()
      self.observerList = self.GetObserverList()
      self.classList = self.GetClassList()
      self.activityList = self.GetActivityList()

      self.new_round_at_new_day = 1 # default = true
      self.timer_interval = 6 # default = 6
      self.max_observation_per_round = 200 # default = 200
      if self.global_paramters.has_key('new_round_at_new_day'):
         self.new_round_at_new_day = self.global_paramters['new_round_at_new_day']
      if self.global_paramters.has_key('timer_interval'):
         self.timer_interval = self.global_paramters['timer_interval']
      if self.global_paramters.has_key('max_observation_per_round'):
         self.max_observation_per_round = self.global_paramters['max_observation_per_round']

      # local variables
      self.rndKidList = self.kidList[:]
      self.rndKidList.insert(0,'Random Select Child')
      self.vaKidList = self.kidList + self.adultList
      self.vaKidList.insert(0,'')
      self.vaKidList.insert(1,'?')
      self.record = None
      self.currentClassroom  = ''
      self.currentObserver = ''
      self.currentGauge = 1
      self.currentObserver = ''
      self.observerDict = self.GetRoundInfo()

      # GUI
      kwds["style"] = wx.DEFAULT_FRAME_STYLE
      wx.Frame.__init__(self, None, -1, **kwds)
      self.CreateStatusBar()

      panel = wx.Panel(self, -1)
      self.SetBackgroundColour( (217, 241 , 255))

      self.label_31 = wx.StaticText(panel, -1, "Current observation #:")
      self.observation_spin= wx.SpinCtrl(panel, -1, "")

      self.label_20 = wx.StaticText(panel, -1, "Data:")
      self.label_21 = wx.StaticText(panel, -1, "")
      self.label_22 = wx.StaticText(panel, -1, "Observer:")
      self.combo_box_ObserverList = wx.ComboBox(panel, -1, choices=self.observerList, style=wx.CB_DROPDOWN)
      self.label_23 = wx.StaticText(panel, -1, "Class:")
      self.combo_box_ClassList = wx.ComboBox(panel, -1, choices=self.classList, style=wx.CB_DROPDOWN)
      self.label_24 = wx.StaticText(panel, -1, "Round#(today):")
      self.round_spin = wx.SpinCtrl(panel, -1, "")

      self.label_26 = wx.StaticText(panel, -1, "# Children present:")
      numOfChild = [str(i) for i in range(1,len(self.kidList))]
      numOfChild.insert(0,'')
      self.combo_box_ChildrenPresent = wx.ComboBox(panel, -1, choices=numOfChild, style=wx.CB_DROPDOWN)
      self.label_28 = wx.StaticText(panel, -1, "Site:")
      self.combo_box_SiteList = wx.ComboBox(panel, -1, choices=self.siteList, style=wx.CB_DROPDOWN)
      self.label_29 = wx.StaticText(panel, -1, "Activity setting:")
      self.combo_box_ActivityList = wx.ComboBox(panel, -1, choices=self.activityList, style=wx.CB_DROPDOWN)


      self.button_randSelKid = buttons.GenBitmapButton(panel, -1, bitRedDice.getsmall_red_diceBitmap(), style = 1)
      self.combo_box_RndChildList = wx.ComboBox(panel, -1,choices=self.rndKidList, style=wx.CB_DROPDOWN)
      self.child_present_checkbox = wx.CheckBox(panel, -1, "(not present)")
      self.button_StartRecord = wx.Button(panel, -1, "Start Recording")
      self.button_SaveRecord = wx.Button(panel, -1, "Save Record")
      self.button_DiscardRecord = wx.Button(panel, -1, "Discard Record")
      self.gauge_Timer = wx.Gauge(panel, -1, size=(100, 30))
      self.gauge_Timer1 = wx.Gauge(panel, -1, size=(100, 30))
      self.label_6 = wx.StaticText(panel, -1, "VR Code:")
      self.radio_box_VR_1 = wx.RadioBox(panel, -1, "", choices=["N/A", "Glance", "Look"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_VR_2 = wx.RadioBox(panel, -1, "", choices=["N/A", "Glance", "Look"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_VR_3 = wx.RadioBox(panel, -1, "", choices=["N/A", "Glance", "Look"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_VR_4 = wx.RadioBox(panel, -1, "", choices=["N/A", "Glance", "Look"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.label_1 = wx.StaticText(panel, -1, "Visual Attention To:")
      self.label_2 = wx.StaticText(panel, -1, "Visual Target 1:")
      self.combo_box_TargetChildList1 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
      self.label_3 = wx.StaticText(panel, -1, "Visual Target 2:")
      self.combo_box_TargetChildList2 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
      self.label_4 = wx.StaticText(panel, -1, "Visual Target 3:")
      self.combo_box_TargetChildList3 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
      self.label_5 = wx.StaticText(panel, -1, "Visual Target 4:")
      self.combo_box_TargetChildList4 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
      self.label_7 = wx.StaticText(panel, -1, "Affect:")
      self.radio_box_Affect_1 = wx.RadioBox(panel, -1, "", choices=["N/A","Positive", "Neutral", "Negtive"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_Affect_2 = wx.RadioBox(panel, -1, "", choices=["N/A","Positive", "Neutral", "Negtive"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_Affect_3 = wx.RadioBox(panel, -1, "", choices=["N/A","Positive", "Neutral", "Negtive"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.radio_box_Affect_4 = wx.RadioBox(panel, -1, "", choices=["N/A","Positive", "Neutral", "Negtive"], majorDimension=0, style=wx.RA_SPECIFY_COLS)
      self.label_8 = wx.StaticText(panel, -1, "%s seconds timer:"%self.timer_interval)
      self.label_9 = wx.StaticText(panel, -1, """
Note: You are to observe the target child for a period 6-sec.\
Note the identifier of EACH person (peer or adult) to whom the observed child directs visual regard.\
Units of VR are coded as "G" if the child looks briefly (<2-sec) at a peer or adult and coded as "L"" \
if the child looks for a longer (>2-sec).""")

      self.led = gizmos.LEDNumberCtrl(panel, -1)
      self.__set_properties()

      self.Bind(wx.EVT_CHECKBOX, self.ChildPresentCheck, self.child_present_checkbox)
      self.Bind(wx.EVT_SPINCTRL, self.OnRoundSpin, self.round_spin)
      self.Bind(wx.EVT_BUTTON, self.RandomSelectChild, self.button_randSelKid)
      self.Bind(wx.EVT_COMBOBOX, self.RandomChildSelected, self.combo_box_RndChildList)
      self.Bind(wx.EVT_BUTTON, self.StartRecord, self.button_StartRecord)
      self.Bind(wx.EVT_BUTTON, self.SaveRecord, self.button_SaveRecord)
      self.Bind(wx.EVT_BUTTON, self.DiscardRecord, self.button_DiscardRecord)
      self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget1, self.combo_box_TargetChildList1)
      self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget2, self.combo_box_TargetChildList2)
      self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget3, self.combo_box_TargetChildList3)
      self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget4, self.combo_box_TargetChildList4)
      self.Bind(wx.EVT_RADIOBOX, self.SelectVR_1, self.radio_box_VR_1)
      self.Bind(wx.EVT_RADIOBOX, self.SelectVR_2, self.radio_box_VR_2)
      self.Bind(wx.EVT_RADIOBOX, self.SelectVR_3, self.radio_box_VR_3)
      self.Bind(wx.EVT_RADIOBOX, self.SelectVR_4, self.radio_box_VR_4)
      self.Bind(wx.EVT_RADIOBOX, self.SelectAffect_1, self.radio_box_Affect_1)
      self.Bind(wx.EVT_RADIOBOX, self.SelectAffect_2, self.radio_box_Affect_2)
      self.Bind(wx.EVT_RADIOBOX, self.SelectAffect_3, self.radio_box_Affect_3)
      self.Bind(wx.EVT_RADIOBOX, self.SelectAffect_4, self.radio_box_Affect_4)
      self.Bind(wx.EVT_COMBOBOX, self.ObserverSelected, self.combo_box_ObserverList)
      self.Bind(wx.EVT_COMBOBOX, self.ClassroomSelected, self.combo_box_ClassList)
      id1 = wx.NewId()
      wx.RegisterId(id1)
      self.timer = wx.Timer(self, id1)
      self.Bind(wx.EVT_TIMER, self.OnTimer,self.timer,id1)
      id2 = wx.NewId()
      wx.RegisterId(id2)
      self.statusTimer = wx.Timer(self,id2)
      self.Bind(wx.EVT_TIMER, self.OnStatusTimer,self.statusTimer,id2)

      self.count = 0
      self.statusTimer.Start(1000)
      self.OnStatusTimer(None)

   def __set_properties(self):
      self.SetTitle("Visual Attention")
      self.SetSize((800, 700))
      self.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

      ## Data: 08/09/10
      self.label_20.SetPosition((10,14))
      self.label_21.SetPosition((70,14))

      ## Observer: combobox
      self.label_22.SetPosition((180,14))
      self.combo_box_ObserverList.SetSize((140,25))
      self.combo_box_ObserverList.SetPosition((280,8))

      ## Class: Combobox
      self.label_23.SetPosition((10, 44))
      self.combo_box_ClassList.SetSize((80,25))
      self.combo_box_ClassList.SetPosition((70, 40))

      ## Round: ComboBOx
      self.label_24.SetPosition((180,44))
      self.round_spin.SetPosition((300,40))
      self.round_spin.SetSize((60,25))

      ## Children: ComboBox
      self.label_26.SetPosition((380,44))
      self.combo_box_ChildrenPresent.SetSize((60,25))
      self.combo_box_ChildrenPresent.SetPosition((380+120,40))

      height = 70
      ## Site: ComboBOx
      self.label_28.SetPosition((10,height+4))
      self.combo_box_SiteList.SetSize((80,25))
      self.combo_box_SiteList.SetPosition((70,height))

      self.label_29.SetPosition((180,height+4))
      self.combo_box_ActivityList.SetSize((150,25))
      self.combo_box_ActivityList.SetPosition((300,height))

      y1 = 100
      ## dice
      self.button_randSelKid.SetPosition((10,y1+15))
      self.combo_box_RndChildList.SetSize((170, 41))
      self.combo_box_RndChildList.SetSelection(0)
      self.combo_box_RndChildList.SetPosition((75,y1+20))
      self.child_present_checkbox.SetPosition((250,y1+24))

      ## observation count
      self.label_31.SetPosition((380,y1+24))
      self.observation_spin.SetPosition((530,y1+20))

      ## Timer
      self.label_8.SetPosition((10,y1+300))
      self.gauge_Timer.SetRange(self.timer_interval*2)
      self.gauge_Timer.SetPosition((140,y1+300))
      self.gauge_Timer1.SetRange(self.timer_interval*2)
      self.gauge_Timer1.SetPosition((240,y1+300))

      ## Buttons
      self.button_StartRecord.SetSize((144, 40))
      self.button_StartRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.button_StartRecord.SetPosition((10,y1+350))

      self.button_SaveRecord.SetSize((124, 40))
      self.button_SaveRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.button_SaveRecord.SetPosition((240,y1+350))
      self.button_SaveRecord.Disable()

      self.button_DiscardRecord.SetSize((124, 40))
      self.button_DiscardRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.button_DiscardRecord.SetPosition((380,y1+350))
      self.button_DiscardRecord.Disable()

      ## VR Code / Affect Code
      self.label_6.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_6.SetPosition((250,y1+100))

      self.radio_box_VR_1.SetSelection(0)
      self.radio_box_VR_1.SetPosition((250,y1+128))
      self.radio_box_VR_2.SetSelection(0)
      self.radio_box_VR_2.SetPosition((250,y1+168))
      self.radio_box_VR_3.SetSelection(0)
      self.radio_box_VR_3.SetPosition((250,y1+208))
      self.radio_box_VR_4.SetSelection(0)
      self.radio_box_VR_4.SetPosition((250,y1+248))

      self.label_7.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_7.SetPosition((480,y1+100))
      self.radio_box_Affect_1.SetSelection(0)
      self.radio_box_Affect_1.SetPosition((480,y1+128))
      self.radio_box_Affect_2.SetSelection(0)
      self.radio_box_Affect_2.SetPosition((480,y1+168))
      self.radio_box_Affect_3.SetSelection(0)
      self.radio_box_Affect_3.SetPosition((480,y1+208))
      self.radio_box_Affect_4.SetSelection(0)
      self.radio_box_Affect_4.SetPosition((480,y1+248))


      self.label_1.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_1.SetPosition((10,y1+100))

      self.label_2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_2.SetPosition((20,y1+138))

      self.combo_box_TargetChildList1.SetSelection(0)
      self.combo_box_TargetChildList1.SetPosition((110,y1+130))

      self.label_3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_3.SetPosition((20,y1+180))
      self.combo_box_TargetChildList2.SetSelection(0)
      self.combo_box_TargetChildList2.SetPosition((110,y1+172))

      self.label_4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_4.SetPosition((20,y1+220))
      self.combo_box_TargetChildList3.SetSelection(0)
      self.combo_box_TargetChildList3.SetPosition((110,y1+212))

      self.label_5.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
      self.label_5.SetPosition((20,y1+260))
      self.combo_box_TargetChildList4.SetSelection(0)
      self.combo_box_TargetChildList4.SetPosition((110,y1+252))


      self.label_9.SetSize((400,140))
      self.label_9.SetPosition((10,y1+400))

      self.led.SetSize((-100,25))
      self.led.SetPosition((300, y1+280))
      self.led.SetBackgroundColour("") #red
      self.led.SetForegroundColour("") #black

   def SaveRoundInfo(self):
      # save round info
      f = open('roundInfo.txt','w')
      for observerID in self.observerDict:
         roundInfo = self.observerDict[observerID]
         for classID in roundInfo:
            f.write('%s,%s,%s,%s,%s\n' % (observerID,
                                              roundInfo[classID][0],
                                           roundInfo[classID][1],
                                           classID,
                                           roundInfo[classID][2].strftime('%d/%m/%y')
                                           ))
      f.close()

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

   def GetRoundInfo(self):
      tmpDict = {}
      f = open('roundInfo.txt')
      line = f.readline()
      # add round info to a dict (observer:(classroom:(rounds,observations,date))
      while(len(line)>0):
         info = line.strip().split(',')
         observer = info[0]
         roundInfo = int(info[1])
         observationInfo = int(info[2])
         if len(info) > 3:
            observationClassroom = info[3]
            if len(info) > 4:
               observationDate = info[4]
               observationDate = datetime.strptime(observationDate, "%d/%m/%y")
               if self.new_round_at_new_day == True:
                  deltaDate = datetime.today() - observationDate
                  deltaDay = deltaDate.days
                  if deltaDay > 0: # start a new round
                     roundInfo += 1
                     observationInfo = 1
                     observationDate = datetime.today()
            else:
               observationDate = datetime.today()

            if not tmpDict.has_key(observer):
               tmpDict[observer] = {}
            tmpDict[observer][observationClassroom] = [roundInfo,observationInfo,observationDate]
         line = f.readline()
      f.close()

      return tmpDict

   def GetSiteList(self):
      siteList = []
      f = open('siteList.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip().split(',')
         if len(line) == 1:
            siteList.append('')
         else:
            siteList.append(line[1])
         line = f.readline()
      f.close()
      return siteList

   def GetKidList(self):
      kidList = []
      presentList = {}
      f = open('childIDList.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip().split(',')
         if len(line) == 1:
            kidList.append('')
         else:
            kidList.append(line[1])
            presentList[line[1]] = 1
         line = f.readline()
      f.close()
      return kidList, presentList

   def GetAdultList(self):
      adultList = []
      f = open('adultList.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip().split(',')
         if len(line) == 1:
            adultList.append('')
         else:
            adultList.append(line[1])
         line = f.readline()
      f.close()
      return adultList

   def GetObserverList(self):
      observerList = []
      f = open('coderList.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip().split(',')
         if len(line) == 1:
            observerList.append('')
         else:
            observerList.append(line[1])
         line = f.readline()
      f.close()
      return observerList

   def GetClassList(self):
      classList = [str(i) for i in range(101,117)]
      classList.insert(0,'')
      return classList

   def GetActivityList(self):
      activityList = []
      f = open('activityList.txt')
      line = f.readline()
      while(len(line)>0):
         line = line.strip().split(',')
         if len(line) == 1:
            activityList.append('')
         else:
            activityList.append(line[1])
         line = f.readline()
      f.close()
      return activityList


   def ChildPresentCheck(self,event):
      if self.PreCheck() == True:
         kid = self.record.childId
         self.presentList[kid] = 1-event.Checked()
         if event.Checked():#not present
            #record it
            self.button_DiscardRecord.Disable()
            self.button_SaveRecord.Enable()
            self.button_StartRecord.Disable()

   def OnRoundSpin(self,event):
      spinnedValue = event.GetInt()
      if self.PreCheck() and spinnedValue>=0:
         if spinnedValue == self.observerDict[self.currentObserver][self.currentClassroom][0]:
            self.observation_spin.SetValue(self.observerDict[self.currentObserver][self.currentClassroom][1])
         elif spinnedValue < self.observerDict[self.currentObserver][self.currentClassroom][0]:
            #dlg = wx.MessageDialog(self, 'You cannot roll back to an old round!','Warning',wx.OK)
            #dlg.ShowModal()
            #dlg.Destroy()
            self.round_spin.SetValue(spinnedValue+1)
            self.observation_spin.SetValue(self.observerDict[self.currentObserver][self.currentClassroom][1])
         else:
            self.observation_spin.SetValue(0)
      else:
         self.round_spin.SetValue(0)

   def OnStatusTimer(self,event):
      # clock
      # get current time from computer
      current = time.localtime(time.time())
      ts = time.strftime("%H:%M:%S", current)
      self.SetStatusText("current time: %s" % ts)
      ts = time.strftime("%d/%m/%y", current)
      self.label_21.SetLabel(ts)

   def OnTimer(self, event):
      # clock
      # get current time from computer
      current = time.localtime(time.time())
      ts = time.strftime("%H %M %S", current)
      self.led.SetValue(ts)

      #gauge
      if self.currentGauge == 1:
         current_gauge = self.gauge_Timer
      elif self.currentGauge == 2:
         current_gauge = self.gauge_Timer1

      self.count = self.count + 1  #timer_interval defaults to 6; see lists
      if self.timer_interval*2 - 4<=self.count <= self.timer_interval*2:
         if self.count % 2 == 0:
            self.label_8.SetForegroundColour("red")
         else:
            self.label_8.SetForegroundColour("black")
         self.Refresh()

      if self.count > self.timer_interval*2:
         self.label_8.SetForegroundColour("black")
         self.Refresh()
         if self.currentGauge == 1:
            self.button_DiscardRecord.Enable()
            self.timer.Stop()
            self.button_StartRecord.Enable()
            self.button_StartRecord.SetLabel("Continue Recording")
            self.currentGauge = 2
         elif self.currentGauge == 2:
            self.button_DiscardRecord.Enable()
            self.button_SaveRecord.Enable()
            self.timer.Stop()
            self.button_StartRecord.SetLabel("Start Recording")
            self.currentGauge = 1

      currentCount = self.count
      #if self.count > 18:
         #self.count = 0
         #currentCount = self.count - 18
      if self.count == 13:
         currentCount = self.count -1
      current_gauge.SetValue(currentCount)

   def PreCheck(self):
      if self.currentObserver == '':
         dlg = wx.MessageDialog(self, 'Please select current observer.','Info',wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return False
      if self.record == None:
         dlg = wx.MessageDialog(self, 'Please select observation child.','Info',wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return False
      return True

   def RandomSelectChild(self, event): # wxGlade: VAFrame.<event_handler>
      """ Allow a child to be randomly selected """
      childRandomPull = randint(0,(len(self.kidList)-1))
      ranChild = self.kidList[childRandomPull]
      dlg = wx.MessageDialog(self, ranChild,'Observe This Child:',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      self.combo_box_RndChildList.SetSelection(childRandomPull+1)
      self.child_present_checkbox.SetValue(1-self.presentList[ranChild])
      self.record = VARecord()
      self.record.childId = ranChild


   def ObserverSelected(self, event):
      self.currentObserver = event.GetString()
      if self.currentObserver != '':
         if not self.observerDict.has_key(self.currentObserver):
            # add new observert to observerDict
            self.observerDict[self.currentObserver] = {}

         if self.currentClassroom != '':
            roundInfo = self.observerDict[self.currentObserver]
            if roundInfo.has_key(self.currentClassroom):
               # round count
               self.round_spin.SetValue(roundInfo[self.currentClassroom][0])
               # observation count
               self.observation_spin.SetValue(roundInfo[self.currentClassroom][1])
            else:
               # new classroom record
               self.observerDict[self.currentObserver][self.currentClassroom] = [1,1,datetime.today()]
               self.round_spin.SetValue(1)
               self.observation_spin.SetValue(1)

      else:
         self.round_spin.SetValue(None)
         self.observation_spin.SetValue(None)

   def ClassroomSelected(self, event):
      self.currentClassroom = event.GetString()
      if self.currentClassroom != '' and self.currentObserver != '':
         roundInfo = self.observerDict[self.currentObserver]
         if roundInfo.has_key(self.currentClassroom):
            # round count
            self.round_spin.SetValue(roundInfo[self.currentClassroom][0])
            # observation count
            self.observation_spin.SetValue(roundInfo[self.currentClassroom][1])
         else:
            # new classroom record
            self.observerDict[self.currentObserver][self.currentClassroom] = [1,1,datetime.today()]
            self.round_spin.SetValue(1)
            self.observation_spin.SetValue(1)

   def RandomChildSelected(self, event):
      kidId = event.GetString()
      dlg = wx.MessageDialog(self, kidId,'Observe This Child:',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()

      self.record = VARecord()
      self.record.childId = kidId
      self.child_present_checkbox.SetValue(1-self.presentList[kidId])
      if self.presentList[kidId] == 0:
         #record it directly
         self.button_DiscardRecord.Disable()
         self.button_SaveRecord.Enable()
         self.button_StartRecord.Disable()

   def StartRecord(self, event):
      if self.PreCheck():
         #self.gauge_Timer.SetValue(0)
         self.count = 0
         # update clock digits every second (1000ms)
         self.timer.Start(500)
         self.OnTimer(None)

         self.button_StartRecord.Disable()

   def ResetCtls(self):
      self.combo_box_RndChildList.SetSelection(0)
      self.combo_box_TargetChildList1.SetSelection(0)
      self.combo_box_TargetChildList2.SetSelection(0)
      self.combo_box_TargetChildList3.SetSelection(0)
      self.combo_box_TargetChildList4.SetSelection(0)
      self.radio_box_Affect_1.SetSelection(0)
      self.radio_box_VR_1.SetSelection(0)
      self.radio_box_Affect_2.SetSelection(0)
      self.radio_box_VR_2.SetSelection(0)
      self.radio_box_Affect_3.SetSelection(0)
      self.radio_box_VR_3.SetSelection(0)
      self.radio_box_Affect_4.SetSelection(0)
      self.radio_box_VR_4.SetSelection(0)
      self.gauge_Timer.SetValue(0)
      self.gauge_Timer1.SetValue(0)

   def DiscardRecord(self, event):
      self.currentGauge = 1
      self.button_StartRecord.SetLabel("Start Recording")
      self.record = None

      self.ResetCtls()
      self.button_StartRecord.Enable()
      self.button_SaveRecord.Disable()
      self.button_DiscardRecord.Disable()

      dlg = wx.MessageDialog(self, 'Current record is discarded.','Infor',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()

   def SelectVisualTarget1(self, event):
      if self.PreCheck():
         self.record.targetId1 = event.GetString()
      else:
         self.combo_box_TargetChildList1.SetSelection(0)

   def SelectVisualTarget2(self, event):
      if self.PreCheck():
         self.record.targetId2 = event.GetString()
      else:
         self.combo_box_TargetChildList2.SetSelection(0)


   def SelectVisualTarget3(self, event):
      if self.PreCheck():
         self.record.targetId3 = event.GetString()
      else:
         self.combo_box_TargetChildList3.SetSelection(0)


   def SelectVisualTarget4(self, event):
      if self.PreCheck():
         self.record.targetId4 = event.GetString()
      else:
         self.combo_box_TargetChildList4.SetSelection(0)

   def SelectVR_1(self, event):
      if self.PreCheck():
         self.record.VR_1 = str(event.GetSelection())
      else:
         self.radio_box_VR_1.SetSelection(0)
   def SelectVR_2(self, event):
      if self.PreCheck():
         self.record.VR_2 = str(event.GetSelection())
      else:
         self.radio_box_VR_2.SetSelection(0)
   def SelectVR_3(self, event):
      if self.PreCheck():
         self.record.VR_3 = str(event.GetSelection())
      else:
         self.radio_box_VR_3.SetSelection(0)
   def SelectVR_4(self, event):
      if self.PreCheck():
         self.record.VR_4 = str(event.GetSelection())
      else:
         self.radio_box_VR_4.SetSelection(0)

   def SelectAffect_1(self, event):
      if self.PreCheck():
         self.record.affect_1 = str(event.GetSelection())
      else:
         self.radio_box_Affect_1.SetSelection(0)
   def SelectAffect_2(self, event):
      if self.PreCheck():
         self.record.affect_2 = str(event.GetSelection())
      else:
         self.radio_box_Affect_2.SetSelection(0)
   def SelectAffect_3(self, event):
      if self.PreCheck():
         self.record.affect_3 = str(event.GetSelection())
      else:
         self.radio_box_Affect_3.SetSelection(0)
   def SelectAffect_4(self, event):
      if self.PreCheck():
         self.record.affect_4 = str(event.GetSelection())
      else:
         self.radio_box_Affect_4.SetSelection(0)

   def CheckHeader(self,item):
      itemName = item.GetName()
      if item.GetValue() == '':
         dlg = wx.MessageDialog(self, itemName+' is empty!','Error',wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return False
      return True

   def SaveRecord(self, event):
      if self.record == None \
           or self.CheckHeader(self.combo_box_ActivityList) == False\
           or self.CheckHeader(self.combo_box_ChildrenPresent) == False\
           or self.CheckHeader(self.combo_box_ClassList) == False\
           or self.CheckHeader(self.combo_box_ObserverList) == False\
           or self.CheckHeader(self.combo_box_SiteList) == False:
         #or self.CheckHeader(self.combo_box_RoundList) == False\
         dlg = wx.MessageDialog(self, 'Record content error!','Error',wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return False

      current = time.localtime(time.time())
      ts = time.strftime("%d/%m/%y %H:%M:%S", current)

      observer = self.combo_box_ObserverList.GetValue()
      classId = self.combo_box_ClassList.GetValue()
      roundId = self.round_spin.GetValue()
      childrenPresent = self.combo_box_ChildrenPresent.GetValue()
      site = self.combo_box_SiteList.GetValue()
      activity = self.combo_box_ActivityList.GetValue()
      observationId = self.observation_spin.GetValue()

      output = None
      if not os.path.exists(self.recordFileName):
         output = open(self.recordFileName,'w')
         output.write('time,observer,class_id,round_id,observation_id,#children present,site,activity,child_id,isPresent,target1,VR1,Affect1,target2,VR2,Affect2,target3,VR3,Affect3,target4,VR4,Affect4\n')
      else:
         output = open(self.recordFileName,'a')
      output.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
                     (ts,
                      observer,
                      classId,
                      roundId,
                      observationId,
                      childrenPresent,
                      site,
                      activity,
                      self.record.childId,
                      self.presentList[self.record.childId],
                      self.record.targetId1,
                      self.record.VR_1,
                      self.record.affect_1,
                      self.record.targetId2,
                      self.record.VR_2,
                      self.record.affect_2,
                      self.record.targetId3,
                      self.record.VR_3,
                      self.record.affect_3,
                      self.record.targetId4,
                      self.record.VR_4,
                      self.record.affect_4
                      ))
      output.close()

      # increase observation count

      if int(observationId) > self.max_observation_per_round:
         dlg = wx.MessageDialog(self,
                                   'Can not save. This user reaches %s observation count in this classroom today.'%self.max_observation_per_round,
                                   'Warning',
                                   wx.OK)
         dlg.ShowModal()
         dlg.Destroy()
         return


      self.observerDict[self.currentObserver][self.currentClassroom][1] = int(observationId) + 1
      observationCount = self.observerDict[self.currentObserver][self.currentClassroom][1]
      self.observation_spin.SetValue(observationCount)

      self.SaveRoundInfo()

      # reset contrls
      self.ResetCtls()
      self.button_StartRecord.Enable()
      self.button_SaveRecord.Disable()
      self.button_DiscardRecord.Disable()
      self.child_present_checkbox.SetValue(0)
      self.record = None

      dlg = wx.MessageDialog(self, '1 record is added!','Info',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()

# end of class VAFrame


if __name__ == "__main__":
   app = wx.App(False)
   #classroom ='104'
   #childList = ['?','000','001','002','003','004','005','006','007','008','009','010','011','012','013']
   #adultList = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13']
   outputfilename = 'vaOutput.csv'
   data = [outputfilename]
   #data = [classroom,childList,adultList,outputfilename]
   frame = VAFrame(data, title="Room Selection")
   frame.Show()
   app.MainLoop()
