'''
Created on 08 May 2014

@author: Deon
'''
from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4.QtGui import QFileDialog
from Output.AsciiGUI import Ui_Ascii
from mylib import ProgressBar
import numpy as np
import sys
import os
import zipfile
from shutil import copy2

        
        
class AsciiDEF(QGroupBox):
    def __init__(self, ScanmanMain=""):
        QGroupBox.__init__(self)
        self.name = "Ascii"
        self.ui = Ui_Ascii()
        self.ui.setupUi(self)
        self.scanman = ScanmanMain
        
        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.Directory)
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.curfilter = ""
        self.lastdir=""
        self.setstart = 0
        self.setend = -1
        self.singlefile = True
        
    #**************************************************************************************
    def CombinedChanged(self):
        if self.ui.combine_files_check.isChecked():
            self.ui.GSASButton.setText("GSAS (*.zip)")
        else:
            self.ui.GSASButton.setText("GSAS (*.fxye)")
    
    #**************************************************************************************
    def ExportGSAS(self):
        sep = os.linesep
        self.Getexportsettings()
        
        if self.scanman.ui.outputGroupBox.ui.files_all_radio.isChecked():           #should put this in also in Getexportsettings
            flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
        elif self.scanman.ui.outputGroupBox.ui.files_current_radio.isChecked():
            flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        
        
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setViewMode(QFileDialog.Detail)
        if self.lastdir == "":
            self.lastdir = self.lastdir=os.path.dirname(self.scanman.ui.sourceGroupBox.filelist[flistidx[0]].location)
        dirname = self.filedialog.getExistingDirectory(self, "Select export dir", self.lastdir)
        if dirname == "": return
        self.lastdir = dirname
        
        numfiles = len(flistidx)
        progress = ProgressBar("Exporting graph data...", numfiles)    
        
        #GSAS only works with angles, therefore force ScanMan to select this (bad hack)
        oldaxistype = self.scanman.axistype
        if oldaxistype != 'Angle':
            self.scanman.ui.angle_radio.click()


        
        
        if self.ui.GSASLinkProfileCheckBox.isChecked():
            insfname = self.ui.GSASProfileLineEdit.text()
            #Set up initial instrument file if it does not exist
            instrumentname = self.scanman.config['instrument']
            wavelength = self.scanman.config['source']['detector']['lambda']
            if insfname == "":
                insfnamebase = instrumentname + "_init_lam(" + str(wavelength) +  ").prm"
                insfname = os.path.join(str(dirname), insfnamebase)
            if os.path.exists(insfname) == False:
                insf = open(insfname, 'w')
                zoffset = 0.0
                insf.write("            123456789012345678901234567890123456789012345678901234567890%s" %(sep))
                insf.write("INS   BANK      1%s" %(sep))    
                insf.write("INS   HTYPE      PNCR%s" %(sep))        #Histogram type: Powder, Neutron, Constant wavelength,  R=fixed for powders   
                insf.write("INS  1 ICONS  %f  0.0       0.0         %f      0.0    0       0.0   %s" %(wavelength, zoffset, sep))
                insf.write("INS  1I HEAD  DUMMY INCIDENT SPECTRUM FOR DIFFRACTOMETER %s%s" %(self.scanman.config['instrument'], sep))
                insf.write("INS  1I ITYP    0    0.0000  180.0000         1                                 %s" %(sep))
                insf.write("INS  1PRCF1     1    6      0.01                                                %s" %(sep))
                insf.write("INS  1PRCF11   0.000000E+00   0.000000E+00   0.000000E+00   0.000000E+00        %s" %(sep))
                insf.write("INS  1PRCF12   0.000000E+00   0.000000E+00   0.000000E+00   0.000000E+00        %s" %(sep))
                insf.write("INS  1PRCF2     2    6      0.01                                                %s" %(sep))
                insf.write("INS  1PRCF21   0.000000E+00   0.000000E+00   0.000000E+00   0.000000E+00        %s" %(sep))
                insf.write("INS  1PRCF22   0.000000E+00   0.000000E+00        %s" %(sep))
                insf.close()
            else:
                insfnamebase = os.path.basename(insfname)
                try:
                    copy2(insfname, os.path.join(str(dirname), insfnamebase))
                except:
                    True
        
        
        
        #Do this if a single zip file must be created
        if self.singlefile == True:
            src = self.scanman.datasrc
            fnames = sorted([self.scanman.ui.sourceGroupBox.filelist[flistidx[i]].filename for i in range(len(flistidx))])
            #fnames.sort()
            name1 = str.split(os.path.basename(os.path.splitext(str(fnames[0]))[0]),".")[0]
            name2 = str.split(os.path.basename(os.path.splitext(str(fnames[-1]))[0]),".")[0]
            if len(name1) > 4 and len(name2) >4:
                try:
                    name2 = str(int(name2[4:]))
                except:
                    True
            fnamezip = name1 + "-" + name2 + self.scanman.modext + "_c" + ".zip"
            zfile = zipfile.ZipFile(os.path.join(str(dirname),fnamezip), "w")
            True
        
        #Do this for all the datafiles
        for filei in flistidx:
            progress.setinfo(self.scanman.ui.sourceGroupBox.filelist[filei].filename)
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            src = self.scanman.datasrc
            
            self.scanman.exportparams.sort()
                
            axistype = self.scanman.axistype        #should now be 'Angle'
            sfname = str.split(os.path.basename(os.path.splitext(str(src.dataset[1].filename))[0]),".")[0]
            sfname = sfname + self.scanman.modext
            
            if self.ui.dset_all_radio.isChecked():
                self.setend = len(src.dataset)
                self.setstart = 1
            for nr in range(self.setstart,self.setend):
                fname = sfname + "_dset(" + str(nr) + ").fxye"
                self.scanman.SelectData(nr,display=False)
                src = self.scanman.datasrc
                x_original = src.dataset[nr].currframe.x_2th.astype(float)
                y_original = src.dataset[nr].currframe.y_2th.astype(float)
                
                nrpoints = len(y_original)
                x = np.linspace(x_original[0], x_original[-1], nrpoints)
                stepsize = x[1]-x[0]
                y = np.interp(x,x_original,y_original)
                thisfname = os.path.join(str(dirname),fname)
                f = open(thisfname, 'wb')
                headerline = src.dataset[nr].filename + " | Dataset: " + str(nr) + " | Type: " + src.ylabel + sep
                f.write(headerline.encode('utf-8'))
                
                if self.ui.GSASLinkProfileCheckBox.isChecked():
                    f.write(("Instrument parameter file:%s%s" %(insfnamebase,sep)).encode('utf-8'))
                    
                detstr = "#"
                for param in src.dataset[nr].detprm: detstr = detstr + sep + "# " + param +":" + str(src.dataset[nr].detprm[param])
                f.write(("%s%s" %(detstr,sep)).encode('utf-8'))
                paramstr = "#"
                for param in self.scanman.exportparams: 
                    try:
                        paramstr = paramstr + sep +"# " + param +":" + src.dataset[nr].prm[param]
                    except:
                        True
                if paramstr == "#": paramstr = sep + "# set:"+str(nr)      #No parameters were selected to export, but we need some text in that line
                f.write(("%s%s" %(paramstr,sep)).encode('utf-8'))
                f.write(("BANK 1 %i %i CONS %f %f 0 0 FXY%s" %(nrpoints, nrpoints, x[0]*100, stepsize*100,sep)).encode('utf-8'))
                for i in np.arange(nrpoints):
                    f.write(('%f %f %s' % (x[i]*100, y[i], sep)).encode('utf-8'))
                f.close()
                
                if self.singlefile == True:     #add it to the zip file
                    zfile.write(thisfname)
                    os.remove(thisfname)
                    True
            progress.step()
        if self.singlefile == True:
            #zfile.write(os.path.join(str(dirname),insfnamebase))
            zfile.close()
  
  
        #Select the initial axis view again
        if oldaxistype != 'Angle':
            if oldaxistype == 'Channel':
                self.scanman.ui.channel_radio.click()
            elif oldaxistype == 'Position':
                self.scanman.ui.position_radio.click()
            elif oldaxistype == 'd-spacing':
                self.scanman.ui.dspacing_radio.click()

        True    
        
        
    
    #**************************************************************************************
    def ExportFullprof(self):
        self.Getexportsettings()
        
        if self.scanman.ui.outputGroupBox.ui.files_all_radio.isChecked():           #should put this in also in Getexportsettings
            flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
        elif self.scanman.ui.outputGroupBox.ui.files_current_radio.isChecked():
            flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
        
        self.filedialog.setAcceptMode(QFileDialog.AcceptSave)
        self.filedialog.setViewMode(QFileDialog.Detail)
        if self.lastdir == "":
            self.lastdir = self.lastdir=os.path.dirname(self.scanman.ui.sourceGroupBox.filelist[flistidx[0]].location)
        dirname = self.filedialog.getExistingDirectory(self, "Select export dir", self.lastdir)
        if dirname == "": return
        self.lastdir = dirname
        
        numfiles = len(flistidx)
        progress = ProgressBar("Exporting graph data...", numfiles)    

        if self.singlefile == True:
            src = self.scanman.datasrc
            fnames = sorted([self.scanman.ui.sourceGroupBox.filelist[flistidx[i]].filename for i in range(len(flistidx))])
            #fnames.sort()
            name1 = str.split(os.path.basename(os.path.splitext(str(fnames[0]))[0]),".")[0]
            name2 = str.split(os.path.basename(os.path.splitext(str(fnames[-1]))[0]),".")[0]
            if len(name1) > 4 and len(name2) >4:
                try:
                    name2 = str(int(name2[4:]))
                except:
                    True
                    
            fname = name1 + "-" + name2 + self.scanman.modext + "_c" + ".xy"
            f = open(os.path.join(str(dirname),fname), 'w')
                    
            True
        
        for filei in flistidx:
            progress.setinfo(self.scanman.ui.sourceGroupBox.filelist[filei].filename)
            self.scanman.ui.sourceGroupBox.SelectDataFile(filei)
            src = self.scanman.datasrc
            
            self.scanman.exportparams.sort()
            axistype = self.scanman.axistype
            #filemod = ""
            if self.singlefile == False:
                fname = str.split(os.path.basename(os.path.splitext(str(src.dataset[1].filename))[0]),".")[0]
                fname = fname + self.scanman.modext + ".xy"
                f = open(os.path.join(str(dirname),fname), 'w')
            
            if self.ui.dset_all_radio.isChecked():
                self.setend = len(src.dataset)
                self.setstart = 1
            for nr in range(self.setstart,self.setend):
                self.scanman.SelectData(nr,display=False)
                src = self.scanman.datasrc
              
                if axistype == 'Channel':
                    x = np.array(src.dataset[nr].currframe.x_chan).astype(float)
                    y = src.dataset[nr].currframe.y.astype(float)
                elif axistype == 'Position':
                    x = src.dataset[nr].currframe.x_mm.astype(float)
                    y = src.dataset[nr].currframe.y.astype(float)
                elif axistype == 'Angle':
                    x = src.dataset[nr].currframe.x_2th.astype(float)
                    y = src.dataset[nr].currframe.y_2th.astype(float)
                elif axistype == 'd-spacing':
                    x = src.dataset[nr].currframe.x_d.astype(float)
                    y = src.dataset[nr].currframe.y_2th.astype(float)
                nrpoints = len(y)
                f.write('XYDATA\n')
                f.write("File name: %s\n" %(src.dataset[nr].filename))
                f.write("| Dataset: %s| Type: %s\n" %(nr, src.ylabel))
                detstr = ""
                for param in src.dataset[nr].detprm: detstr = detstr + "| " + param +":" + str(src.dataset[nr].detprm[param])
                f.write("%s\n" %(detstr))
                paramstr = ""
                #for param in src.exportparams: paramstr = paramstr + ", " + param +":" + src.dataset[nr].prm[param]
                for param in self.scanman.exportparams: 
                    try:
                        paramstr = paramstr + "| " + param +":" + src.dataset[nr].prm[param]
                    except:
                        True
                if paramstr == "": paramstr = "| set:"+str(nr)      #No parameters were selected to export, but we need some text in that line
                f.write("%s\n" %(paramstr))
                f.write("%s Intensity\n" %(axistype))
                for i in np.arange(nrpoints):
                    f.write('%f %f\n' % (x[i], y[i]))
                f.write("\n")
            
            if self.singlefile == False:
                f.truncate(f.tell()-2)      #Removes the last extra newline
                f.close()
            progress.step()
        if self.singlefile == True:
            f.truncate(f.tell()-2)      #Removes the last extra newline
            f.close()    
        True    
        

    #**************************************************************************************
    def OpenFileGSASProfile(self):
        self.filedialog.setFileMode(QFileDialog.ExistingFiles)
        self.filedialog.setViewMode(QFileDialog.Detail)
        curdir = self.lastdir
        if curdir == "":
            if self.scanman.ui.outputGroupBox.ui.files_all_radio.isChecked():           
                flistidx = range(len(self.scanman.ui.sourceGroupBox.filelist))
            elif self.scanman.ui.outputGroupBox.ui.files_current_radio.isChecked():
                flistidx = [self.scanman.ui.sourceGroupBox.ui.file_tbl.currentRow()]
            curdir = os.path.dirname(self.scanman.ui.sourceGroupBox.filelist[flistidx[0]].location)
        file_types = "GSAS-II iparam file (*.instprm);;GSAS iparmam file (*.prm);; All (*.*)"
        fnames, filters = self.filedialog.getOpenFileNamesAndFilter(self, 'Open file', curdir, file_types, initialFilter=self.curfilter)
        if (fnames==[]): return
        self.lastdir = os.path.dirname(str(fnames[0]))
        self.filedialog.setDirectory(self.lastdir)
        
        self.curfilter = filters
        self.ui.GSASProfileLineEdit.setText(fnames[0])

    
    #**************************************************************************************
    def Getexportsettings(self):
        if self.ui.dset_all_radio.isChecked():
            self.setstart = 1
            self.setend = len(self.scanman.datasrc.dataset)
        elif self.ui.dset_current_radio.isChecked():
            self.setstart = self.scanman.datasrc.currset
            self.setend = self.setstart+1
        elif self.ui.dset_range_radio.isChecked():
            self.setstart = self.ui.dset_rangemin_spin.value()
            self.setend = self.ui.dset_rangemax_spin.value() + 1
        #self.includeHeader = self.ui.headers_check.isChecked()
        self.singlefile = self.ui.combine_files_check.isChecked()
        True
       

if __name__ == '__main__':
    import PyQt4.QtGui as qt
    app = qt.QApplication(sys.argv)
    window=AsciiDEF()
    window.show()
    sys.exit(app.exec_())

        