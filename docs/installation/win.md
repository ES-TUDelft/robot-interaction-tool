# II. Windows Installation guide

*These steps are to guide throught the installation process. If you encounter some errors, try to modify the default paths to fit what you have on your machine!*

## II.1. Visual Studio

* Install [Visual Studio](https://visualstudio.microsoft.com/vs/community/)

   * In the Workloads, select "Python development" and enable "Python native development tools" only
   
* Install [Microsoft Visual C++ Redistributable for Visual Studio (x86)](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
   
* Optional: Install [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)


## II.2. Python 2.7

* Install [Python 2.7 32-bits](https://www.python.org/downloads/release/python-2717/) (select "Windows x86 MSI installer")

* Verify that your system recognizes python: open a command prompt and try

`$ python`

==> **Note**: you may need to manually add python to your system **PATH** by editing the system environment variables and appending: C:\Python27; C:\Python27\Lib\site-packages; C:\Python27\Scripts to the Path variable.

## II.3. NAOqi for Python

* Download Pynaoqi (pynaoqi-python2.7-2.5.7.1-win32-vs2013) for Windows:
   * Go to: [https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares)
   * Click on Old Pepper SDK and download **Pepper SDK 2.5.10 - Python 2.7 SDK** under WINDOWS
   
* Follow the installation instructions (for Windows) from SoftbankRobotics http://doc.aldebaran.com/2-5/dev/python/install_guide.html#python-install-guide
   * extract pynaoqi (downloaded in the previous step) to your Documents folder (or somewhere else)
   * modify your user environment variables by adding the following:
    
         Variable name: PYTHONPATH
         Variable value: C:\Users\YOUR_USER_NAME\Documents\pynaoqi-python2.7-2.5.7.1-win32-vs2013\lib; C:\Python27\Lib\site-packages
   
* Open a new command prompt and try the following:

`$ python`

`>>> import naoqi`


## II.4. Install PIP and other dependencies

* Open a command prompt and install pip:

`$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`$ python get-pip.py`

* Use pip to install the project requirements:

`$ cd robot-interaction-tool`

`$ pip install -r requirements.txt`

   * ==> if pip is not recognized, try: `python -m pip install -r requirements.txt`

  * If you get errors related to the "qi" library, try to install it separately (e.g., pip install qi).

---

### **NOTE**
* Before performing Steps 5-7, try the following:

* download PyQt5 build from: https://github.com/ES-TUDelft/PyQt5-Windows.git

* Copy **ONLY "PyQt5" folder** to C:\Python27\Lib\site-packages

* Add the following to your environment variables:
   * Variable name: QT_QPA_PLATFORM_PLUGIN_PATH
   * Variable value: C:\Python27\Lib\site-packages\PyQt5\plugins\platforms

* Make sure that C:\Python27\Lib\site-packages AND C:\Python27\Scripts are in your PATH environment variable

* Try Step II.8: if it works then you're good to go; otherwise, continue with step II.5.

---

## II.5. Qt 5.13

* Install [Qt 5.13.2](https://download.qt.io/official_releases/online_installers/) from https://download.qt.io/official_releases/online_installers/. When asked to select components, deselect everything (to reduce the size of the required files) and select: MSVC 2015 & 2017 32-bits and 64-bits, and MinGW 32 and 64-bits. 


## II.6. SIP 4.19

* Download SIP-4.19.23 from https://www.riverbankcomputing.com/software/sip/download 

* Unzip the file

* Open a **Visual-Studio Developer Command prompt** and cd to where you downloaded SIP (verify the path in all the following commands):

`$ "C:\Qt\5.13.2\msvc2017\bin\qtenv2.bat"`

`$ "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars32.bat"`

`$ cd \Users\YOUR_USER_NAME\Downloads\sip-4.19.23`

`$ python configure.py --sip-module PyQt5.sip`

`$ nmake`

`$ nmake install`

## II.7. PyQt5-5.13.2
* Download PyQt5-5.13.2 from https://www.riverbankcomputing.com/software/pyqt/download5 

  * If v5.13.2 is missing, you can find it from here: [PyQt5-5.13.2](https://github.com/ES-TUDelft/robot-interaction-tool/tree/master/docs/extra)

* unzip the file

* In the same **Visual-Studio Developer Command prompt** as step II.6 do the following:

`$ cd \Users\YOUR_USER_NAME\Downloads\PyQt5-5.13.2`

`$ python configure.py --confirm-license --no-designer-plugin --no-qml-plugin --assume-shared --disable=QtNfc --qmake=C:\Qt\5.13.2\msvc2017\bin\qmake.exe`

`$ nmake`

`$ nmake install`
 
 * To make sure that PyQt5 is installed correctly, try the following:

`$ python`

`>>> from PyQt5 import QtWidgets`

===> If you have errors, this means that PyQt5 is not installed correctly! Check [**Annex A**](#a-known-installation-issues) for known issues!


---

# A. Known Installation Issues

## a. ImportError: libQt5Widgets.so.5 not found!

This means that your newly installed library is not in the system path (i.e., it may be in the local usr path). 

You have to do it manually by adding two lines to local.conf as such (note that adding the path to local lib should suffice, but you can add path to qt513 to be sure):

==> I’m assuming you installed qt513 at: /opt/qt513:

* OPTION A): do it using echo

`$ echo “/usr/local/lib\n/opt/qt513/lib” > /etc/ld.so.conf.d/local.conf`

`$ sudo ldconfig`
   
* OPTION B): create a new file and add two lines to it as such:

`$ sudo vim /etc/ld.so.conf.d/local.conf`

`/usr/local/lib`

`/opt/qt513/lib`

*(P.S.: to exit vim and save the changes do: ESC :wq!)*

`$ sudo ldconfig`

* Now that you added the path to the newly created library, try to import PyQt5 again:

`$ python`

`>>> import PyQt5`

==> This should not return any errors. If it does, try step III.b!


## b. Qt not found!

If you experience issues related to Qt, try the following:

* Download Qt 5.13.2 for linux from: https://download.qt.io/official_releases/qt/5.13/5.13.2/ 
* Open a terminal:

`$ cd ~/Downloads`

`$ chmod +x qt-opensource-linux-x64-5.13.2.run`

`$ ./qt-opensource-linux-x64-5.13.2.run`

## c. Spotify integration

* ***If you experience issues with Spotipy*** (python library for the Spotify web api), uninstall the pip version then install it from the source as follows:

`$ pip uninstall spotipy`

`$ git clone https://github.com/plamere/spotipy.git`

`$ cd spotipy`

`$ python setup.py install`
