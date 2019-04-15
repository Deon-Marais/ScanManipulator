'''
Created on 05 Mar 2014

@author: Deon
'''
import h5py
import numpy as np
import os


def AddScatter(excel, sheet, left=10, top=10, width=300, height=150, Xaxis="X", Yaxis="Y"):
    from win32com.client import constants as c
    ch = sheet.Shapes.AddChart(XlChartType=c.xlXYScatterLinesNoMarkers, Left=left, Top=top, Width=width, Height=height).Select()
    chrt = excel.ActiveChart
    chrt.Axes()[c.xlValue].HasTitle=True
    chrt.Axes()[c.xlValue].AxisTitle.Text=Yaxis
    chrt.Axes()[c.xlCategory].HasTitle=True
    chrt.Axes()[c.xlCategory].AxisTitle.Text=Xaxis 
    return chrt   

def AddSeries(chrt,xrange,yrange,name):
        chrt.SeriesCollection().NewSeries()
        series = chrt.SeriesCollection(chrt.SeriesCollection().Count)
        series.Format.Line.Weight = 0.5
        series.XValues = xrange
        series.Values = yrange
        series.Name = name    

def ChangeXAxes(chrt_list,xmin, xmax):
    from win32com.client import constants as c
    for ch in chrt_list:
        ch.Axes(c.xlCategory).MinimumScale = xmin
        ch.Axes(c.xlCategory).MaximumScale = xmax
        ch.Axes(c.xlCategory).TickLabels.NumberFormat = "# ##0.0"
        

def ToExcelCol(aList):
    mylist=[]
    for item in aList:
        mylist.append([np.str(item)])
    return tuple(mylist)
     
 
def Xport2Excel(filename):
    f = h5py.File(filename,"r")
    dset = f.get("/")
    hmm_x = dset["/entry1/instrument/detector/hmm_x_corrected"]
    x_stth = dset["/entry1/instrument/detector/x_stth"]
    stth = dset["/entry1/sample/stth"]
    eventrate = dset["/entry1/monitor/bm1_event_rate"]
    counttime = dset["/entry1/data/time"]
    
    numruns = len(hmm_x)
    
   # from win32com.client.gencache import EnsureDispatch 
   # excel = EnsureDispatch("Excel.Application")
   
    from win32com.client import Dispatch 
    excel = Dispatch("Excel.Application")

    from win32com.client import constants as c
    excel.Visible=1
    #excel.ScreenUpdating = False
    wb = excel.Workbooks.Add()
    sh=excel.ActiveSheet
    
    chh = 150
    chw = 300
    chsp = 50
    
    ch_counts = AddScatter(excel, sh, 0*chw+chsp, chsp, chw, chh, Xaxis="2*Theta", Yaxis="Raw Counts")
    ch_count_norm_time = AddScatter(excel, sh, 1*chw+2*chsp, chsp, chw, chh, Xaxis="2*Theta", Yaxis="Counts norm to time")
    ch_count_norm_rate = AddScatter(excel, sh, 2*chw+3*chsp, chsp, chw, chh, Xaxis="2*Theta", Yaxis="Counts norm to event rate")
 
    ch_all_counts = AddScatter(excel, sh, 0*chw+chsp, 2*chsp+1*chh, chw, chh, Xaxis="2*Theta", Yaxis="Raw Counts")
    ch_all_count_norm_time = AddScatter(excel, sh, 1*chw+2*chsp, 2*chsp+1*chh, chw, chh, Xaxis="2*Theta", Yaxis="Counts norm to time")
    ch_all_count_norm_rate = AddScatter(excel, sh, 2*chw+3*chsp, 2*chsp+1*chh, chw, chh, Xaxis="2*Theta", Yaxis="Counts norm to event rate")
 
    ch_list = [ch_counts,ch_count_norm_time,ch_count_norm_rate,ch_all_counts,ch_all_count_norm_time,ch_all_count_norm_rate]   

    sh.Cells(1,1).Value = "stth_all"
    sh.Cells(1,2).Value = "hmm_x_corrected_all"
    sh.Cells(1,3).Value = "hmm_x_normalised_time_all"
    sh.Cells(1,4).Value = "hmm_x_normalised_rate_all"
    
    colperser = 4  
    for run in range(numruns):
        
        sh.Cells(1,(run+1)*colperser+1).Value = "stth = " + str(stth[run])
        sh.Cells(1,(run+1)*colperser+2).Value = "hmm_x_corrected_" + str(stth[run])
        sh.Cells(1,(run+1)*colperser+3).Value = "hmm_x_normalised_time_" + str(stth[run])
        sh.Cells(1,(run+1)*colperser+4).Value = "hmm_x_normalised_rate_" + str(stth[run])
        numvals = len(x_stth[run])
        range_x_stth = sh.Range(sh.Cells(2,(run+1)*colperser+1), sh.Cells(numvals+1,(run+1)*colperser+1))
        range_hmm_x = sh.Range(sh.Cells(2,(run+1)*colperser+2), sh.Cells(numvals+1,(run+1)*colperser+2))
        range_hmm_x_norm_time = sh.Range(sh.Cells(2,(run+1)*colperser+3), sh.Cells(numvals+1,(run+1)*colperser+3))
        range_hmm_x_norm_rate = sh.Range(sh.Cells(2,(run+1)*colperser+4), sh.Cells(numvals+1,(run+1)*colperser+4))
        range_x_stth.Borders(c.xlEdgeLeft).LineStyle = c.xlContinuous

        range_all_x_stth = sh.Range(sh.Cells(run*numvals+2,1), sh.Cells(run*numvals+2+numvals-1,1))
        range_all_hmm_x = sh.Range(sh.Cells(run*numvals+2,2), sh.Cells(run*numvals+2+numvals-1,2))
        range_all_hmm_x_norm_time = sh.Range(sh.Cells(run*numvals+2,3), sh.Cells(run*numvals+2+numvals-1,3))
        range_all_hmm_x_norm_rate = sh.Range(sh.Cells(run*numvals+2,4), sh.Cells(run*numvals+2+numvals-1,4))
        
        
        col_x_stth = ToExcelCol(x_stth[run])
        col_hmm_x = ToExcelCol(hmm_x[run])
        col_hmm_x_norm_time = tuple([[float(col_hmm_x[a][0])/counttime[run]] for a in range(numvals-1)])
        col_hmm_x_norm_rate = tuple([[float(col_hmm_x[a][0])/eventrate[run]] for a in range(numvals-1)])

        range_x_stth.Value = col_x_stth
        range_hmm_x.Value = col_hmm_x
        range_hmm_x_norm_time.Value = col_hmm_x_norm_time
        range_hmm_x_norm_rate.Value = col_hmm_x_norm_rate
        
        range_all_x_stth.Value = col_x_stth
        range_all_hmm_x.Value = col_hmm_x
        range_all_hmm_x_norm_time.Value = col_hmm_x_norm_time
        range_all_hmm_x_norm_rate.Value = col_hmm_x_norm_rate
        
        AddSeries(ch_counts, range_x_stth, range_hmm_x, str(stth[run]))
        AddSeries(ch_count_norm_time, range_x_stth, range_hmm_x_norm_time, str(stth[run]))
        AddSeries(ch_count_norm_rate, range_x_stth, range_hmm_x_norm_rate, str(stth[run]))
    pass

    #excel.ScreenUpdating = True
    range_all_sort = sh.Range(sh.Cells(2,1), sh.Cells(numruns*numvals+2,4))
    range_prim_sort_key = sh.Range(sh.Cells(2,1), sh.Cells(numruns*numvals+2,1))
    range_all_sort.Sort(Key1=range_prim_sort_key, Order1=c.xlAscending, Orientation=c.xlTopToBottom, SortMethod=c.xlPinYin)

    range_all_x_stth = sh.Range(sh.Cells(2,1), sh.Cells(numruns*numvals+1,1))
    range_all_hmm_x = sh.Range(sh.Cells(2,2), sh.Cells(numruns*numvals+1,2))
    range_all_hmm_x_norm_time = sh.Range(sh.Cells(2,3), sh.Cells(numruns*numvals+1,3))
    range_all_hmm_x_norm_rate = sh.Range(sh.Cells(2,4), sh.Cells(numruns*numvals+1,4))

    AddSeries(ch_all_counts, range_all_x_stth, range_all_hmm_x, "All")
    AddSeries(ch_all_count_norm_time, range_all_x_stth, range_all_hmm_x_norm_time, "All")
    AddSeries(ch_all_count_norm_rate, range_all_x_stth, range_all_hmm_x_norm_rate, "All")
    
    minax=round(min(range_all_x_stth.Value)[0]-5,-1) #Will round to closest 10 below
    maxax=round(max(range_all_x_stth.Value)[0],-1) # Will round to closest 10 above
    ChangeXAxes(ch_list,minax,maxax)
   
pass
    
    
    


#********************************************************************************************************
def CreateX_stth(filename):
    f = h5py.File(filename,"a")
    dset = f.get("/")
    x_axis = dset["/entry1/instrument/detector/x_pixel_offset"]
    s2d =  dset["/entry1/instrument/detector/sample_to_detector_distance"][0]
    hmm_x = dset["/entry1/instrument/detector/hmm_x_corrected"]
    stth = dset["/entry1/sample/stth"]
    numruns = len(hmm_x)
    numbins = len(x_axis)

    try :
        f.create_dataset("/entry1/instrument/detector/x_stth", (numruns,numbins), dtype="d")
    except :
        pass
    x_stth = dset["/entry1/instrument/detector/x_stth"]
    idx = range(numbins)
    for runi in range(numruns):
        for i in idx :
            x_stth[runi,i] = np.rad2deg(np.arctan(x_axis[i]/s2d)) + stth[runi]
    f.close()



#********************************************************************************************************
if __name__ == '__main__':
    import sys
    filename = ""
    try : 
        filename = sys.argv[1]
    except :
        print "Usage: " + sys.argv[0] + " <hdf_filename>"
        print "This script will open an hdf file, calculate the stth axis for all the scans and display it in Excel"
        exit()
    CreateX_stth(filename)
    Xport2Excel(filename)
    pass
