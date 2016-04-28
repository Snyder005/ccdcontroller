from PyQt4 import QtCore
import time
import sys

class AThread(QtCore.QThread):

    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print "Increasing"
            count +=1

def usingQThread():

    app = QtCore.QCoreApplication([])
    thread = AThread()
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    usingQThread()

"""
    @QtCore.pyqtSlot()
    def process(self):

        print "Process started."

        ## Check if single exposure
        if self.exptype in ["Exposure", "Dark", "Bias"]:

            filebase = "{0}.{1}.{2}s".format(self.imtitle, self.mode, self.exptime)
   
            ## Perform exposure
            self.log.emit("Starting {0}s {1} image with filebase {2}.".format(self.exptime,
                                                                              self.exptype,
                                                                              filebase), 'info')

            time.sleep(5)
            try:
                filename = exposure.im_acq(self.mode, filebase, self.exptime)
            except subprocess.CalledProcessError:
                self.log.emit("Error in executable {0}_acq. Image not taken.".format(self.mode), 'error')
            except OSError:
                self.log.emit("Executable {0}_acq not found. Image not taken.".format(self.mode), 'error')
            else:
                self.log.emit("Exposure {0} finished successfully.".format(filename), 'info')

        elif self.exptype in ["Exposure Stack", "Dark Stack", "Bias Stack"]:

            filebase = "{0}.{1}.{2}s".format(self.imtitle, self.mode, self.exptime)

            ## Perform stack
            self.log.emit("Starting {0} with imcount {1}, exptime {2}, and filebase {3}.".format(self.exptype, self.imcount, self.exptime, filebase), 'info')

            time.sleep(5)
            try:
                exposure.stack(self.mode, filebase, self.imcount, self.exptime, self.start)
            except subprocess.CalledProcessError:
                self.log.emit("Error in executable {0}_acq. Image not taken.".format(self.mode), 'error')
            except OSError:
                self.log.emit("Executable {0}_acq not found. Image not taken.".format(self.mode), 'error')
            else:
                self.log.emit("Exposure stack {0} finished successfully.".format(filebase), 'info')

        elif self.exptype in ["Exposure Series", "Dark Series"]:

            filebase = "{0}.{1}".format(self.imtitle, self.mode)

            ## Parameter checks
            if self.mintime > self.maxtime:
                self.log.emit("Minimum time must be less than Maximum time.")
                self.finished.emit()
                return

            ## Perform series
            self.log.emit("Starting {0} with mintime {1}, maxtime {2}, step {3}, and filebase {4}.".format(self.exptype, self.mintime, self.maxtime, self.step, filebase), 'info')

            time.sleep(5)
            try:
                exposure.series(self.mode, filebase, self.mintime, self.maxtime, self.step)
            except subprocess.CalledProcessError:
                self.log.emit("Error in executable {0}_acq. Image not taken.".format(self.mode), 'error')
            except OSError:
                self.log.emit("Executable {0}_acq not found. Image not taken.".format(self.mode), 'error')
            else:
                self.log.emit("Exposure series {0} finished successfully.".format(filebase), 'info')

        self.finished.emit()"""
