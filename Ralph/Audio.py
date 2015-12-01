from direct.showbase.DirectObject import DirectObject
from direct.showbase import Audio3DManager
from direct.interval.IntervalGlobal import Sequence, SoundInterval


class Audio(DirectObject):
    def __init__(self, main):
        # self.taskMgr = taskMgr
        # self.base = base
        self.main = main
        # # Create an audio manager. This is attached to the camera for
        # # player 1, so sounds close to other players might not be very loud
        # self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.camera)

        # play background music
        # self.main.taskMgr.add(self.play_music, "PlayMusic")

    def play_music(self, task):
        # load background music
        music1 = loader.loadSfx("audio/bkgd/Sandstorm.m4a")
        music2 = loader.loadSfx("audio/bkgd/LevelsNoVocals.mp3")
        music3 = loader.loadSfx("audio/bkgd/RaceMusic.mp3")

        music_seq = Sequence(SoundInterval(music1), SoundInterval(music2), SoundInterval(music3),
                             name="Music Sequence")
        music_seq.loop(0.0, -1.0, 1.0)


    def startAudioManager(self):

        # Create an audio manager. This is attached to the camera for
        # player 1, so sounds close to other players might not be very
        # loud
        self.audioManager = Audio3DManager.Audio3DManager(base.sfxManagerList[0],base.camera)

        # Distance should be in m, not feet
        self.audioManager.setDistanceFactor(3.28084)

        # self.initialiseSound(self.audioManager)


    def initialiseSound(self,char):
            """Start the engine sound and set collision sounds"""

            # Set sounds to play for collisions
            # self.collisionSound = CollisionSound(
            #     nodePath=self.np,
            #     sounds=["data/sounds/09.wav"],
            #     thresholdForce=600.0,
            #     maxForce=800000.0)

            # np - nodePath

            self.engineSound = self.audioManager.loadSfx("sound/engine.wav")
            self.audioManager.attachSoundToObject(self.engineSound, char)
            self.engineSound.setLoop(True)
            self.engineSound.setPlayRate(0.6)
            self.engineSound.play()

            # self.gearSpacing = (self.specs["sound"]["maxExpectedRotationRate"] /
            #     self.specs["sound"]["numberOfGears"])

            self.gearSpacing = (150 / 4)

            self.reversing = False


    def updateSound(self):
            """Use vehicle speed to update sound pitch"""

            # soundSpecs = self.specs["sound"]
            # Use rear wheel rotation speed as some measure of engine revs
            # wheels = (self.vehicle.getWheel(idx) for idx in (2, 3))
            # wheelRate is in degrees per second
            # wheelRate = 0.5 * abs(sum(w.getDeltaRotation() / dt for w in wheels))
            wheelRate = 0.5 * self.main.speed

            # Calculate which gear we're in, and what the normalised revs are
            if self.reversing:
                numberOfGears = 1
            else:
                numberOfGears = 4
            # gear = min(int(wheelRate / self.gearSpacing),
            #         numberOfGears - 1)

            gear = min(int(wheelRate/ self.gearSpacing),
                    numberOfGears - 1)

            print gear

            if max(int(wheelRate/ self.gearSpacing),numberOfGears - 1) < 4 :
                # posInGear = (wheelRate - gear * self.gearSpacing) / self.gearSpacing
                posInGear = (wheelRate - gear * self.gearSpacing) / self.gearSpacing

                print posInGear

                targetPlayRate = 0.6 + posInGear * (1.5 - 0.6)

                print targetPlayRate

                currentRate = self.engineSound.getPlayRate()
                self.engineSound.setPlayRate(0.8 * currentRate + 0.2 * targetPlayRate)
