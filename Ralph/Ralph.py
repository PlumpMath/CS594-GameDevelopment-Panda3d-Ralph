# Roaming-Ralph was modified to remove collision part.

import direct.directbase.DirectStart
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

from direct.gui.DirectGui import *

from direct.directbase.DirectStart import *
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Texture
from panda3d.core import WindowProperties
from panda3d.core import *
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence
# from common.Constants import Constants

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
# from Character import Character
import datetime
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

from panda3d.bullet import BulletVehicle


from direct.showbase import Audio3DManager

from Audio import Audio



SPEED = 0.5

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class World(DirectObject):

    def __init__(self):
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0}
        base.win.setClearColor(Vec4(0,0,0,1))


        self.speed = 0



        self.font_digital = loader.loadFont('font/SFDigitalReadout-Heavy.ttf')


        # Speedometer
        self.speed_img = OnscreenImage(image="models/speedometer.png", scale=.5, pos=(1.1, 0, -.95))
        self.speed_img.setTransparency(TransparencyAttrib.MAlpha)
        OnscreenText(text="km\n/h", style=1, fg=(1, 1, 1, 1),
                     font=self.font_digital, scale=.07, pos=(1.25, -.92))


        # Display Speed
        self.display_speed = OnscreenText(text=str(self.speed), style=1, fg=(1, 1, 1, 1),
                                          pos=(1.3, -0.95), align=TextNode.ARight, scale=.07, font=self.font_digital)

        # Health Bar

        self.bars = {'H' : 100, 'EH' : 0 ,'A' : 0 }

        # bk_text = "This is my Demo"
        # self.textObject = OnscreenText(text = bk_text, pos = (0.55,-0.05),scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)

        self.Health_bar = DirectWaitBar(text = "", value = 100, pos = (0.280,0,0.475), barColor= (1,0,0,1), frameSize = (0,.705,.3,.35))

        self.EHealth_bar = DirectWaitBar(text = "", value = 0, pos = (1,0,0.475), barColor= (0,1,0,1), frameSize = (0,.23,.3,.35),range = 50 )

        self.Armour_bar = DirectWaitBar(text = "", value = 0, pos = (.43,0,.593), barColor= (159,0,255,1), frameSize = (0,.8,.3,.35))

        # self.bar = DirectWaitBar(text = "hi",
        #     value = 0,
        #     range = 500,
        #     pos = ( 0,0,0), 
        #     barColor = (0.97,0,0,1), 
        #     frameSize = (-0.3,0.3,0.5,0.8),
        #     text_mayChange = 1,
        #     text_shadow =(0,0,0,0.8),
        #     text_fg = (0.9,0.9,0.9,1),
        #     text_scale = 0.025, 
        #     text_pos = (0,0.01,0))


        def getHealthStatus() :
            return self.bars

        def displayBars() :
            health = getHealthStatus()
            self.Health_bar['value'] = health['H']
            self.EHealth_bar['value'] = health['EH']
            self.Armour_bar['value'] = health['A']


        def armourPickup() :
            self.bars['A'] += 25
            displayBars()

        def healthPickup() :
            self.bars['EH'] += 25
            displayBars()

        def decHealth() :
            self.bars['H'] -= 10
            displayBars()


              


        # Post the instructions
        self.frame = OnscreenImage(image = "models/gframe.png", pos = (0,0,0), scale = (1.25, 1, 1) )
        self.frame.setTransparency(TransparencyAttrib.MAlpha)


        # self.title = addTitle("Panda3D Tutorial: Roaming Ralph (Walking on the Moon)")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[Left Arrow]: Rotate Ralph Left")
        self.inst3 = addInstructions(0.85, "[Right Arrow]: Rotate Ralph Right")
        self.inst4 = addInstructions(0.80, "[Up Arrow]: Run Ralph Forward")
        self.inst6 = addInstructions(0.70, "[A]: Rotate Camera Left")
        self.inst7 = addInstructions(0.65, "[S]: Rotate Camera Right")
        
        # Set up the environment
        #
        self.environ = loader.loadModel("models/square")      
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)
        self.environ.setScale(100,100,1)
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
    	self.environ.setTexture(self.moon_tex, 1)
        
        # Create the main character, Ralph

        self.ralph = Actor("models/ralph",
                                 {"run":"models/ralph-run",
                                  "walk":"models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(0,0,0)

        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["forward",1])
        self.accept("a", self.setKey, ["cam-left",1])
        self.accept("s", self.setKey, ["cam-right",1])
        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["forward",0])
        self.accept("a-up", self.setKey, ["cam-left",0])
        self.accept("s-up", self.setKey, ["cam-right",0])
        self.accept("h", decHealth)
        self.accept("j", healthPickup)
        self.accept("k", armourPickup)

        taskMgr.add(self.move,"moveTask")

        taskMgr.doMethodLater(.1, self.show_speed, 'updateSpeed')

        # Game state variables
        self.isMoving = False

        # Set up the camera
        
        base.disableMouse()
        base.camera.setPos(self.ralph.getX(),self.ralph.getY()+10,2)
        

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))



        self.audioManager = Audio(self)
        self.audioManager.startAudioManager()

        self.audioManager.initialiseSound(self.ralph)

        
    def show_speed(self, task):
        # self.speed = str(format(self.ralph.getCurrentSpeedKmHour(), '0.2f'))
        # self.speed = 2
        # print self.speed

        # Update Speed Display
        self.display_speed.destroy()
        self.display_speed = OnscreenText(text=str(self.speed), style=3, fg=(1, 1, 1, 1),
            pos=(1.2, -0.95), align=TextNode.ARight, scale=.15, font=self.font_digital)
        return task.cont


        
    
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value


    
    

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        base.camera.lookAt(self.ralph)
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +20 * globalClock.getDt())

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.ralph.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

        if (self.keyMap["left"]!=0):
            self.ralph.setH(self.ralph.getH() + 300 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            self.ralph.setH(self.ralph.getH() - 300 * globalClock.getDt())
        if (self.keyMap["forward"]!=0):
            self.ralph.setY(self.ralph, -25 * globalClock.getDt())
            # print "walk", self.speed 
            if self.speed < 100 :
                self.speed = self.speed + self.speed/100 + 1
            else :
                self.speed = self.speed + self.speed/200 + 1
                # print self.speed
            # self.audioManager.updateSound()
            self.audioManager.updateSound()

        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):
            if self.isMoving is False:
                self.ralph.loop("run")
                # print "run"
                self.isMoving = True
        else:
            if self.isMoving:
                self.ralph.stop()
                self.speed = 0
                self.ralph.pose("walk",5)
                self.isMoving = False

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.ralph.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

         
        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.
        
        self.floater.setPos(self.ralph.getPos())
        self.floater.setZ(self.ralph.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        return task.cont


w = World()
run()

