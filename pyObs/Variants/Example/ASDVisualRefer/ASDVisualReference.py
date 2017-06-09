""" This is an example of using pyObs to construct
an Autism Spectrum Disorder joint attention observation 
coding data collection GUI"""

__version__ = 'ASD Joint Attention; pyObsExample; .8'
__author__ = 'William A Griffin'
__author_email__ = 'william.griffin@asu.edu'


import wx
import  wx.gizmos   as  gizmos
import  wx.lib.buttons  as  buttons
import time,copy,os, sys
from random import randint
import bitRedDice

### for MAC
#if sys.platform == 'Snow Leopard':
    #list_dir = "/Users/observer/Documents/AffExp/lists/"
#if sys.platform == 'win32':
    #list_dir = "C:\\AffExp\\lists\\"

class VARecord():
    def __init__(self):
        self.classId = ''
        self.childId = ''
        self.targetId1 = '?'
        self.targetId2 = ''
        self.targetId3 = ''
        self.targetId4 = ''
        self.Attend = '0' #0-2
        self.affect = '0' # 0-4

class VAFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # from *args
        if len(args) == 0:
            dlg = wx.MessageDialog(self, 'Parameters setting error','Error',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        #self.classid = args[0][0]
        #self.kidList = args[0][1]
        #self.adultList = args[0][2]
        self.recordFileName = args[0][0] #args[0][3]

        # local variables
        self.siteList = self.GetSiteList()
        self.kidList = self.GetKidList()
        self.adultList = self.GetAdultList()

        self.observerList = self.GetObserverList()
        self.classList = self.GetClassList()
        self.activityList = self.GetActivityList()

        self.rndKidList = self.kidList[:]
        self.rndKidList.insert(0,'Random Select Child')
        self.vaKidList = self.kidList + self.adultList
        self.vaKidList.insert(0,'')
        self.vaKidList.insert(1,'?')
        self.record = None

        self.currentGauge = 1
        self.observerDict = self.GetRoundInfo()
        self.currentObserver = ''

        # GUI
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, None, -1, **kwds)
        self.CreateStatusBar()

        panel = wx.Panel(self, -1)
        self.SetBackgroundColour( (217, 241 , 255))

        self.label_30 = wx.StaticText(panel, -1, '')
        self.label_31 = wx.StaticText(panel, -1, "Current observation #:")
        self.input1 = wx.TextCtrl(panel, -1, '', (95, 105))

        self.label_20 = wx.StaticText(panel, -1, "Date:")
        self.label_21 = wx.StaticText(panel, -1, "")
        self.label_22 = wx.StaticText(panel, -1, "Observer:")
        self.combo_box_ObserverList = wx.ComboBox(panel, -1, choices=self.observerList, style=wx.CB_DROPDOWN)
        self.label_23 = wx.StaticText(panel, -1, "Class:")
        self.combo_box_ClassList = wx.ComboBox(panel, -1, choices=self.classList, style=wx.CB_DROPDOWN)
        self.label_24 = wx.StaticText(panel, -1, "Round# (today):")
        #roundList = [str(i) for i in range(1,21)]
        #roundList.insert(0,'')
        #self.combo_box_RoundList= wx.ComboBox(panel, -1, choices=roundList, style=wx.CB_DROPDOWN)

        self.label_26 = wx.StaticText(panel, -1, "# Children present:")
        #self.label_27 = wx.StaticText(panel, -1, "")
        numOfChild = [str(i) for i in range(1,len(self.kidList))]
        numOfChild.insert(0,'')
        self.combo_box_ChildrenPresent = wx.ComboBox(panel, -1, choices=numOfChild, style=wx.CB_DROPDOWN)
        self.label_28 = wx.StaticText(panel, -1, "Site:")
        self.combo_box_SiteList = wx.ComboBox(panel, -1, choices=self.siteList, style=wx.CB_DROPDOWN)
        self.label_29 = wx.StaticText(panel, -1, "Activity setting:")
        self.combo_box_ActivityList = wx.ComboBox(panel, -1, choices=self.activityList, style=wx.CB_DROPDOWN)


        self.button_randSelKid = buttons.GenBitmapButton(panel, -1, bitRedDice.getsmall_red_diceBitmap(), style = 1)
        self.combo_box_RndChildList = wx.ComboBox(panel, -1,choices=self.rndKidList, style=wx.CB_DROPDOWN)
        self.button_StartRecord = wx.Button(panel, -1, "Start Recording")
        self.button_SaveRecord = wx.Button(panel, -1, "Save Record")
        self.button_DiscardRecord = wx.Button(panel, -1, "Discard Record")
        self.gauge_Timer = wx.Gauge(panel, -1, size=(100, 30))
        self.gauge_Timer1 = wx.Gauge(panel, -1, size=(100, 30))
        self.label_6 = wx.StaticText(panel, -1, "Attention:")
        self.radio_box_Attend = wx.RadioBox(panel, -1, "", choices=["N/A", "Glance", "Look"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.label_1 = wx.StaticText(panel, -1, "Joint Attention To:")
        self.label_2 = wx.StaticText(panel, -1, "Attend Target 1:")
        self.combo_box_TargetChildList1 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
        self.label_3 = wx.StaticText(panel, -1, "Attend Target 2:")
        self.combo_box_TargetChildList2 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
        self.label_4 = wx.StaticText(panel, -1, "Attend Target 3:")
        self.combo_box_TargetChildList3 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
        self.label_5 = wx.StaticText(panel, -1, "Attend Target 4:")
        self.combo_box_TargetChildList4 = wx.ComboBox(panel, -1, choices=self.vaKidList, style=wx.CB_DROPDOWN)
        self.label_7 = wx.StaticText(panel, -1, "Affect:")
        self.radio_box_Affect = wx.RadioBox(panel, -1, "", choices=["N/A","Positive", "Neutral", "Negtive"], majorDimension=0, style=wx.RA_SPECIFY_ROWS)
        self.label_8 = wx.StaticText(panel, -1, "6 seconds timer:")
        self.label_9 = wx.StaticText(panel, -1, """
Coder Note: Observe the target child for a period 6-sec.\
Identify each person with whom the target child follows attending behavior.\
Episodes of joint attention are coded as "G" if the child looks briefly (<3-sec) \
at the reference object and coded as "L"\
if the child looks for a longer (>=3-sec).  \
After scoring "G" or "L", record affect.
""")

        self.led = gizmos.LEDNumberCtrl(panel, -1)
        self.__set_properties()
        #self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.RandomSelectChild, self.button_randSelKid)
        self.Bind(wx.EVT_COMBOBOX, self.RandomChildSelected, self.combo_box_RndChildList)
        self.Bind(wx.EVT_BUTTON, self.StartRecord, self.button_StartRecord)
        self.Bind(wx.EVT_BUTTON, self.SaveRecord, self.button_SaveRecord)
        self.Bind(wx.EVT_BUTTON, self.DiscardRecord, self.button_DiscardRecord)
        self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget1, self.combo_box_TargetChildList1)
        self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget2, self.combo_box_TargetChildList2)
        self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget3, self.combo_box_TargetChildList3)
        self.Bind(wx.EVT_COMBOBOX, self.SelectVisualTarget4, self.combo_box_TargetChildList4)
        self.Bind(wx.EVT_RADIOBOX, self.SelectAttend, self.radio_box_Attend)
        self.Bind(wx.EVT_RADIOBOX, self.SelectAffect, self.radio_box_Affect)
        self.Bind(wx.EVT_COMBOBOX, self.ObserverSelected, self.combo_box_ObserverList)
        id1 = wx.NewId()
        wx.RegisterId(id1)
        self.timer = wx.Timer(self, id1)
        self.Bind(wx.EVT_TIMER, self.OnTimer,self.timer,id1)
        id2 = wx.NewId()
        wx.RegisterId(id1)
        self.statusTimer = wx.Timer(self,id2)
        self.Bind(wx.EVT_TIMER, self.OnStatusTimer,self.statusTimer,id2)
        

        self.count = 0
        self.statusTimer.Start(1000)
        self.OnStatusTimer(None)


    def __set_properties(self):
        self.SetTitle("ASD Joint Attention")
        self.SetSize((670, 700))
        self.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

        ## Date: 08/09/10
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

        ## Round: Combobox
        self.label_24.SetPosition((180,44))
        #self.combo_box_RoundList.SetSize((60,25))
        #self.combo_box_RoundList.SetPosition((300,40))
        self.label_30.SetPosition((300,40))

        ## Children: ComboBox
        self.label_26.SetPosition((370,44))
        self.combo_box_ChildrenPresent.SetSize((60,25))
        self.combo_box_ChildrenPresent.SetPosition((380+120,40))

        height = 70
        ## Site: Combobox
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

        ## observation count
        self.label_31.SetPosition((260,y1+24))
        self.input1.SetPosition((410,y1+20))

        ## Timer
        self.label_8.SetPosition((470,y1+100))
        self.gauge_Timer.SetRange(18)
        self.gauge_Timer.SetPosition((470,y1+126))
        self.gauge_Timer1.SetRange(18)
        self.gauge_Timer1.SetPosition((470,y1+226))


        ## Buttons
        self.button_StartRecord.SetSize((144, 40))
        self.button_StartRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_StartRecord.SetPosition((10,y1+330))

        self.button_SaveRecord.SetSize((124, 40))
        self.button_SaveRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_SaveRecord.SetPosition((240,y1+330))
        self.button_SaveRecord.Disable()

        self.button_DiscardRecord.SetSize((124, 40))
        self.button_DiscardRecord.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_DiscardRecord.SetPosition((380,y1+330))
        self.button_DiscardRecord.Disable()

        ## Attend Code / Affect Code
        self.label_6.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_6.SetPosition((300,y1+100))

        self.radio_box_Attend.SetSelection(0)
        self.radio_box_Attend.SetPosition((370,y1+100))

        self.label_1.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_1.SetPosition((10,y1+100))

        self.label_2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_2.SetPosition((40,y1+140))

        self.combo_box_TargetChildList1.SetSelection(0)
        self.combo_box_TargetChildList1.SetPosition((160,y1+140))

        self.label_3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_3.SetPosition((40,y1+180))
        self.combo_box_TargetChildList2.SetSelection(0)
        self.combo_box_TargetChildList2.SetPosition((160,y1+180))

        self.label_4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_4.SetPosition((40,y1+220))
        self.combo_box_TargetChildList3.SetSelection(0)
        self.combo_box_TargetChildList3.SetPosition((160,y1+220))

        self.label_5.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_5.SetPosition((40,y1+260))
        self.combo_box_TargetChildList4.SetSelection(0)
        self.combo_box_TargetChildList4.SetPosition((160,y1+260))

        self.label_7.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_7.SetPosition((300,y1+200))
        self.radio_box_Affect.SetSelection(0)
        self.radio_box_Affect.SetPosition((370,y1+200))

        self.label_9.SetSize((400,140))
        self.label_9.SetPosition((10,y1+400))

        self.led.SetSize((-100,25))
        self.led.SetPosition((300, y1+280))
        self.led.SetBackgroundColour("") #red
        self.led.SetForegroundColour("")  #black

    def SaveRoundInfo(self):
        # save round info
        f = open('ASDroundInfo.txt','w')
        for observerID in self.observerDict:
            f.write('%s;%s;%s\n' % (observerID,self.observerDict[observerID][0],self.observerDict[observerID][1]))
        f.close()

    ####
    def GetRoundInfo(self):
        tmpDict = {}
        f = open('ASDroundInfo.txt')
        line = f.readline()
        # add round info to a dict (observer:(round,observation))
        while(len(line)>0):
            info = line.strip().split(';')
            observerInfo = info[0]
            roundInfo = int(info[1])
            observationInfo = int(info[2])
            tmpDict[observerInfo] = [roundInfo, observationInfo]
            line = f.readline()
        f.close()

        return tmpDict

    def GetSiteList(self):
        siteList = []
        f = open('siteList.txt')
        line = f.readline()
        while(len(line)>0):
            line = line.strip().split(';')
            if len(line) == 1:
                siteList.append('')
            else:
                siteList.append(line[1])
            line = f.readline()
        f.close()
        return siteList

    def GetKidList(self):
        kidList = []
        f = open('childIDList.txt')
        line = f.readline()
        while(len(line)>0):
            line = line.strip().split(';')
            if len(line) == 1:
                kidList.append('')
            else:
                kidList.append(line[1])
            line = f.readline()
        f.close()
        return kidList

    def GetAdultList(self):
        adultList = []
        f = open('adultList.txt')
        line = f.readline()
        while(len(line)>0):
            line = line.strip().split(';')
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
            line = line.strip().split(';')
            if len(line) == 1:
                observerList.append('')
            else:
                observerList.append(line[1])
            line = f.readline()
        f.close()
        return observerList

    def GetClassList(self):
        classList = [str(i) for i in range(1,11)]
        classList.insert(0,'')
        return classList

    def GetActivityList(self):
        activityList = []
        f = open('activityList.txt')
        line = f.readline()
        while(len(line)>0):
            line = line.strip().split(';')
            if len(line) == 1:
                activityList.append('')
            else:
                activityList.append(line[1])
            line = f.readline()
        f.close()
        return activityList

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

        #guage
        if self.currentGauge == 1:
            current_gauge = self.gauge_Timer
        elif self.currentGauge == 2:
            current_gauge = self.gauge_Timer1

        self.count = self.count + 1
        if 12<=self.count <= 18:
            if self.count % 2 == 0:
                self.label_8.SetForegroundColour("red")
            else:
                self.label_8.SetForegroundColour("black")
            self.Refresh()

        if self.count > 18:
            self.label_8.SetForegroundColour("black")
            self.Refresh()
            self.count = 0
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
        if self.count > 18:
            currentCount = self.count - 18
        current_gauge.SetValue(currentCount)

    def PreCheck(self):
        if self.currentObserver == '':
            dlg = wx.MessageDialog(self, 'Select observer.','Info',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        if self.record == None:
            dlg = wx.MessageDialog(self, 'Select target child.','Info',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        return True

    def RandomSelectChild(self, event): 
        """ Allow a child to be randomly selected """
        childRandomPull = randint(0,(len(self.kidList)-1))
        ranChild = self.kidList[childRandomPull]
        dlg = wx.MessageDialog(self, ranChild,'Observe This Child:',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.combo_box_RndChildList.SetSelection(childRandomPull+1)

        self.record = VARecord()
        self.record.childId = ranChild

    def ObserverSelected(self, event):
        self.currentObserver = event.GetString()
        if self.currentObserver != '' and self.observerDict.has_key(self.currentObserver):
            # round count
            self.label_30.SetLabel(str(self.observerDict[self.currentObserver][0]))
            # observation count
            self.input1.SetValue(str(self.observerDict[self.currentObserver][1]))
        else:
            self.label_30.SetLabel('')
            self.input1.SetValue('')


    def RandomChildSelected(self, event): 
        kidId = event.GetString()
        dlg = wx.MessageDialog(self, kidId,'Observe This Child:',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        self.record = VARecord()
        self.record.childId = kidId

    def StartRecord(self, event): 
        if self.PreCheck():
            self.gauge_Timer.SetValue(0)
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
        self.radio_box_Affect.SetSelection(0)
        self.radio_box_Attend.SetSelection(0)

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

    def SelectAttend(self, event): 
        if self.PreCheck():
            self.record.Attend = str(event.GetSelection())
        else:
            self.radio_box_Attend.SetSelection(0)


    def SelectAffect(self, event): 
        if self.PreCheck():
            self.record.affect = str(event.GetSelection())
        else:
            self.radio_box_Affect.SetSelection(0)

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
        roundId = self.label_30.GetLabel()
        childrenPresent = self.combo_box_ChildrenPresent.GetValue()
        site = self.combo_box_SiteList.GetValue()
        activity = self.combo_box_ActivityList.GetValue()
        observationId = self.input1.GetValue()

        output = None
        if not os.path.exists(self.recordFileName):
            output = open(self.recordFileName,'w')
            output.write('time,observer,class_id,round_id,observation_id,#children present,site,activity,child_id,Attend,target1,target2,target3,target4,affect\n')
        else:
            output = open(self.recordFileName,'a')
        output.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
                     (ts,
                      observer,
                      classId,
                      roundId,
                      observationId,
                      childrenPresent,
                      site,
                      activity,
                      self.record.childId,
                      self.record.Attend,
                      self.record.targetId1,
                      self.record.targetId2,
                      self.record.targetId3,
                      self.record.targetId4,
                      self.record.affect))
        output.close()

        # increase observation count
        if int(observationId) < 200:
            self.observerDict[self.currentObserver][1] = int(observationId) + 1
            observationCount = self.observerDict[self.currentObserver][1]
            self.input1.SetValue(str(observationCount))
        else:
            # round + 1
            self.observerDict[self.currentObserver][0] += 1
            roundCount = self.observerDict[self.currentObserver][0]
            # reset observation count
            self.observerDict[self.currentObserver][1] = 1
            observationCount = self.observerDict[self.currentObserver][1]

            self.label_30.SetLabel(str(roundCount))
            self.input1.SetValue(str(observationCount))

        self.SaveRoundInfo()

        # reset contrls
        self.ResetCtls()
        self.button_StartRecord.Enable()
        self.button_SaveRecord.Disable()
        self.button_DiscardRecord.Disable()
        self.record = None

        dlg = wx.MessageDialog(self, '1 record is added!','Info',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()




if __name__ == "__main__":
    app = wx.App()
    outputfilename = 'JointAttendOutput.csv'
    data = [outputfilename]
    frame = VAFrame(data, title="Room Selection")
    frame.Show()
    app.MainLoop()
