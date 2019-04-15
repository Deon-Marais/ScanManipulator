from PyQt4.QtGui import QGroupBox as QGroupBox
from PyQt4 import QtCore
import PyQt4.QtGui as qt
from PyQt4.QtGui import QFileDialog
from Misc.NeuralNetGUI import Ui_NeuralNet
import numpy as np
import os.path
#import urllib2
import copy
import time
import struct

import mylib

class NeuralNetDEF(QGroupBox):
    def __init__(self, ScanmanMain):
        QGroupBox.__init__(self)
        self.name="NeuralNet"
        
        self.ui = Ui_NeuralNet()
        self.ui.setupUi(self)        
        self.trainTable = mylib.Table(self.ui.trainingDataTable)
        #self.ui.trainingDataTable = self.trainTable
        

        self.scanman = ScanmanMain
        
        
        #self.trainTable= mylib.Table(self.ui.trainingDataTable)
        self.testDataTable = mylib.Table(self.ui.testDataTable)
        
        self.filedialog = QFileDialog()
        self.filedialog.setFileMode(QFileDialog.ExistingFiles)
        self.filedialog.setViewMode(QFileDialog.Detail)
        self.curfilter = ""
        
        self.tableHeaders = ["1","2","3"]
        self.ui.trainingDataTable.setHorizontalHeaderLabels(self.tableHeaders)
        #self.trainTable.setHorizontalHeaderLabels(self.tableHeaders)
        self.trainingdata = [[]]
        self.nrrows = self.nrcols = 0
        
        
    
    #**************************************************************************************
    def NrInputsChanged(self,newnrinputs):
        self.nrinputs = newnrinputs
        self.nroutputs = self.nrcols - self.nrinputs
        self.ui.nroutputsLabel.setText(str(self.nroutputs))
        
        self.inputvals = np.transpose(self.trainingdata[:self.nrinputs])
        self.outputvals = np.transpose(self.trainingdata[self.nrinputs:])
        #self.in_scale = [0]*self.nrinputs
        #self.in_min = [0]*self.nrinputs
        #self.in_max = [0]*self.nrinputs
        #self.out_scale = [0]*self.nroutputs
        #self.out_min = [0]*self.nroutputs
        #self.out_max = [0]*self.nroutputs
        #for i in range(self.nrinputs):
        #    self.in_min[i]= min(self.trainingdata[i])
        #    self.in_max[i]= max(self.trainingdata[i])
        #    self.in_scale[i]=self.in_max[i] - self.in_min[i]
        #    True
        #for i in range(self.nroutputs):
        #    self.out_min[i]= min(self.trainingdata[self.nrinputs+i])
        #    self.out_max[i]= max(self.trainingdata[self.nrinputs+i])
        #    self.out_scale[i]=self.out_max[i] - self.out_min[i]
        #    True
        
        #self.train_min=np.min(self.outputvals)
        #self.train_max=np.max(self.outputvals)
        #self.scalefactor = (self.train_max - self.train_min)
        self.out_min = np.min(self.outputvals)
        self.out_max = np.max(self.outputvals)
        self.out_scale = (self.out_max - self.out_min)
        self.in_min = np.min(self.inputvals)
        self.in_max = np.max(self.inputvals)
        self.in_scale = (self.in_max - self.in_min)
        
        
        nrvals = len(self.inputvals)
        self.mindiff = 9.9e99
        self.maxdiff = 0.0
        for i in range(self.nrinputs):
            sorted = np.sort(self.trainingdata[:self.nrinputs][i])
            diff = sorted[1:nrvals] - sorted[:nrvals-1]
            mindiff = min(diff)
            maxdiff = max(diff)
            if mindiff < self.mindiff: self.mindiff = mindiff
            if maxdiff > self.maxdiff: self.maxdiff = maxdiff
        self.ui.minResolutionEdit.setText(str(self.mindiff))
        self.ui.desiredResolutionEdit.setText(str(self.maxdiff))
        
        True
        
    #**************************************************************************************
    def Read_columns(self,fname):
        f = open(fname, 'r')
        filecontent = f.read()
        f.close()
        data = filecontent.split("\n")[:-1]
        header = data[0].split()
        try:
            a=float(header[0])
            datastart = 0
            self.tableHeaders = [str(item) for item in range(len(header))]
        except:
            datastart = 1
            self.tableHeaders = header
        nrcols = len(self.tableHeaders)
        #self.trainingdata = [[]]*nrcols
        datavar = [[]]*nrcols
        for dataln in data[datastart:]:
            linevals = dataln.split()
            for item in range(nrcols):
                #self.trainingdata[item] = self.trainingdata[item] + [float(linevals[item])]
                datavar[item] = datavar[item] + [float(linevals[item])]
        return datavar
        True #To be implemented
    
    #**************************************************************************************
    def FileOpenTraining(self):
        file_types = ";;Columns (*.txt);;All (*.*)"
        #self.filedialog.selectFilter(self.curfilter)
        fname, filters = self.filedialog.getOpenFileNameAndFilter(self, 'Open file', '', file_types, initialFilter=self.curfilter)
        if (fname==[]): return
        self.filedialog.setDirectory(os.path.dirname(str(fname)))
        self.curfilter = filters
        #self.LoadMayavi()
        filetype = os.path.splitext(fname)[1][1:]
        if filetype =="txt":
            self.trainingdata = self.Read_columns(fname)
        
        self.nrcols = len(self.trainingdata)
        self.nrrows = len(self.trainingdata[0])
        self.ui.trainingDataTable.setColumnCount(self.nrcols)
        self.ui.trainingDataTable.setRowCount(self.nrrows)
        self.ui.trainingDataTable.setHorizontalHeaderLabels(self.tableHeaders)
        for i in range(self.nrcols):
            for j in range(self.nrrows):
                self.ui.trainingDataTable.setItem(j,i,qt.QTableWidgetItem())
                self.ui.trainingDataTable.item(j, i).setText(str(self.trainingdata[i][j]))
                True
        self.ui.nrInputsSpinBox.setMaximum(self.nrcols)
        
        #self.ui.testDataTable.setColumnCount(self.nrcols)
        #self.ui.testDataTable.setRowCount(self.nrrows)
        #self.ui.testDataTable.setHorizontalHeaderLabels(self.tableHeaders)
        #for i in range(self.nrcols):
        #    for j in range(self.nrrows):
        #        self.ui.testDataTable.setItem(j,i,qt.QTableWidgetItem())
        #        self.ui.testDataTable.item(j, i).setText(str(self.trainingdata[i][j]))
        #       True
        self.NrInputsChanged(self.ui.nrInputsSpinBox.value())


        #**************************************************************************************
    def FileOpenTest(self):
        file_types = ";;Columns (*.txt);;All (*.*)"
        #self.filedialog.selectFilter(self.curfilter)
        fname, filters = self.filedialog.getOpenFileNameAndFilter(self, 'Open file', '', file_types, initialFilter=self.curfilter)
        if (fname==[]): return
        self.filedialog.setDirectory(os.path.dirname(str(fname)))
        self.curfilter = filters
        filetype = os.path.splitext(fname)[1][1:]
        if filetype =="txt":
            self.testdata = self.Read_columns(fname)
        
        self.nrcols_testdata = len(self.testdata)
        self.nrrows_testdata = len(self.testdata[0])
        #self.ui.trainingDataTable.setColumnCount(self.nrcols)
        #self.ui.trainingDataTable.setRowCount(self.nrrows)
        #self.ui.trainingDataTable.setHorizontalHeaderLabels(self.tableHeaders)
        #for i in range(self.nrcols):
        #    for j in range(self.nrrows):
        #        self.ui.trainingDataTable.setItem(j,i,qt.QTableWidgetItem())
        #        self.ui.trainingDataTable.item(j, i).setText(str(self.trainingdata[i][j]))
        #        True
        #self.ui.nrInputsSpinBox.setMaximum(self.nrcols)
        
        self.ui.testDataTable.setColumnCount(self.nrcols_testdata)
        self.ui.testDataTable.setRowCount(self.nrrows_testdata)
        self.ui.testDataTable.setHorizontalHeaderLabels(self.tableHeaders)
        for i in range(self.nrcols_testdata):
            for j in range(self.nrrows_testdata):
                self.ui.testDataTable.setItem(j,i,qt.QTableWidgetItem())
                self.ui.testDataTable.item(j, i).setText(str(self.testdata[i][j]))
                True
        #self.NrInputsChanged(self.ui.nrInputsSpinBox.value())


        
    #**************************************************************************************
    def TrainTesting(self):
        from fann2 import libfann
        
        connection_rate = self.ui.connectionRateSpinBox.value()
        learning_rate = self.ui.learningRateSpinBox.value()
        num_input = self.nrinputs
        num_hidden = self.ui.layersSpinBox.value()
        neurons_per_layer = self.ui.neuronsSpinBox.value()
        num_output = self.nroutputs
        
        netparams=[]
        netparams = netparams + [num_input]
        netparams = netparams + [neurons_per_layer]*num_hidden
        netparams = netparams + [num_output]
        

        desired_error = self.ui.desiredErrorSpinBox.value()
        max_iterations = self.ui.maxIterSpinBox.value()
        iterations_between_reports = 10000
        
        ann = libfann.neural_net()
        #ann.create_standard(3,3,9,3)
        ann.create_standard_array(tuple(netparams))
        #ann.create_shortcut_array(tuple(netparams))
        #ann.create_sparse_array(connection_rate, (num_input, num_hidden, num_output))
        
        ann.set_learning_rate(learning_rate)
        #ann.set_training_algorithm(libfann.TRAIN_INCREMENTAL);
        

        #for i in range(1,num_hidden): 
        #    ann.set_activation_function_layer(libfann.LINEAR,i)
        #SIGMOID_SYMMETRIC_STEPWISE, SIGMOID_SYMMETRIC, COS_SYMMETRIC, LINEAR
        ann.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC)
        ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC)
        
        #ann.set_activation_steepness(0.75)
        ann.set_train_error_function(libfann.ERRORFUNC_LINEAR)
        #ann.set_training_algorithm(libfann.TRAIN_INCREMENTAL)
        ann.set_training_algorithm(libfann.TRAIN_BATCH)
        #ann.set_activation_steepness(0.5)
        
        self.train_data = libfann.training_data()
        #self.train_data.set_train_data(self.inputvals,self.outputvals)
        self.train_data.set_train_data((self.inputvals-self.in_min)/self.in_scale,(self.outputvals-self.out_min)/self.out_scale)
        #self.train_data.scale_input_train_data(0.0, 1.0)
        #self.train_data.scale_output_train_data(0.0, 1.0)
        #self.train_data.shuffle_train_data()
        tic=time.time() 
        ann.train_on_data(self.train_data, max_iterations, iterations_between_reports, desired_error)
        neurons_between_reports = 2
        #ann.cascadetrain_on_data(self.train_data,neurons_per_layer,neurons_between_reports, desired_error)
        toc = time.time()-tic
        print ("%i iterations in %.0fs (%0.f iterations/second)\n" % (max_iterations,toc,max_iterations/toc))
        self.ann = ann
        #self.ann.print_connections()
        #result = np.array(ann.run([0,0]/self.scalefactor))*self.scalefactor
        #print result
        
        
        #ann.save("xor.net")

        True

    #**************************************************************************************
    def Train(self):
        from fann2 import libfann
        
        connection_rate = self.ui.connectionRateSpinBox.value()
        learning_rate = self.ui.learningRateSpinBox.value()
        num_input = self.nrinputs
        num_hidden = self.ui.layersSpinBox.value()
        neurons_per_layer = self.ui.neuronsSpinBox.value()
        num_output = self.nroutputs
        
        netparams=[]
        netparams = netparams + [num_input]
        netparams = netparams + [neurons_per_layer]*num_hidden
        netparams = netparams + [num_output]
        

        desired_error = self.ui.desiredErrorSpinBox.value()
        max_iterations = self.ui.maxIterSpinBox.value()
        iterations_between_reports = 10000
        
        ann = libfann.neural_net()
        ann.create_shortcut_array(tuple(netparams))
        ann.set_learning_rate(learning_rate)
        ann.set_train_error_function(libfann.ERRORFUNC_LINEAR)
        self.train_data = libfann.training_data()
        self.train_data.set_train_data((self.inputvals-self.in_min)/self.in_scale,(self.outputvals-self.out_min)/self.out_scale)
        self.train_data.shuffle_train_data()
        tic=time.time() 
        neurons_between_reports = 2
        ann.cascadetrain_on_data(self.train_data,neurons_per_layer,neurons_between_reports, desired_error)
        toc = time.time()-tic
        print ("%i iterations in %.0fs (%0.f iterations/second)\n" % (max_iterations,toc,max_iterations/toc))
        self.ann = ann
        True    

    #**************************************************************************************
    def Save(self):
        self.ann.save("currneuralnet.net")
        
    #**************************************************************************************
    def Load(self):
        if "self.ann" not in locals():
            from fann2 import libfann
            self.ann = libfann.neural_net()
        self.ann.create_from_file("currneuralnet.net")
    

    #**************************************************************************************
    def Test(self):
        inputvals = [""]*self.nrinputs
        nrrows = self.ui.testDataTable.rowCount()
        for i in range(nrrows):
            for j in range(self.nrinputs):
                #inputvals[j]= float(self.ui.testDataTable.item(i,j).text())
                inputvals[j]= (float(self.ui.testDataTable.item(i,j).text())-self.in_min)/self.in_scale
            #result = np.array(self.ann.run(inputvals/self.scalefactor))*self.scalefactor
            #result = np.array(self.ann.run(inputvals))
            outputresults = np.array(self.ann.run(inputvals))
            #result = outputresults*self.scalefactor/2.0
            result = (outputresults*self.out_scale)+self.out_min
            #result = outputresults
            for k in range(self.nroutputs):
                self.ui.testDataTable.item(i,j+k+1).setText(str(result[k]))


    #**************************************************************************************
    def Match(self):
        trainin=np.transpose(self.trainingdata[:self.nrinputs])
        trainout=np.transpose(self.trainingdata[self.nrinputs:])
        testin=np.transpose(self.testdata[:self.nrinputs])
        testout=np.transpose(self.testdata[self.nrinputs:])
        rangetrainsets=range(len(trainin))
        rangeinputs=range(self.nrinputs)
        rangetestsets=range(len(testin))
        
        maxdiffFe = 1000
        maxdiffBe = 1000
        maxdiffNi = 1000
        for i in rangetestsets:
            diff = np.abs((trainin -testin[i]))
            difft = np.transpose(diff)
            Fe=np.where((difft[0]<maxdiffFe))
            Be=np.where((difft[1]<maxdiffBe))
            Ni=np.where((difft[2]<maxdiffNi))
            A1=np.intersect1d(Ni,np.intersect1d(Fe, Be))
            

            if len(A1)<1:
                A1=np.concatenate((Fe,Be,Ni),1)[0]
            tr=trainout[A1]            
            df=diff[A1]
            mindiff = np.sum(diff[A1],1)
            min_idiff=np.argmin(mindiff)
            min_i=A1[min_idiff]
            for k in range(self.nroutputs):
                self.ui.testDataTable.item(i,self.nroutputs+k).setText(str(trainout[min_i][k]))
            
        diff = np.abs((trainin -testin[0]))
        f=open("D:\\home\\deon\\Documents\\PhD\\Models\\Fiducial_Marker\\Marker10\\Measurements\\ENGINX\\Mantid_out\\testfile.txt","w")
        for i in rangetrainsets:
            for j in rangeinputs:
                f.write(str(diff[i][j])+"\t")
            f.write("\n")
        f.close()
        mindiff = np.sum(diff,1)
        min_i=np.argmin(mindiff)
        
        
        res = float(self.ui.desiredResolutionEdit.text())
        testvals = [""]*self.nrinputs
        trainginput=np.array(self.trainingdata[:self.nrinputs])
        trainingoutput=np.transpose(self.trainingdata[self.nrinputs:]) 
        idx = [""]*self.nrinputs
        for i in range(self.nrrows_testdata):
            for j in range(self.nrinputs):
                testvals[j]= float(self.ui.testDataTable.item(i,j).text())
                testval = float(self.ui.testDataTable.item(i,j).text())
                idx[j]=np.where((trainginput[j]>=(testval-res)) & (trainginput[j]<=(testval+res)))[0]
                True
            b=np.intersect1d(idx[0],idx[1])
            True
            
                
        True
        
        

