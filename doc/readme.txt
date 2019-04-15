ScanManipulator *should* work on Linux and macOS, but this has not been tested. All development was done on a Windows 64-bit environment.
There may be many ways to get ScanManipulator up and running, this is a suggestion:

Install Anaconda Python 3.7 64-Bit from here: https://www.anaconda.com/distribution/
Download (unofficial) library wheels from here: http://www.lfd.uci.edu/~gohlke/pythonlibs
Newer libraries should also probably work if the API does not change
Install the libraries using pip (probably not such a good idea to mix pip with conda, but this was the easiest)

library		wheel
-------		-----
pyface		pyface-6.0.0-py3-none-any.whl
pyQt		PyQt4-4.11.4-cp37-cp37m-win_amd64.whl
matplotlib	matplotlib-3.0.3-cp37-cp37m-win_amd64.whl
yaml		PyYAML-5.1-cp37-cp37m-win_amd64.whl
pywin		pywin32-224-cp37-cp37m-win_amd64.whl
shapely		Shapely-1.6.4.post1-cp37-cp37m-win_amd64.whl
pillow		Pillow-5.4.1-cp37-cp37m-win_amd64.whl
trimesh	
OpenGL		PyOpenGL-3.1.3b2-cp37-cp37m-win_amd64.whl
h5py		h5py-2.9.0-cp37-cp37m-win_amd64.whl
urllib		urllib3-1.24.1-py2.py3-none-any.whl
fann		fann2-1.1.2-cp37-cp37m-win_amd64.whl

Configure the Win32com library for Excel linking:
	In the directory where Python is installed (such as C:\Anaconda3) browse to \Lib\site-packages\win32com\client\ and run the file "makepy.py". A list will pop up. Select "Microsoft Excel x.x Object Library"


