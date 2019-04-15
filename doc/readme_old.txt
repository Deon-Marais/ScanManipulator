ScanMan was initially written using Python2.7

Install Python(x,y): "\\rddiffserver\fileserver\install\development\python\Python(x,y)\Python(x,y)-2.7.5.0.exe"
This includes Pyhton, numpy, pyqt and a few oter libraries in one package. During the installation stage, select to install EVERYTHING

Install pyspec library: "\\rddiffserver\fileserver\install\development\python\libs\pyspec\pyspec-master.zip"
Once it has been unzipped, comment out all the lines in the setup.cfg.win32 file before beginning the installation

Install yaml: "\\rddiffserver\fileserver\install\development\python\libs\yaml"
Copy the folder to "C:\Python27\Lib\site-packages" so that it looks like this: "C:\Python27\Lib\site-packages\yaml"

Configure the Win32com library for Excel linking:
In the directory "C:\Python27\Lib\site-packages\win32com\client" run the file "makepy.py". A list will pop up. Select "Microsoft Excel x.x Object Library"

For Fast Artificial Neuron Network (FANN) installation:
Upgrade the pip installation to something greater than version 6 (pip -V) with: pip install --upgrade pip
Had lots of difficulty to install FANN using the normal pip installation, therefore download the fann wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/#fann2. cp27 is for python version 2.7 and so forth.
If wheel is not installed, do this: pip install wheel
Now install the FANN wheel with: pip install c:\path\to\fann2-1.0.7-cp27-none-win32.whl

64bit instructions
------------------
Install a 64bit Pytjon 2.7.x

Most of the Python (unofficial) wheels are available from http://www.lfd.uci.edu/~gohlke/pythonlibs and also put on the fileserver. Wheels are installed with the command: pip install "c:\path\to\wheelname.whl"
If there are dependancies, add the proxy: pip --proxy xxx.xxx.xxx.xxx:yyyy install "c:\path\to\wheelname.whl"

pip: upgrade pip using: pip --proxy xxx.xxx.xxx.xxx:yyyy install pip --upgrade

pyQT:
PyQt4-4.11.4-cp27-none-win_amd64.whl
PyQtdesignerplugins-1.1-py2.py3-none-any.whl

numpy: numpy-1.9.3+mkl-cp27-none-win_amd64.whl

matplotlib: matplotlib-1.5.0-cp27-none-win_amd64.whl

pywin32 (for clipboard): http://sourceforge.net/projects/pywin32/files/pywin32/Build%20214/
execute the 64bit exe installer

Configure the Win32com library for Excel linking:
In the directory "C:\Python27\Lib\site-packages\win32com\client" run the file "makepy.py". A list will pop up. Select "Microsoft Excel x.x Object Library"

codetools: pip --proxy xxx.xxx.xxx.xxx:yyyy install codetools

h5py: pip --proxy xxx.xxx.xxx.xxx:yyyy install nose
h5py: pip --proxy xxx.xxx.xxx.xxx:yyyy install pkgconfig
pip install c:\path\to\h5py-2.5.0-cp27-none-win_amd64.whl

fann2: fann2-1.0.7-cp27-none-win_amd64.whl

pyYAML: C:\path\to\PyYAML-3.11-cp27-none-win_amd64.whl

pyspec: pyspec-0.2.post0-cp27-none-win_amd64.whl
Also, after installation mpfit (in Lib\site-packages\pyspec) must be updated from the source on github (https://github.com/stuwilkins/pyspec)

scipy: pip --proxy xxx.xxx.xxx.xxx:yyyy install c:\path\to\scipy-0.16.1-cp27-none-win_amd64.whl

Configure the Win32com library for Excel linking:
In the directory "C:\Python27\Lib\site-packages\win32com\client" run the file "makepy.py". A list will pop up. Select "Microsoft Excel x.x Object Library"

Problems were experieced on some machines with VTK6.2.0 and Mayavi 4.4.3. If this happens, use the older versions (VTK 5.10.1 and Mayavi 4.3.1)

vtk: pip --proxy xxx.xxx.xxx.xxx:yyyy install c:\path\to\VTK-6.2.0-cp27-none-win_amd64.whl

mayavi: pip --proxy xxx.xxx.xxx.xxx:yyyy install c:\path\to\mayavi-4.4.3+vtk620-cp27-none-win_amd64.whl

shapely: pip --proxy xxx.xxx.xxx.xxx:yyyy install "c:\path\to\Shapely-1.6.4.post1-cp27-cp27m-win_amd64.whl"

Pillow (replacement for Python Image Library): pip --proxy xxx.xxx.xxx.xxx:yyyy install "c:\path\to\Pillow-5.0.0-cp27-cp27m-win_amd64.whl"

