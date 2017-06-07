""" pyObs: Individual 
This is the scan procedure for collecting
observational data on the playground at ASU's
Child Development Lab.  Funded via NSF #
Orginal Copyright 2006, William Griffin
"""

__version__ = 'Individual_2.2.01'
__author__ = 'William A Griffin'
__author_email__ = 'william.griffin@asu.edu'


import wx, os, sys, time
import wx.lib.statbmp as statbmp
import  wx.lib.buttons  as  buttons
from random import randint
from numpy import *
import bitPALsMaps

# System Selection
# modify as needed
if sys.platform == 'darwin':
    list_dir = "./lists/"
if sys.platform == 'win32':    
    list_dir = ".//lists"
if sys.platform == 'linux2':
    list_dir = "./lists/"    

USE_GENERIC = 0

if USE_GENERIC:
    from wx.lib.stattext import GenStaticText as StaticText
else:
    StaticText = wx.StaticText

class PALsFrame(wx.Frame):    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Project Name', size=(1024, 768)) #project name
        global maps, childList, errorReview

        errorReview = 0

        panel = wx.Panel(self, -1)        

        """ Let's make it look good """
        #self.SetBackgroundColour(wx.NullColour)#("sky blue")  
        self.SetBackgroundColour("sky blue") 

        text = StaticText(panel, -1, "Data Entry: Ind", (15, 5))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        text.SetFont(font)

        text2 = StaticText(panel, -1, "pyObs", (650, 365))
        font = wx.Font(35, wx.SWISS, wx.NORMAL, wx.BOLD)
        text2.SetFont(font)

        """ Put the GIS data in a 'global' list (or dictionary). """
        maps = []

        """ Begin data acquistion section """ 
        """ Mapping Buttons """               
        wx.StaticText(panel, -1, "Outside #1", (350, 5))
        bmpOut1I = bitPALsMaps.getOut1IconBitmap()  #converted prior
        #bmpOut1I = wx.Bitmap("Out1Icon.bmp") 
        bO1 = buttons.GenBitmapButton(panel, -1, bmpOut1I, (350, 20))
        self.Bind(wx.EVT_BUTTON, self.OnMapButton1, bO1)         

        wx.StaticText(panel, -1, "Outside #2", (350, 165))
        bmpOut2I = bitPALsMaps.getOut2IconBitmap()  #converted prior
        #bmpOut2I = wx.Bitmap("Out2Icon.bmp")
        bO2 = buttons.GenBitmapButton(panel, -1, bmpOut2I, (350, 180))
        self.Bind(wx.EVT_BUTTON, self.OnMapButton2, bO2)

        wx.StaticText(panel, -1, "Outside #3", (350, 325))
        bmpOut3I = bitPALsMaps.getOut3IconBitmap()  #converted prior
        #bmpOut3I = wx.Bitmap("Out3Icon.bmp") 
        bO3 = buttons.GenBitmapButton(panel, -1, bmpOut3I, (350, 340))
        self.Bind(wx.EVT_BUTTON, self.OnMapButton3, bO3)

        wx.StaticText(panel, -1, "Inside Classroom #1", (600, 5))
        bmpLacI = bitPALsMaps.getCourtney2IconBitmap()  #converted prior
        #bmpLacI = wx.Bitmap("Courtney2Icon.bmp") 
        bL = buttons.GenBitmapButton(panel, -1, bmpLacI, (600, 20))
        self.Bind(wx.EVT_BUTTON, self.OnMapButtonCourtney2, bL)

        wx.StaticText(panel, -1, "Inside Classroom #2", (600, 165))
        bmpCourtI = bitPALsMaps.getGordonIconBitmap()  #converted prior
        #bmpCourtI = wx.Bitmap("GordonIcon.bmp") 
        bC = buttons.GenBitmapButton(panel, -1, bmpCourtI, (600, 180))
        self.Bind(wx.EVT_BUTTON, self.OnMapButtonGordon, bC)

        """ Select Random Child """              
        wx.StaticText(panel, -1, "Pick Child Randomly", (165,180))
        ranKid = bitPALsMaps.getsmall_red_diceBitmap()  #converted prior
        #ranKid = wx.Bitmap("small_red_dice.bmp")#("roll.bmp")
        ranKidGet = buttons.GenBitmapButton(panel, -1, ranKid,\
                                            (180, 195), style = 1)
        self.Bind(wx.EVT_BUTTON, self.OnRanButton, ranKidGet)

        """ Data Selection Section """

        """ Event List  """
        eventList = []
        for x in range(0,300): 
            eventList.append(str(x))            
        wx.StaticText(panel, -1, "Event Number:", (15, 50))
        self.event = wx.Choice(panel, -1, (25, 70), choices = eventList)
        self.event.SetSelection(1)

        """ Coder List; internal or external list """
        coderList = ['', 'Observer 1', 'Observer 2', 'Observer 3', 'Observer 4', 'Observer 5']
        
        wx.StaticText(panel, -1, "Coder ID List:", (15, 100))
        self.coderID = wx.Choice(panel, -1, (25, 115), choices = coderList)
        self.coderID.SetSelection(0)
        
        """ Child List; add new names at the end, immedately prior to Other Peer; 
        remember to add ID number to ID list; internal or external list.  There is a
        corresponding ID number associated with each child. """         
        childList = [' ', 'Child 1', 'Child 2', 'Child 3', 'Child 4', 'Child 5', 'Child 6',\
                     'Child 7', 'Child 8', 'Child 9', 'Child 10', 'Other Peer 1', 'Other Peer 2', 'Other Peer 3',\
                     'Toddler Peer 1', 'Toddler Peer 2', 'Toddler Peer 3']
        
        wx.StaticText(panel, -1, "Child List:", (15, 150))
        self.child = wx.Choice(panel, -1, (25, 165), choices = childList) 

        """ Child Available List  """
        childAvailist = ['','Yes', 'Absent', 'Yes, Unavailable']
        wx.StaticText(panel, -1, "Child Available:", (15, 200))
        self.childAdvail = wx.Choice(panel, -1, (25, 215), choices = childAvailist)
        self.childAdvail.SetSelection(0)

        """ Structure List  """                    
        structureList = ['None', 'FreePlay', 'Structured']
        wx.StaticText(panel, -1, "Play Structure", (15, 250))
        self.playStructure = wx.Choice(panel, -1, (25, 265), choices = structureList)       
        self.playStructure.SetSelection(0)

        """ Play Location List  """
        inoutList = ['None', 'In', 'Out']
        wx.StaticText(panel, -1, "Play Location", (135, 250))
        self.playLocation = wx.Choice(panel, -1, (145, 265), choices = inoutList)        
        self.playLocation.SetSelection(0)

        """ Behavior Type List  """
        behaviorList = ['None', 'Solitary', 'Parallel', 'Social', 'Teacher Oriented']
        wx.StaticText(panel, -1, "Behavior", (15, 290))
        self.behaviorType = wx.Choice(panel, -1, (25, 305), choices = behaviorList)          
        self.behaviorType.SetSelection(0)

        """ Teacher Available List  """
        ifTeachAvailList = ['None', 'Yes', 'No']
        wx.StaticText(panel, -1, "TeacherPres", (160, 290))
        self.ifTeachAvail = wx.Choice(panel, -1, (160, 305), choices = ifTeachAvailList)  
        self.ifTeachAvail.SetSelection(0)      

        """ If Teacher List  """
        ifTeacherList = ['None', 'Corrective', 'Resource', 'PlayMate']
        wx.StaticText(panel, -1, "Teacher Role", (235, 290))
        self.ifTeacher = wx.Choice(panel, -1, (235, 305), choices = ifTeacherList)  
        self.ifTeacher.SetSelection(0)

        """ Initiation """
        initiationList = ['None', 'Target', 'Peer']
        wx.StaticText(panel, -1, "Initiation", (15, 329))
        self.initiation = wx.Choice(panel, -1, (25, 341), choices = initiationList)          
        self.initiation.SetSelection(0)

        """ Task List  """              
        taskList = ['None','Affection','Art','Board Games','Circle Time','Clean up',\
                    'Computer','Conflict','Digging',\
                    'Figure play','Instruction','Instrumental Help',\
                    'Language Arts','Large motor','Manipulatives','Math/Science',\
                    'Molding','Music/Singing','Onlooking','Other','Physical Games',\
                    'Pretend Play','Problem Solve','Sensory Play','Snack','Talk',\
                    'Unoccupied','Walking','Non-directed Physical','Animal Obs']    
                    

        wx.StaticText(panel, -1, "Task", (15, 363))
        self.taskList = wx.Choice(panel, -1, (25, 377), choices = taskList) 
        self.taskList.SetSelection(0)

        """ TeacherSolicit """ 
        self.teachSol = wx.CheckBox(panel, -1, "Teacher Solicit", (250, 341),(95, 20), wx.NO_BORDER)

        """ Affect List  """        
        affectList = ['None', 'Positive', 'Neutral', 'Negative', 'Unseen']
        wx.StaticText(panel, -1, "T_Affect", (15, 403))
        self.affectList = wx.Choice(panel, -1, (25, 418), choices = affectList)                
        self.affectList.SetSelection(0)
        """ Affect Direction List  """        
        affectDirectionList = ['None', '1', '2', 'Unknown']
        wx.StaticText(panel, -1, "T_Direction", (130, 403))
        self.affectDirectList = wx.Choice(panel, -1, (128, 418), choices = affectDirectionList)        
        self.affectDirectList.SetSelection(0)
        """ Affect Intensity List  """                
        affectIntensityList = ['None', 'NeutralNone', 'Minimal', 'Moderate', 'Strong', 'Unseen']
        wx.StaticText(panel, -1, "T_Intensity", (230, 403))
        self.affectIntenseList = wx.Choice(panel, -1, (228, 418), choices = affectIntensityList)        
        self.affectIntenseList.SetSelection(0)

        """ Peers """   

        """ Peer1 """
        wx.StaticText(panel, -1, "Peer 1 List", (15, 450))
        self.peer1 = wx.Choice(panel, -1, (25, 465), choices = childList) 
        self.peer1.SetSelection(0)
        """ Peer1 Affect"""
        wx.StaticText(panel, -1, "Peer 1 Affect", (15, 495))
        self.peer1Affect = wx.Choice(panel, -1, (25, 510), choices = affectList)
        self.peer1Affect.SetSelection(0)
        """ Peer1 Direction """
        wx.StaticText(panel, -1, "Peer 1 Direction", (130, 495))
        self.peer1Direction = wx.Choice(panel, -1, (128, 510), choices = affectDirectionList)
        self.peer1Direction.SetSelection(0)
        """ Peer1 Intensity """
        wx.StaticText(panel, -1, "Peer 1 Intensity", (230, 495))
        self.peer1Intensity = wx.Choice(panel, -1, (228, 510), choices = affectIntensityList)
        self.peer1Intensity.SetSelection(0)

        """ Peer 2 """              
        wx.StaticText(panel, -1, "Peer 2 List", (330, 495))
        self.peer2 = wx.Choice(panel, -1, (328, 510), choices = childList)
        self.peer2.SetSelection(0)
        """ Peer 3 """
        wx.StaticText(panel, -1, "Peer 3 List", (430, 495))
        self.peer3 = wx.Choice(panel, -1, (428, 510), choices = childList)
        self.peer3.SetSelection(0)
        """ Peer 4 """
        wx.StaticText(panel, -1, "Peer 4 List", (530, 495))
        self.peer4 = wx.Choice(panel, -1, (528, 510), choices = childList)#was (528, 510)
        self.peer4.SetSelection(0)
        """ Peer 5 """
        wx.StaticText(panel, -1, "Peer 5 List", (630, 495))
        self.peer5 = wx.Choice(panel, -1, (655, 510), choices = childList) #was (528, 510)
        self.peer5.SetSelection(0)


        """ Bid """
        bidList = ['None', 'Accept', 'Counterbid','Reject','Ignore']
        wx.StaticText(panel, -1, "Bid", (15, 540))
        self.bid = wx.Choice(panel, -1, (25, 555), choices = bidList)          
        self.bid.SetSelection(0)
        """ Bid Type """
        bidTypeList = ['None', 'Acquisition', 'Relinquish', 'Maintain', 'Mutual', 'No Resource']
        wx.StaticText(panel, -1, "Bid Type", (15, 590))
        self.bidType = wx.Choice(panel, -1, (25, 605), choices = bidTypeList)          
        self.bidType.SetSelection(0)
        """ Bid Direction """
        bidDirectList = ['None', '1', '2']
        wx.StaticText(panel, -1, "Bid Direction", (15, 640))
        self.bidDirect = wx.Choice(panel, -1, (25, 655), choices = bidDirectList)          
        self.bidDirect.SetSelection(0)

        """ Area Peers """
        text = StaticText(panel, -1, "Area Peers", (130, 555))
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
        text.SetFont(font)
        """ Area Peer 1 """
        wx.StaticText(panel, -1, "Area Peer 1", (230, 535))
        self.areaPeer1 = wx.Choice(panel, -1, (228, 550), choices = childList)
        self.areaPeer1.SetSelection(0)
        """ Area Peer 2 """      
        wx.StaticText(panel, -1, "Area Peer 2", (330, 535))
        self.areaPeer2 = wx.Choice(panel, -1, (328, 550), choices = childList)
        self.areaPeer2.SetSelection(0)
        """ Area Peer 3 """
        wx.StaticText(panel, -1, "Area Peer 3", (430, 535))
        self.areaPeer3 = wx.Choice(panel, -1, (428, 550), choices = childList)
        self.areaPeer3.SetSelection(0)
        """ Area Peer 4 """
        wx.StaticText(panel, -1, "Area Peer 4", (530, 535))
        self.areaPeer4 = wx.Choice(panel, -1, (528, 550), choices = childList)
        self.areaPeer4.SetSelection(0)
        """ Area Peer 5 """
        wx.StaticText(panel, -1, "Area Peer 5", (630, 535))
        self.areaPeer5 = wx.Choice(panel, -1, (628, 550), choices = childList)
        self.areaPeer5.SetSelection(0)

        """ Attending """   
        self.attend = wx.CheckBox(panel, -1, "Attending", (130, 590),(85, 20), wx.NO_BORDER)        
        """ Attending Peer 1 """
        wx.StaticText(panel, -1, "Attending Peer 1", (230, 575))
        self.attendPeer1 = wx.Choice(panel, -1, (228, 590), choices = childList)
        self.attendPeer1.SetSelection(0)
        """ Attending Peer 2 """      
        wx.StaticText(panel, -1, "Attending Peer 2", (330, 575))
        self.attendPeer2 = wx.Choice(panel, -1, (328, 590), choices = childList)
        self.attendPeer2.SetSelection(0)
        """ Attending Peer 3 """ 
        wx.StaticText(panel, -1, "Attending Peer 3", (430, 575))
        self.attendPeer3 = wx.Choice(panel, -1, (428, 590), choices = childList)
        self.attendPeer3.SetSelection(0)
        """ Attending Peer 4 """
        wx.StaticText(panel, -1, "Attending Peer 4", (530, 575))
        self.attendPeer4 = wx.Choice(panel, -1, (528, 590), choices = childList)
        self.attendPeer4.SetSelection(0)
        """ Attending Peer 5 """
        wx.StaticText(panel, -1, "Attending Peer 5", (630, 575))
        self.attendPeer5 = wx.Choice(panel, -1, (628, 590), choices = childList)
        self.attendPeer5.SetSelection(0)


        """ Referencing """
        self.reference = wx.CheckBox(panel, -1, "Referencing", (130, 630),(85, 20), wx.NO_BORDER)
        """ Reference Peer 1 """
        wx.StaticText(panel, -1, "Reference Peer 1", (230, 615))
        self.referPeer1 = wx.Choice(panel, -1, (228, 630), choices = childList)
        self.referPeer1.SetSelection(0)
        """ Reference Peer 2 """      
        wx.StaticText(panel, -1, "Reference Peer 2", (330, 615))
        self.referPeer2 = wx.Choice(panel, -1, (328, 630), choices = childList)
        self.referPeer2.SetSelection(0)
        """ Reference Peer 3 """ 
        wx.StaticText(panel, -1, "Reference Peer 3", (430, 615))
        self.referPeer3 = wx.Choice(panel, -1, (428, 630), choices = childList)
        self.referPeer3.SetSelection(0)
        """ Reference Peer 4 """
        wx.StaticText(panel, -1, "Reference Peer 4", (530, 615))
        self.referPeer4 = wx.Choice(panel, -1, (528, 630), choices = childList)
        self.referPeer4.SetSelection(0)
        """ Reference Peer 5 """
        wx.StaticText(panel, -1, "Reference Peer 5", (630, 615))
        self.referPeer5 = wx.Choice(panel, -1, (628, 630), choices = childList)
        self.referPeer5.SetSelection(0)     

        """ Coercion """
        self.coercion = wx.CheckBox(panel, -1, "Coercion", (130, 670),(85, 20), wx.NO_BORDER)
        """ Coercion Peer 1 """
        wx.StaticText(panel, -1, "Coercion Peer 1", (230, 655))
        self.coercionPeer1 = wx.Choice(panel, -1, (228, 670), choices = childList)
        self.coercionPeer1.SetSelection(0)
        """ Coercion Peer 2 """      
        wx.StaticText(panel, -1, "Coercion Peer 2", (330, 655))
        self.coercionPeer2 = wx.Choice(panel, -1, (328, 670), choices = childList)
        self.coercionPeer2.SetSelection(0)
        """ Coercion Peer 3 """ 
        wx.StaticText(panel, -1, "Coercion Peer 3", (430, 655))
        self.coercionPeer3 = wx.Choice(panel, -1, (428, 670), choices = childList)
        self.coercionPeer3.SetSelection(0)
        """ Coercion Peer 4 """
        wx.StaticText(panel, -1, "Coercion Peer 4", (530, 655))
        self.coercionPeer4 = wx.Choice(panel, -1, (528, 670), choices = childList)
        self.coercionPeer4.SetSelection(0)
        """ Coercion Peer 5 """
        wx.StaticText(panel, -1, "Coercion Peer 5", (630, 655))
        self.coercionPeer5 = wx.Choice(panel, -1, (628, 670), choices = childList)
        self.coercionPeer5.SetSelection(0)

        """ Initiation Outcome """
        initiationOutList = ['None', 'Successful', 'Unsuccessful']
        wx.StaticText(panel, -1, "Initiation Outcome", (130, 329))
        self.initiationOut = wx.Choice(panel, -1, (128, 341), choices = initiationOutList)          
        self.initiationOut.SetSelection(0)
        """ Initiation Peers """
        text = StaticText(panel, -1, "Initiation Peers", (130, 715))
        font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
        text.SetFont(font)
        """ Initiation Peer 1 """
        wx.StaticText(panel, -1, "Initiation Peer 1", (230, 695))
        self.initiationPeer1 = wx.Choice(panel, -1, (228, 710), choices = childList)
        self.initiationPeer1.SetSelection(0)
        """ Initiation Peer 2 """      
        wx.StaticText(panel, -1, "Initiation Peer 2", (330, 695))
        self.initiationPeer2 = wx.Choice(panel, -1, (328, 710), choices = childList)
        self.initiationPeer2.SetSelection(0)
        """ Initiation Peer 3 """ 
        wx.StaticText(panel, -1, "Initiation Peer 3", (430, 695))
        self.initiationPeer3 = wx.Choice(panel, -1, (428, 710), choices = childList)
        self.initiationPeer3.SetSelection(0)
        """ Initiation Peer 4 """
        wx.StaticText(panel, -1, "Initiation Peer 4", (530, 695))
        self.initiationPeer4 = wx.Choice(panel, -1, (528, 710), choices = childList)
        self.initiationPeer4.SetSelection(0)
        """ Initiation Peer 5 """
        wx.StaticText(panel, -1, "Initiation Peer 5", (630, 695))
        self.initiationPeer5 = wx.Choice(panel, -1, (628, 710), choices = childList)
        self.initiationPeer5.SetSelection(0)

        """ Manipulate Data and Store: Buttons """                

        errCheck = wx.Button(panel, -1, "Error Check", (800, 55)) 
        self.Bind(wx.EVT_BUTTON, self.OnErrorCheck, errCheck)     # Uses OnErrorCheck     
        errCheck.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))        
        errCheck.SetBackgroundColour("Black")
        errCheck.SetForegroundColour("Yellow")
        errCheck.SetToolTipString("Error Check")
        errCheck.SetSize(errCheck.GetBestSize())

        done = wx.Button(panel, -1, "Submit Data", (800, 121))
        self.Bind(wx.EVT_BUTTON, self.OnComplete, done)     # Uses OnComplete     
        done.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))        
        done.SetBackgroundColour("Black")
        done.SetForegroundColour("Yellow")
        done.SetToolTipString("Compile event data")
        done.SetSize(done.GetBestSize()) 

        ano = wx.Button(panel, -1, "Another Event", (800, 182))
        self.Bind(wx.EVT_BUTTON, self.OnAnother, ano)       #Uses OnAnother       
        ano.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False)) 
        ano.SetForegroundColour('Yellow')
        ano.SetToolTipString("Refresh entry values")
        ano.SetSize(ano.GetBestSize())
        ano.SetBackgroundColour('Black')

        q = wx.Button(panel, -1, "Quit", (800, 550))
        self.Bind(wx.EVT_BUTTON, self.OnClose, q)           #Uses OnClose
        q.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD, False))        
        q.SetBackgroundColour("Red")
        q.SetForegroundColour(wx.BLACK)
        q.SetToolTipString("This exits the program...")
        q.SetSize(q.GetBestSize())       

        wx.StaticText(panel, -1, "Timer", (210,35))
        dPro = bitPALsMaps.getS_accurate_clockBitmap()  #converted prior
        #dPro = wx.Bitmap("S_accurate_clock.bmp")
        dProGet = buttons.GenBitmapButton(panel, -1, dPro,\
                                          (165, 50), style = 1)
        self.Bind(wx.EVT_BUTTON, self.OnButtondPro, dProGet)


        """ Manipulate Data and Store: Methods """

    def OnButtondPro(self, evt):
        """ Find local wav files """
        self.sound1 = wx.Sound(r'./sounds/mid.wav') #local
        self.sound2 = wx.Sound(r'./sounds/end.wav') 
        #self.sound1 = wx.Sound(r'C:\Windows\Media\notify.wav') #
        #self.sound2 = wx.Sound(r'C:\Windows\Media\ding.wav')
        max = 10
        dlg = wx.ProgressDialog("Observation Interval", "Seconds",
                                maximum = max, parent=self,style = wx.PD_AUTO_HIDE
                                |wx.PD_APP_MODAL
                                |wx.PD_ELAPSED_TIME
                                |wx.PD_REMAINING_TIME)
        keepGoing = True
        count = 0
        while keepGoing and count < max:            
            count += 1
            wx.Sleep(1)
            if count == (max / 2):
                keepGoing = dlg.Update(count, "Half!")
                wx.Sound.Play(self.sound1)  
            else:
                keepGoing = dlg.Update(count)
            if count == max: 
                wx.Sound.Play(self.sound2)
        dlg.Destroy()

    def OnClose(self, event):       
        self.Destroy()          


    def OnErrorCheck(self, evt):
        """ data entries; 'None' added to begin with 1 - easier for counting """  
        global errorReview
        # use these taskList numbers to construct error rules for taskList
                    # None
                    #1. Affection,
                    #2. Art,
                    #3. Board Games,
                    #4. Circle Time,
                    #5. Clean Up 
                    #6. Computer
                    #7. Conflict
                    #8. Digging
                    #9. Figure play 
                    #10. Instruction 
                    #11. Instrumental Help 
                    #12. Language Arts 
                    #13. Large motor 
                    #14. Manipulatives 
                    #15. Math/ Science
                    #16. Molding 
                    #17. Music/Singing
                    #18. Onlooking 
                    #19. Other
                    #20. Physical Games 
                    #21. Pretend Play 
                    #22. Problem Solve
                    #23. Sensory Play
                    #24. Snack
                    #25. Talk 
                    #26. Unoccupied
                    #27. Walking
                    #28. Non-directed Physical
                    #29. Animal Obs

        retrieveDataEntries = \
                            ['None',
                             self.event.GetSelection(),            #1        
                             self.coderID.GetSelection(),          #2
                             self.child.GetSelection(),            #3
                             self.childAdvail.GetSelection(),      #4
                             self.playStructure.GetSelection(),    #5
                             self.playLocation.GetSelection(),     #6
                             self.behaviorType.GetSelection(),     #7
                             self.ifTeachAvail.GetSelection(),     #8
                             self.ifTeacher.GetSelection(),        #9
                             self.taskList.GetSelection(),         #10- see above                             
                             self.affectList.GetSelection(),       #11
                             self.affectDirectList.GetSelection(), #12
                             self.affectIntenseList.GetSelection(),#13
                             self.peer1.GetSelection(),            #14
                             self.peer1Affect.GetSelection(),      #15
                             self.peer1Direction.GetSelection(),   #16
                             self.peer1Intensity.GetSelection(),   #17
                             self.peer2.GetSelection(),            #18
                             self.peer3.GetSelection(),            #19
                             self.peer4.GetSelection(),            #20
                             self.peer5.GetSelection(),            #21
                             self.areaPeer1.GetSelection(),        #22
                             self.areaPeer2.GetSelection(),        #23
                             self.areaPeer3.GetSelection(),        #24
                             self.areaPeer4.GetSelection(),        #25
                             self.areaPeer5.GetSelection(),        #26
                             self.initiation.GetSelection(),       #27 start Individual (vs Scan)
                             self.bid.GetSelection(),              #28
                             self.bidType.GetSelection(),          #29
                             self.bidDirect.GetSelection(),        #30
                             self.teachSol.GetValue(),             #31
                             self.attend.GetValue(),                #32
                             self.attendPeer1.GetSelection(),      #33
                             self.attendPeer2.GetSelection(),      #34
                             self.attendPeer3.GetSelection(),      #35
                             self.attendPeer4.GetSelection(),      #36
                             self.attendPeer5.GetSelection(),      #37
                             self.reference.GetValue(),             #38
                             self.referPeer1.GetSelection(),       #39
                             self.referPeer2.GetSelection(),       #40
                             self.referPeer3.GetSelection(),       #41
                             self.referPeer4.GetSelection(),       #42
                             self.referPeer5.GetSelection(),       #43
                             self.coercion.GetValue(),                #44
                             self.coercionPeer1.GetSelection(),    #45
                             self.coercionPeer2.GetSelection(),    #46
                             self.coercionPeer3.GetSelection(),    #47
                             self.coercionPeer4.GetSelection(),    #48
                             self.coercionPeer5.GetSelection(),    #49
                             self.initiationOut.GetSelection(),     #50
                             self.initiationPeer1.GetSelection(),  #51
                             self.initiationPeer2.GetSelection(),  #52
                             self.initiationPeer3.GetSelection(),  #53
                             self.initiationPeer4.GetSelection(),  #54
                             self.initiationPeer5.GetSelection()]  #55

        """ Review for errors before sending """
        """for i,v in enumerate(retrieveDataEntries):  #use listingIndex.py to create          
            #print i,v

             or 
        code = []; response = []    
        for q, a in zip(code, response): print 'This is the code:response pairing %s:%s. % (q, a)
        """
        
        ############## Error Checking  ##############################
        ######################################################

        """ Coder ID Data Error """
        if retrieveDataEntries[2] == 0:
            coderIDMessage = wx.MessageBox('No CoderID Assigned',\
                                           caption = 'CoderID Needed:',\
                                           style = wx.OK, parent = self) 

        """ Child ID Data Error """   
        childN = len(childList)
        if retrieveDataEntries[3] < 1 or retrieveDataEntries[3] == childN - 1:
            childMessage = wx.MessageBox('No Child Assigned',\
                                         caption = 'Child Needed:',\
                                         style = wx.OK, parent = self) 

        """ Child Available Error """        
        if retrieveDataEntries[4] == 0:
            childMessage = wx.MessageBox('No Child Available Assigned',\
                                         caption = 'Child Availability Needed:',\
                                         style = wx.OK, parent = self)
        """ Map Data Error """        
        if retrieveDataEntries[4] > 1:
            #fill in map vector for equal length string
            emptyMaplist = (0,0,0,0,0,0,0,0,0)
            maps.append(emptyMaplist)  
            cleanList = [self.playStructure.SetSelection(0),\
                         self.playLocation.SetSelection(0),\
                         self.behaviorType.SetSelection(0),\
                         self.ifTeachAvail.SetSelection(0),\
                         self.ifTeacher.SetSelection(0),\
                         self.taskList.SetSelection(0),\
                         self.affectList.SetSelection(0),\
                         self.affectDirectList.SetSelection(0),\
                         self.affectIntenseList.SetSelection(0),\
                         self.peer1.SetSelection(0),\
                         self.peer1Affect.SetSelection(0),\
                         self.peer1Direction.SetSelection(0),\
                         self.peer1Intensity.SetSelection(0),\
                         self.peer2.SetSelection(0),\
                         self.peer3.SetSelection(0),\
                         self.peer4.SetSelection(0),\
                         self.peer5.SetSelection(0),\
                         self.areaPeer1.SetSelection(0),\
                         self.areaPeer2.SetSelection(0),\
                         self.areaPeer3.SetSelection(0),\
                         self.areaPeer4.SetSelection(0),\
                         self.areaPeer5.SetSelection(0),\
                         self.initiation.SetSelection(0),\
                         self.bid.SetSelection(0),\
                         self.bidType.SetSelection(0),\
                         self.bidDirect.SetSelection(0),\
                         self.teachSol.SetValue(0),\
                         self.attend.SetValue(0),\
                         self.attendPeer1.SetSelection(0),\
                         self.attendPeer2.SetSelection(0),\
                         self.attendPeer3.SetSelection(0),\
                         self.attendPeer4.SetSelection(0),\
                         self.attendPeer5.SetSelection(0),\
                         self.reference.SetValue(0),\
                         self.referPeer1.SetSelection(0),\
                         self.referPeer2.SetSelection(0),\
                         self.referPeer3.SetSelection(0),\
                         self.referPeer4.SetSelection(0),\
                         self.referPeer5.SetSelection(0),\
                         self.coercion.SetValue(0),\
                         self.coercionPeer1.SetSelection(0),\
                         self.coercionPeer2.SetSelection(0),\
                         self.coercionPeer3.SetSelection(0),\
                         self.coercionPeer4.SetSelection(0),\
                         self.coercionPeer5.SetSelection(0),\
                         self.initiationOut.SetSelection(0),\
                         self.initiationPeer1.SetSelection(0),\
                         self.initiationPeer2.SetSelection(0),\
                         self.initiationPeer3.SetSelection(0),\
                         self.initiationPeer4.SetSelection(0),\
                         self.initiationPeer5.SetSelection(0)]
            for each in range(len(cleanList)):
                cleanList[each]

            errorReview = 1
        else:

            if retrieveDataEntries[4] == 1:
                """ Map Assigment Complete Error """
                if len(maps) != 6:        
                    mapper = str(maps)
                    mapInfodlg = wx.MessageBox(mapper, caption = 'Error.  Re-Enter Map Assignment.', \
                                               style = wx.OK, parent = self)             
                    for eachItem in range(len(maps)):
                        maps.pop()                                      

                """ Structure Assignment Error """            
                if retrieveDataEntries[5] == 0:
                    structureMessage = wx.MessageBox('Child present but no structure assigned',\
                                                     caption = 'Error on Structure Assignment:',\
                                                     style = wx.OK, parent = self)

                """ Behavior Assignment Error """            
                if retrieveDataEntries[7] == 0:
                    behaviorMessage = wx.MessageBox('Child present but no behavior assigned',\
                                                    caption = 'Error on Behavior Assignment:',\
                                                    style = wx.OK, parent = self)  

                """ Teacher Present Assignment Error """            
                if retrieveDataEntries[8] == 0:
                    teacherPresMessage = wx.MessageBox('Child present but no teacher presence assigned',\
                                                       caption = 'Error on Teacher Presence Assignment:',\
                                                       style = wx.OK, parent = self)  

                """ Task Assignment Error """            
                if retrieveDataEntries[10] == 0:
                    taskMessage = wx.MessageBox('Child present but no task assigned',\
                                                caption = 'Error on Task Assignment:',\
                                                style = wx.OK, parent = self)  
                if retrieveDataEntries[10] == 1 \
                   or retrieveDataEntries[10] == 7\
                   or retrieveDataEntries[10] == 10\
                   or retrieveDataEntries[10] == 11\
                   or retrieveDataEntries[10] == 22:
                    if retrieveDataEntries[7] < 3:
                        taskMessage = wx.MessageBox('Task: Social or Teach Orient',\
                                                    caption = 'Social or Teacher Orient:',\
                                                    style = wx.OK, parent = self)    

                """ Affect & Intensity Assignment """           
                if retrieveDataEntries[11] == 0:
                    affectMessage = wx.MessageBox('Child present but no affect assigned',\
                                                  caption = 'Error on Affect Assignment:',\
                                                  style = wx.OK, parent = self)
                if retrieveDataEntries[11] > 0:                  # affect
                    if retrieveDataEntries[11] == 1:             # affect== Pos
                        if retrieveDataEntries[13] != 2 and \
                           retrieveDataEntries[13] != 3 and \
                           retrieveDataEntries[13] != 4:         # intensity 
                            intensityRangeMessage = wx.MessageBox('Affect present but intensity is out of range',\
                                                                  caption = 'Error #1 on Intensity Assignment:',\
                                                                  style = wx.OK, parent = self) 
                    if retrieveDataEntries[11] == 2:             # affect== Neutral
                        self.affectIntenseList.SetSelection(1)       
                    if retrieveDataEntries[11] == 3:             # affect== Negative
                        if retrieveDataEntries[13] != 2 and \
                           retrieveDataEntries[13] != 3 and \
                           retrieveDataEntries[13] != 4:         # intensity  
                            intensityRangeMessage = wx.MessageBox('Affect present but intensity is out of range',\
                                                                  caption = 'Error #2 on Intensity Assignment:',\
                                                                  style = wx.OK, parent = self)  
                    if retrieveDataEntries[11] == 4:             # affect== Unseen
                        self.affectIntenseList.SetSelection(5)  
                """ Solitary or Parallel: No Direction """        
                if retrieveDataEntries[7] == 1:
                    self.peer1Direction.SetSelection(0)
                    self.affectDirectList.SetSelection(0)
                    if retrieveDataEntries[10] != 18:
                        self.peer1.SetSelection(0)
                        self.peer2.SetSelection(0)
                        self.peer3.SetSelection(0)
                        self.peer4.SetSelection(0)
                        self.peer5.SetSelection(0)

                """ No Peer Assignment Error """  
                if retrieveDataEntries[14] == 0:                 # no peer 1
                    """ Onlooking Error """
                    if retrieveDataEntries[7] == 1 and retrieveDataEntries[10] == 18:  #solitary & onlook
                        onlookNoPeerMessage = wx.MessageBox('Onlooking but no peer selected',\
                                                            caption = 'Onlooking But No Peer: ',\
                                                            style = wx.OK, parent = self) 
                    if retrieveDataEntries[7] == 2: 
                        parallelNoPeerMessage = wx.MessageBox('Parallel but no peer selected',\
                                                              caption = 'Parallel But No Peer: ',\
                                                              style = wx.OK, parent = self)    
                    if retrieveDataEntries[7] == 3:              # beh == social
                        socialNoPeerMessage = wx.MessageBox('Social play but no peer selected',\
                                                            caption = 'Social But No Peer: ',\
                                                            style = wx.OK, parent = self)  


                """ Parallel with Peer: Direction """        
                if retrieveDataEntries[14] != 0:                 # peer 
                    if retrieveDataEntries[7] == 2:              # beh == parallel
                        self.peer1Direction.SetSelection(0)
                        self.affectDirectList.SetSelection(0)

                """ Social But No Peer """         
                if retrieveDataEntries[14] != 0:                 # peer                                            
                    if retrieveDataEntries[18] == 0:
                        if retrieveDataEntries[7] == 3:          # beh == social
                            if retrieveDataEntries[12] == 0:
                                teacherRoleMessage = wx.MessageBox('Social play but no direction given',\
                                                                   caption = 'Social But No Target Direction: ',\
                                                                   style = wx.OK, parent = self)
                            if retrieveDataEntries[14] == 0:
                                teacherRoleMessage = wx.MessageBox('Social play but no direction given',\
                                                                   caption = 'Social But No Peer1 Direction: ',\
                                                                   style = wx.OK, parent = self)    
                """ Peer2 so No Peer1 Direction """
                if retrieveDataEntries[7] == 3:                    
                    if retrieveDataEntries[14] != 0 and retrieveDataEntries[18] != 0:
                        # Social with Peer 1 & Peer 2
                        self.affectDirectList.SetSelection(0)
                        self.peer1Affect.SetSelection(0)
                        self.peer1Direction.SetSelection(0)
                        self.peer1Intensity.SetSelection(0)

                """ No Direction for Target & Peer with Parallel """   
                if retrieveDataEntries[7] == 2:                  # Parallel 
                    if retrieveDataEntries[18] == 0:             # No peer 2
                        if retrieveDataEntries[14] != 0:         # Peer 1
                            self.affectDirectList.SetSelection(0)
                            self.peer1Direction.SetSelection(0) 
                        if retrieveDataEntries[15] == 0: 
                            peer1affectMessage = wx.MessageBox('Need Peer1 Affect',\
                                                               caption = 'Provide Peer1 Affect:',\
                                                               style = wx.OK, parent = self) 
                        if retrieveDataEntries[17] == 0: 
                            peer1affectMessage = wx.MessageBox('Need Peer1 Intensity',\
                                                               caption = 'Provide Peer1 Intensity:',\
                                                               style = wx.OK, parent = self)    
                ### added 1/1/08 ###   #modified for no peer 2 on 1/13/08         
                """ No Affect or Intensity Assignment Error """   
                if retrieveDataEntries[7] == 1:                  # beh = solitary
                    # onlooking; no peer 2
                    if retrieveDataEntries[10] == 18 and retrieveDataEntries[18] == 0: 
                        #assumes that peer 1 is present; error caught above
                        if retrieveDataEntries[15] == 0:         # Peer 1 affect
                            socialPeerAffectMessage = wx.MessageBox('Onlooking: Need Affect: Peer 1',\
                                                   caption = 'No Affect for Peer 1 Recorded:',\
                                                   style = wx.OK, parent = self)
                        if retrieveDataEntries[17] == 0:         # Peer 1 intensity
                            socialPeerIntensityMessage = wx.MessageBox('Onlooking: Need Intensity: Peer 1',\
                                                   caption = 'No Intensity for Peer 1 Recorded:',\
                                                   style = wx.OK, parent = self) 
                #################################################################   
                """ No Affect or Intensity Assignment Error """   
                if retrieveDataEntries[7] == 3:                  # beh = social
                    if retrieveDataEntries[18] == 0:             # peer 2 = none
                        if retrieveDataEntries[14] != 0:         # Peer 1
                            if retrieveDataEntries[12] == 0:     # Target needs Direction
                                affectT_DirectMessage = wx.MessageBox('Need Direction: Target',\
                                                                      caption = 'No Direction for Target:',\
                                                                      style = wx.OK, parent = self) 
                            if retrieveDataEntries[15] == 0:     # Peer 1 affect
                                socialPeerAffectMessage = wx.MessageBox('Need Affect: Peer 1',\
                                                                        caption = 'No Affect for Peer 1 Recorded:',\
                                                                        style = wx.OK, parent = self)
                            if retrieveDataEntries[16] == 0:     # Peer 1 direction
                                socialPeerAffectMessage = wx.MessageBox('Need Direction: Peer 1',\
                                                                        caption = 'No Direction for Peer 1 Recorded:',\
                                                                        style = wx.OK, parent = self)    
                            if retrieveDataEntries[17] == 0:     # Peer 1 intensity
                                socialPeerIntensityMessage = wx.MessageBox('Need Intensity: Peer 1',\
                                                                           caption = 'No Intensity for Peer 1 Recorded:',\
                                                                           style = wx.OK, parent = self) 
                """ Teacher Role """
                if retrieveDataEntries[7] == 4:                  # Teacher Oriented
                    self.peer1Direction.SetSelection(0)
                    if retrieveDataEntries[9] == 0:
                        teacherRoleMessage = wx.MessageBox('Teacher Role',\
                                                           caption = 'Teacher Needs Role Assignment: ',\
                                                           style = wx.OK, parent = self)    
                    """if retrieveDataEntries[12] == 0:
                        affectDirectionMessage = wx.MessageBox('T_Direction Assignment',\
                                                   caption = 'T_Direction Needed: ',\
                                                   style = wx.OK, parent = self)"""         
                """ Teacher Not Involved """
                if retrieveDataEntries[7] != 0 and retrieveDataEntries[7] != 4:
                    self.ifTeacher.SetSelection(0)

                """ Peer 2 Consequences """    
                """ Affect Peer 1 Restrictions """                 
                if retrieveDataEntries[15] == 4:           # peer1 affect = unseen
                    self.peer1Intensity.SetSelection(5)    # unseen intensity
                if retrieveDataEntries[15] == 2:           # peer1 affect = neutral
                    self.peer1Intensity.SetSelection(1)    # netural none   
                if retrieveDataEntries[15] == 1 or retrieveDataEntries[15] == 3:
                    if retrieveDataEntries[17] == 5 or retrieveDataEntries[17] < 2:
                        intensityPeer1Message = wx.MessageBox('Intensity Adjustment: Peer1',\
                                                              caption = 'Intensity Needs Proper Assignment: ',\
                                                              style = wx.OK, parent = self)
                """ Target Direction/Peer1 Direction """ 
                if retrieveDataEntries[12] == 0 and retrieveDataEntries[7] == 4: 
                    if retrieveDataEntries[10] != 18: 
                        targetDirectTeachMessage = wx.MessageBox('Target Direction Error: Teacher',\
                                                                 caption = 'Assign Target Direction: Teacher: ',\
                                                                 style = wx.OK, parent = self)
                if retrieveDataEntries[12] != 0 and retrieveDataEntries[7] == 4: 
                    if retrieveDataEntries[10] == 18:
                        self.affectDirectList.SetSelection(0)

                if retrieveDataEntries[14] != 0 and retrieveDataEntries[18] == 0:                    
                    if retrieveDataEntries[7] != 1: 
                        if retrieveDataEntries[15] == 0:
                            peer1DirectMessage = wx.MessageBox('Peer 1 Affect Error:',\
                                                               caption = 'Peer 1 Affect: ',\
                                                               style = wx.OK, parent = self)
                        if retrieveDataEntries[17] == 0:
                            peer1DirectMessage = wx.MessageBox('Peer 1 Intensity Error:',\
                                                               caption = 'Peer 1 Intensity: ',\
                                                               style = wx.OK, parent = self)        

                if retrieveDataEntries[12] == 1 and retrieveDataEntries[16] == 1:
                    sameDirectMessage = wx.MessageBox('Directions are Same Error:',\
                                                      caption = 'Same Target & Peer Direction: ',\
                                                      style = wx.OK, parent = self)
                if retrieveDataEntries[12] == 2 and retrieveDataEntries[16] == 2:
                    sameDirectMessage = wx.MessageBox('Directions are Same Error:',\
                                                      caption = 'Same Target & Peer Direction: ',\
                                                      style = wx.OK, parent = self)     
                if retrieveDataEntries[12] == 3: 
                    self.peer1Direction.SetSelection(3)      
                if retrieveDataEntries[16] == 3: 
                    self.affectDirectList.SetSelection(3) 
                if retrieveDataEntries[14] != 0 and retrieveDataEntries[18] != 0: 
                    self.peer1Intensity.SetSelection(0) 
                    self.peer1Direction.SetSelection(0)
                    self.peer1Affect.SetSelection(0)
                    if retrieveDataEntries[7] != 4:
                        self.affectDirectList.SetSelection(0)



                """ Peer1 Affect Unseen; Intensity unseen """       
                if retrieveDataEntries[15] == 4:            # Affect Peer1 Unseen
                    self.peer1Intensity.SetSelection(5)     # Unseen   
                """ Peer Assigment errors """    
                if retrieveDataEntries[10] == 18:           # onlook 
                    if retrieveDataEntries[7] == 1 and retrieveDataEntries[14] == 0:
                        self.peer1Direction.SetSelection(0)
                        self.affectDirectList.SetSelection(0)
                        onlookPeerMessage = wx.MessageBox('Onlooking Solitary without Peer',\
                                                          caption = 'Onlooking Solitary: Assign Peer: ',\
                                                          style = wx.OK, parent = self) 
                if retrieveDataEntries[10] == 18:           # onlook 
                    if retrieveDataEntries[14] != 0:
                        if retrieveDataEntries[7] == 2 or retrieveDataEntries[7] == 3: #social, parallel
                            onlookSolMessage = wx.MessageBox('Onlooking with Peer: Teacher, Solitary',\
                                                             caption = 'Onlooking & Peer: Assign Solitary or Teacher: ',\
                                                             style = wx.OK, parent = self)  
                if retrieveDataEntries[18] != 0:            # peer2 selected
                    if retrieveDataEntries[14] == 0:
                        peer1MissingMessage = wx.MessageBox('Peer1 Assignment Error',\
                                                            caption = 'Peer1 Not Assigned: ',\
                                                            style = wx.OK, parent = self) # peer3 selected
                if retrieveDataEntries[19] != 0: 
                    if retrieveDataEntries[18] == 0:
                        peer2MissingMessage = wx.MessageBox('Peer2 Assignment Error',\
                                                            caption = 'Peer2 Not Assigned: ',\
                                                            style = wx.OK, parent = self)  
                if retrieveDataEntries[20] != 0:            # peer4 selected
                    if retrieveDataEntries[19] == 0:
                        peer3MissingMessage = wx.MessageBox('Peer3 Assignment Error',\
                                                            caption = 'Peer3 Not Assigned: ',\
                                                            style = wx.OK, parent = self)   
                if retrieveDataEntries[21] != 0:            # peer5 selected
                    if retrieveDataEntries[20] == 0:
                        peer4MissingMessage = wx.MessageBox('Peer4 Assignment Error',\
                                                            caption = 'Peer4 Not Assigned: ',\
                                                            style = wx.OK, parent = self)
                """ Begin Group Rules """       
                if retrieveDataEntries[28] != 0:   #Bid must be social
                    self.behaviorType.SetSelection(3)
                    if retrieveDataEntries[29] == 0:
                        bidTypeMessage = wx.MessageBox('Bid Type Error',\
                                                       caption = 'Bid Type Not Assigned: ',\
                                                       style = wx.OK, parent = self)
                    if retrieveDataEntries[30] == 0:
                        bidDirectMessage = wx.MessageBox('Bid Direction Error',\
                                                         caption = 'Bid Direction Not Assigned: ',\
                                                         style = wx.OK, parent = self)

                if retrieveDataEntries[27] != 0 and retrieveDataEntries[50] == 0:
                    initiationOutcomeMessage = wx.MessageBox('Initiation Outcome Error',\
                                                             caption = 'Initiation Outcome Needed: ',\
                                                             style = wx.OK, parent = self)      #Initiation outcome
                if retrieveDataEntries[27] != 0 and retrieveDataEntries[51] == 0:
                    initiationPeerMessage = wx.MessageBox('Initiation Peer Error',\
                                                          caption = 'Initiation Peer Needed: ',\
                                                          style = wx.OK, parent = self)  #Initiation peer
                if retrieveDataEntries[27] == 0 and retrieveDataEntries[51] != 0: 
                    initiationMessage = wx.MessageBox('Initiation Error',\
                                                      caption = 'Initiation Needed: ',\
                                                      style = wx.OK, parent = self)  #Initiation needed
                #if retrieveDataEntries[32] == 1 and retrieveDataEntries[7] != 3:   
                    #attendSocialMessage = wx.MessageBox('Attending Social Error',\
                                                    #caption = 'Social Behavior Needed: ',\
                                                    #style = wx.OK, parent = self)  #attending Social
                if retrieveDataEntries[44] == 1 and retrieveDataEntries[7] != 3:   
                    coercionSocialMessage = wx.MessageBox('Coercion Social Error',\
                                                          caption = 'Social Behavior Needed: ',\
                                                          style = wx.OK, parent = self)  #coercion Social  
                if retrieveDataEntries[38] != 0 and retrieveDataEntries[39] == 0:
                    referencePeerMessage = wx.MessageBox('Reference Peer Error',\
                                                         caption = 'Reference Peer Needed: ',\
                                                         style = wx.OK, parent = self)  #Reference peer
                if retrieveDataEntries[38] == 0 and retrieveDataEntries[39] != 0: 
                    referenceMessage = wx.MessageBox('Reference Error',\
                                                     caption = 'Reference Needed: ',\
                                                     style = wx.OK, parent = self)  #Reference needed


                """ Maps Location consistent with selection """        
                if maps[0] > 3:
                    self.playLocation.SetSelection(1)
                else:    
                    self.playLocation.SetSelection(2)
                print 'maps 0 = ', maps[0]    
                if maps[2] > 3:
                    self.playLocation.SetSelection(1)
                else:    
                    self.playLocation.SetSelection(2)   
                print 'maps 2 = ', maps[2]    
                if maps[4] > 3:
                    self.playLocation.SetSelection(1)
                else:    
                    self.playLocation.SetSelection(2)
                print 'maps 4 = ', maps[4]    
                #############################################################
                #############################################################
                p1,p2,p3,p4,p5 = retrieveDataEntries[14],retrieveDataEntries[18],\
                  retrieveDataEntries[19],retrieveDataEntries[20],retrieveDataEntries[21]  

                ap1,ap2,ap3,ap4,ap5 = retrieveDataEntries[22],retrieveDataEntries[23],\
                   retrieveDataEntries[24],retrieveDataEntries[25],retrieveDataEntries[26]

                atp1,atp2,atp3,atp4,atp5 = retrieveDataEntries[33],retrieveDataEntries[34],\
                    retrieveDataEntries[35],retrieveDataEntries[36],retrieveDataEntries[37]

                rp1,rp2,rp3,rp4,rp5 = retrieveDataEntries[39],retrieveDataEntries[40],\
                   retrieveDataEntries[41],retrieveDataEntries[42],retrieveDataEntries[43]  

                cp1,cp2,cp3,cp4,cp5 = retrieveDataEntries[45],retrieveDataEntries[46],\
                   retrieveDataEntries[47],retrieveDataEntries[48],retrieveDataEntries[49]

                ip1,ip2,ip3,ip4,ip5 = retrieveDataEntries[51],retrieveDataEntries[52],\
                   retrieveDataEntries[53],retrieveDataEntries[54],retrieveDataEntries[55]
                
                # Entry errors for peer
                peer = retrieveDataEntries[14]
                pentries = [peer,p2,p3,p4,p5,ap1,ap2,ap3,ap4,ap5]             
                
                # peer in multiple peer slots
                multiEntries =[]
                for entry in range(len(pentries)):
                    if pentries[entry] != 0: 
                        if pentries.count(pentries[entry]) > 1: 
                            multiEntries.append(pentries.count(pentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Peer Listed - Multiple',\
                                       caption = 'Double Listing Of Child: ',\
                                       style = wx.OK, parent = self) 
                    multiEntries =[] 
                ##########################################################               
                # target in peer slots
                target = retrieveDataEntries[3]                
                tentries = [p1,p2,p3,p4,p5,\
                           ap1,ap2,ap3,ap4,ap5,\
                           atp1,atp2,atp3,atp4,atp5,\
                           rp1,rp2,rp3,rp4,rp5,\
                           cp1,cp2,cp3,cp4,cp5,\
                           ip1,ip2,ip3,ip4,ip5] 
                
                for each in range(len(tentries)):
                    if tentries[each] == target:                        
                        subjectListedTwiceMessage = wx.MessageBox('Target Listed - Multiple',\
                                                              caption = 'Double Listing Of Target: ',\
                                                              style = wx.OK, parent = self)    
                ##############################################################
                # errors for assorted peer categories
                apentries = [ap1,ap2,ap3,ap4,ap5]
                multiEntries =[]
                for entry in range(len(apentries)):
                    if apentries[entry] != 0: 
                        if apentries.count(apentries[entry]) > 1: 
                            multiEntries.append(apentries.count(apentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Area Peer Listed - Multiple',\
                                                              caption = 'Double Listing Of Child: ',\
                                                              style = wx.OK, parent = self) 
                    multiEntries =[] 
                ############################################################    
                atentries = [atp1,atp2,atp3,atp4,atp5]
                multiEntries =[]
                for entry in range(len(atentries)):
                    if atentries[entry] != 0: 
                        if atentries.count(atentries[entry]) > 1: 
                            multiEntries.append(atentries.count(atentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Attending Peer Listed - Multiple',\
                                                              caption = 'Double Listing Of Child: ',\
                                                              style = wx.OK, parent = self) 
                    multiEntries =[] 
                ##############################################################
                rpentries = [rp1,rp2,rp3,rp4,rp5]
                multiEntries =[]
                for entry in range(len(rpentries)):
                    if rpentries[entry] != 0: 
                        if rpentries.count(rpentries[entry]) > 1: 
                            multiEntries.append(rpentries.count(rpentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Reference Peer Listed - Multiple',\
                                                              caption = 'Double Listing Of Child: ',\
                                                              style = wx.OK, parent = self) 
                    multiEntries =[] 
                ###############################################################
                cpentries = [cp1,cp2,cp3,cp4,cp5]
                multiEntries =[]
                for entry in range(len(cpentries)):
                    if cpentries[entry] != 0: 
                        if cpentries.count(cpentries[entry]) > 1: 
                            multiEntries.append(cpentries.count(cpentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Coercion Peer Listed - Multiple',\
                                                              caption = 'Double Listing Of Child: ',\
                                                              style = wx.OK, parent = self) 
                    multiEntries =[] 
                ############################################################
                ipentries = [ip1,ip2,ip3,ip4,ip5]
                multiEntries =[]
                for entry in range(len(ipentries)):
                    if ipentries[entry] != 0: 
                        if ipentries.count(ipentries[entry]) > 1: 
                            multiEntries.append(ipentries.count(ipentries[entry]))
                if len(multiEntries) > 0:
                    subjectListedTwiceMessage = wx.MessageBox('Initiation Peer Listed - Multiple',\
                                                              caption = 'Double Listing Of Child: ',\
                                                              style = wx.OK, parent = self) 
                    multiEntries =[] 
                ############################################################################# 
                #############################################################################  

            errorReview = 1

        return errorReview


    def OnComplete(self, evt): 
        """ Collect data; post to dialog - approve and send """
        global errorReview
        eventVector = []
        #print errorReview
        if errorReview != 1:
            dataSubdlg = wx.MessageBox('Please Submit Error Checking', caption = 'Error Status', \
                                       style = wx.OK, parent = self) 
        else:    
            """ Insert new IDs at the end, immediately prior to 888; following the IDs, come
            3 peer and 3 toddler identifiers"""
            IDs = [000, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 888, 889, 890, 891, 892, 893]
            #childList = this is global 
            retrieveDataEntries = [self.event.GetSelection(),\
                                   self.coderID.GetSelection(), \
                                   IDs[self.child.GetSelection()],\
                                   self.childAdvail.GetSelection(),\
                                   self.playStructure.GetSelection(),\
                                   self.playLocation.GetSelection(),\
                                   self.behaviorType.GetSelection(),\
                                   self.ifTeachAvail.GetSelection(),\
                                   self.ifTeacher.GetSelection(),\
                                   self.taskList.GetSelection(),\
                                   self.affectList.GetSelection(),\
                                   self.affectDirectList.GetSelection(),\
                                   self.affectIntenseList.GetSelection(),\
                                   IDs[self.peer1.GetSelection()],\
                                   self.peer1Affect.GetSelection(),\
                                   self.peer1Direction.GetSelection(),\
                                   self.peer1Intensity.GetSelection(),\
                                   IDs[self.peer2.GetSelection()],\
                                   IDs[self.peer3.GetSelection()], \
                                   IDs[self.peer4.GetSelection()], \
                                   IDs[self.peer5.GetSelection()],\
                                   IDs[self.areaPeer1.GetSelection()],\
                                   IDs[self.areaPeer2.GetSelection()],\
                                   IDs[self.areaPeer3.GetSelection()],\
                                   IDs[self.areaPeer4.GetSelection()],\
                                   IDs[self.areaPeer5.GetSelection()],\
                                   self.initiation.GetSelection(),\
                                   self.bid.GetSelection(),\
                                   self.bidType.GetSelection(),\
                                   self.bidDirect.GetSelection(),\
                                   self.teachSol.GetValue(),\
                                   self.attend.GetValue(),\
                                   IDs[self.attendPeer1.GetSelection()],\
                                   IDs[self.attendPeer2.GetSelection()],\
                                   IDs[self.attendPeer3.GetSelection()],\
                                   IDs[self.attendPeer4.GetSelection()],\
                                   IDs[self.attendPeer5.GetSelection()],\
                                   self.reference.GetValue(),\
                                   IDs[self.referPeer1.GetSelection()],\
                                   IDs[self.referPeer2.GetSelection()],\
                                   IDs[self.referPeer3.GetSelection()],\
                                   IDs[self.referPeer4.GetSelection()],\
                                   IDs[self.referPeer5.GetSelection()],\
                                   self.coercion.GetValue(),\
                                   IDs[self.coercionPeer1.GetSelection()],\
                                   IDs[self.coercionPeer2.GetSelection()],\
                                   IDs[self.coercionPeer3.GetSelection()],\
                                   IDs[self.coercionPeer4.GetSelection()],\
                                   IDs[self.coercionPeer5.GetSelection()],\
                                   self.initiationOut.GetSelection(),\
                                   IDs[self.initiationPeer1.GetSelection()],\
                                   IDs[self.initiationPeer2.GetSelection()],\
                                   IDs[self.initiationPeer3.GetSelection()],\
                                   IDs[self.initiationPeer4.GetSelection()],\
                                   IDs[self.initiationPeer5.GetSelection()]]

            """ Pull data sources together """        

            eventVector.extend(time.localtime()); eventVector.extend(retrieveDataEntries); eventVector.extend(maps)

            """ Send to File """
            ### use regular expression here to export without braces and brackets
            outputTxt = 'individualOut.txt'
            os.chdir('\pyObs')  # out to local directory            
            txtout = open(outputTxt,'a')
            voutInitial = eventVector
            vout = str(voutInitial[:]).strip('[]').replace(')', '').replace('(', '').replace('True','1').\
                 replace('False','0')
            txtout.write(str(vout))
            txtout.write('\n')                
            txtout.close
            """ To Excel """
            outputTxt = 'individualOut.csv'
            os.chdir('\pyObsOut')  # out to local directory   
            txtout = open(outputTxt,'a')        
            #vout = eventVector
            txtout.write(str(vout))
            txtout.write('\n')                
            txtout.close
            #print "This was sent %s"%(eventVector)
            for eachItem in range(len(maps)):
                maps.pop()

            dataSubdlg = wx.MessageBox('Data Successfully Submitted', caption = 'Data Status', \
                                       style = wx.OK, parent = self) 

            """ reset errorCount for next observation """
            errorReview = 0
            return errorReview

    def OnAnother(self, evt): 
        """ Refresh all entries; increment event number and keep coder ID the same """

        nxtEvent = self.event.GetSelection()+1
        dataEntries = [self.event.ClearBackground(),self.event.Refresh(),self.event.SetSelection(nxtEvent),\
                       self.coderID.ClearBackground(),self.coderID.Refresh(),\
                       self.child.ClearBackground, self.child.SetSelection(0),\
                       self.child.Refresh(), self.child.SetFocus(),\
                       self.childAdvail.ClearBackground(),self.childAdvail.Refresh(),self.childAdvail.SetSelection(0),\
                       self.playStructure.ClearBackground(),self.playStructure.Refresh(),self.playStructure.SetSelection(0),\
                       self.playLocation.ClearBackground(),self.playLocation.Refresh(),self.playLocation.SetSelection(0),\
                       self.behaviorType.ClearBackground(),self.behaviorType.Refresh(),self.behaviorType.SetSelection(0),\
                       self.ifTeachAvail.ClearBackground(),self.ifTeachAvail.Refresh(),self.ifTeachAvail.SetSelection(0),\
                       self.ifTeacher.ClearBackground(),self.ifTeacher.Refresh(),self.ifTeacher.SetSelection(0),\
                       self.taskList.ClearBackground(),self.taskList.Refresh(),self.taskList.SetSelection(0),\
                       self.affectList.ClearBackground(),self.affectList.Refresh(),self.affectList.SetSelection(0),\
                       self.affectDirectList.ClearBackground(),self.affectDirectList.Refresh(),self.affectDirectList.SetSelection(0),\
                       self.affectIntenseList.ClearBackground(),self.affectIntenseList.Refresh(),self.affectIntenseList.SetSelection(0),\
                       self.peer1.ClearBackground(),self.peer1.Refresh(),self.peer1.SetSelection(0),\
                       self.peer1Affect.ClearBackground(),self.peer1Affect.Refresh(),self.peer1Affect.SetSelection(0),\
                       self.peer1Direction.ClearBackground(),self.peer1Direction.Refresh(),self.peer1Direction.SetSelection(0),\
                       self.peer1Intensity.ClearBackground(),self.peer1Intensity.Refresh(),self.peer1Intensity.SetSelection(0),\
                       self.peer2.ClearBackground(),self.peer2.Refresh(),self.peer2.SetSelection(0),\
                       self.peer3.ClearBackground(),self.peer3.Refresh(),self.peer3.SetSelection(0),\
                       self.peer4.ClearBackground(),self.peer4.Refresh(),self.peer4.SetSelection(0),\
                       self.peer5.ClearBackground(),self.peer5.Refresh(),self.peer5.SetSelection(0),\
                       self.areaPeer1.ClearBackground(),self.areaPeer1.Refresh(),self.areaPeer1.SetSelection(0),\
                       self.areaPeer2.ClearBackground(),self.areaPeer2.Refresh(),self.areaPeer2.SetSelection(0),\
                       self.areaPeer3.ClearBackground(),self.areaPeer3.Refresh(),self.areaPeer3.SetSelection(0),\
                       self.areaPeer4.ClearBackground(),self.areaPeer4.Refresh(),self.areaPeer4.SetSelection(0),\
                       self.areaPeer5.ClearBackground(),self.areaPeer5.Refresh(),self.areaPeer5.SetSelection(0),\
                       self.initiation.ClearBackground(), self.initiation.Refresh(), self.initiation.SetSelection(0),\
                       self.bid.ClearBackground(), self.bid.Refresh(), self.bid.SetSelection(0),\
                       self.bidType.ClearBackground(), self.bidType.Refresh(), self.bidType.SetSelection(0),\
                       self.bidDirect.ClearBackground(),self.bidDirect.Refresh(),self.bidDirect.SetSelection(0),\
                       self.teachSol.ClearBackground(), self.teachSol.Refresh(), self.teachSol.SetValue(0),\
                       self.attend.ClearBackground(), self.attend.Refresh(), self.attend.SetValue(0),\
                       self.attendPeer1.ClearBackground(), self.attendPeer1.Refresh(), self.attendPeer1.SetSelection(0),\
                       self.attendPeer2.ClearBackground(), self.attendPeer2.Refresh(), self.attendPeer2.SetSelection(0),\
                       self.attendPeer3.ClearBackground(), self.attendPeer3.Refresh(), self.attendPeer3.SetSelection(0),\
                       self.attendPeer4.ClearBackground(), self.attendPeer4.Refresh(), self.attendPeer4.SetSelection(0),\
                       self.attendPeer5.ClearBackground(), self.attendPeer5.Refresh(), self.attendPeer5.SetSelection(0),\
                       self.reference.ClearBackground(), self.reference.Refresh(), self.reference.SetValue(0),\
                       self.referPeer1.ClearBackground(), self.referPeer1.Refresh(), self.referPeer1.SetSelection(0),\
                       self.referPeer2.ClearBackground(), self.referPeer2.Refresh(), self.referPeer2.SetSelection(0),\
                       self.referPeer3.ClearBackground(), self.referPeer3.Refresh(), self.referPeer3.SetSelection(0),\
                       self.referPeer4.ClearBackground(), self.referPeer4.Refresh(), self.referPeer4.SetSelection(0),\
                       self.referPeer5.ClearBackground(), self.referPeer5.Refresh(), self.referPeer5.SetSelection(0),\
                       self.coercion.ClearBackground(), self.coercion.Refresh(), self.coercion.SetValue(0),\
                       self.coercionPeer1.ClearBackground(), self.coercionPeer1.Refresh(), self.coercionPeer1.SetSelection(0),\
                       self.coercionPeer2.ClearBackground(), self.coercionPeer2.Refresh(), self.coercionPeer2.SetSelection(0),\
                       self.coercionPeer3.ClearBackground(), self.coercionPeer3.Refresh(), self.coercionPeer3.SetSelection(0),\
                       self.coercionPeer4.ClearBackground(), self.coercionPeer4.Refresh(), self.coercionPeer4.SetSelection(0),\
                       self.coercionPeer5.ClearBackground(), self.coercionPeer5.Refresh(), self.coercionPeer5.SetSelection(0),\
                       self.initiationOut.ClearBackground(), self.initiationOut.Refresh(), self.initiationOut.SetSelection(0),\
                       self.initiationPeer1.ClearBackground(), self.initiationPeer1.Refresh(), self.initiationPeer1.SetSelection(0),\
                       self.initiationPeer2.ClearBackground(), self.initiationPeer2.Refresh(), self.initiationPeer2.SetSelection(0),\
                       self.initiationPeer3.ClearBackground(), self.initiationPeer3.Refresh(), self.initiationPeer3.SetSelection(0),\
                       self.initiationPeer4.ClearBackground(), self.initiationPeer4.Refresh(), self.initiationPeer4.SetSelection(0),\
                       self.initiationPeer5.ClearBackground(), self.initiationPeer5.Refresh(), self.initiationPeer5.SetSelection(0)]
        for each in range(len(dataEntries)): 
            dataEntries[each]
        for eachItem in range(len(maps)):
            maps.pop()

    def OnRanButton(self, evt):  
        """ Allow a child to be randomly selected """
        childRandomPull = randint(1,(len(childList)-1))
        ranChild = childList[childRandomPull]
        dlg = wx.MessageDialog(self,ranChild,'Observe This Child:',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()    

        """ GIS Mapping """
    def OnMapButton1(self, evt):
        win = MyMapFrame1()
        win.SetSize((800, 600))
        win.CenterOnParent(wx.BOTH)
        win.Show(True)
    def OnMapButton2(self, evt):
        win = MyMapFrame2()
        win.SetSize((600, 500))
        win.CenterOnParent(wx.BOTH)
        win.Show(True)
    def OnMapButton3(self, evt):
        win = MyMapFrame3()
        win.SetSize((600, 500))
        win.CenterOnParent(wx.BOTH)
        win.Show(True)   
    def OnMapButtonCourtney2(self, evt):
        win = MyMapFrameCourtney2()
        win.SetSize((600, 500))
        win.CenterOnParent(wx.BOTH)
        win.Show(True)
    def OnMapButtonGordon(self, evt):
        win = MyMapFrameGordon()
        win.SetSize((600, 500))
        win.CenterOnParent(wx.BOTH)
        win.Show(True)   
    ##############################  


class MyMapFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Map of Outside # 1')
        bmp1 = bitPALsMaps.getOut1_3feetGridBitmap()  #converted to code prior
        #bmp = wx.Bitmap("Out1_3FeetGrid.bmp") # raw map
        self.Image = statbmp.GenStaticBitmap(self, -1, bmp1)
        self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.Image, 0)
        self.SetSizerAndFit(S)         

    def OnClick(self, event):
        # if needed time: maps.append([time.strftime("%M:%S"),mF1x,mF1y])
        maps.append(1)
        maps.append(event.GetPosition().Get())
        #maps.append(event.GetX()); maps.append(event.GetY())
        #print maps
        map1Infodlg = wx.MessageBox('Data Recorded', \
                                    caption = 'Data Status for Map 1', \
                                    style = wx.OK, parent = self)   

class MyMapFrame2(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Map of Outside # 2')
        bmp2 = bitPALsMaps.getOut2_3feetGridBitmap()
        #bmp = wx.Bitmap("Out2_3FeetGrid.bmp")
        self.Image = statbmp.GenStaticBitmap(self, -1, bmp2)
        self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.Image, 0)
        self.SetSizerAndFit(S)

    def OnClick(self, event):
        maps.append(2)
        maps.append(event.GetPosition().Get())        
        map2Infodlg = wx.MessageBox('Data Recorded', \
                                    caption = 'Data Status for Map 2', \
                                    style = wx.OK, parent = self) 

class MyMapFrame3(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Map of Outside # 3')
        bmp3 = bitPALsMaps.getOut3_3feetGridBitmap()
        #bmp = wx.Bitmap("Out3_3FeetGrid.bmp")
        self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmp3)
        self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.Image, 0)
        self.SetSizerAndFit(S)

    def OnClick(self, event): 
        maps.append(3)
        maps.append(event.GetPosition().Get())
        map3Infodlg = wx.MessageBox('Data Recorded', \
                                    caption = 'Data Status for Map 3', \
                                    style = wx.OK, parent = self)         

class MyMapFrameCourtney2(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Map of Inside Class # 1')
        bmpL = bitPALsMaps.getCourtney2_3feetGridBitmap()
        #bmp = wx.Bitmap("Courtney2_3FeetGrid.bmp")
        self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmpL)
        self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.Image, 0)
        self.SetSizerAndFit(S)

    def OnClick(self, event):
        maps.append(4)
        maps.append(event.GetPosition().Get())
        map4Infodlg = wx.MessageBox('Data Recorded', \
                                    caption = 'Data Status for Inside Class 1 Map', \
                                    style = wx.OK, parent = self) 

class MyMapFrameGordon(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Map of Inside Class # 2')
        bmpC = bitPALsMaps.getGordon_3feetGridBitmap()
        #bmp = wx.Bitmap("Gordon_3FeetGrid.bmp")
        self.Image = statbmp.GenStaticBitmap(self, wx.ID_ANY, bmpC)
        self.Image.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(self.Image, 0)
        self.SetSizerAndFit(S)

    def OnClick(self, event):
        maps.append(5)
        maps.append(event.GetPosition().Get())
        map5Infodlg = wx.MessageBox('Data Recorded', \
                                    caption = 'Data Status for Inside Class 2 Map', \
                                    style = wx.OK, parent = self) 

if __name__ == '__main__':
    app = wx.App(False)
    PALsFrame().Show()
    app.MainLoop()             