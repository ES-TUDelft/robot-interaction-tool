## III. MAC Installation Guide

## III.1. Python 2.7

* Install [Python 2.7](https://www.python.org/downloads/release/python-2717/) 

## III.2. NAOqi for Python

* Install [PYNAOqi 2.5 for Python](http://doc.aldebaran.com/2-5/dev/python/install_guide.html):
   
   * Go to: [https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares)
   * Click on Old Pepper SDK and download **Pepper SDK 2.5.10 - Python 2.7 SDK** under MAC

* Open a terminal and do the following:

`$ cd ~/Downloads`

`$ tar -xvzf pynaoqi-python2.7-2.5.7.1-mac64.tar`

`$ mv pynaoqi-python2.7-2.5.7.1-mac64 ~/Documents`

* Tip: add NAOqi to the PYTHONPATH by appending the following line to the end of the *.bash_profile* file as follows: *(change naoqi path to where you stored **pynaoqi-python2.7-2.5.7.1-mac64**)*

`$ vim ~/.bash_profile`

`export PYTHONPATH=${PYTHONPATH}:/usr/local/lib/python2.7/site-packages`

`export PYTHONPATH=${PYTHONPATH}:/path_to/pynaoqi-python2.7-2.5.7.1-mac64/lib/python2.7/site-packages`

`export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/path_to/pynaoqi-python2.7-2.5.7.1-mac64/lib`

* ==> save the file using ESC:wq!

`$ source ~/.bash_profile`

* Test that NAOqi is imported correctly:

`$ python`

`>>> import naoqi`

* In case of errors, verify that you're not using the default python (e.g., try: $ which python) and set it in your PYTHONPAH or check Softbank documentation at: [http://doc.aldebaran.com/2-5/dev/python/install_guide.html](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)


## III.3. Install PIP and other dependencies

* Open a terminal

`$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`$ python get-pip.py`

* Now use pip to install the project requirements:

`$ pip install -r requirements.txt`

    * If you get errors related to the "qi" library, verify that NAOqi is in the PYTHONPATH.
    

## III.4. Install qt513

* Install [Qt 5.13](https://download.qt.io/official_releases/online_installers/) (select: qt-unified-mac-x64-online.dmg) from https://download.qt.io/official_releases/online_installers/

  * Note that for this step you will need **XCode** to be installed on your machine.

## III.5. Install SIP 4.19.24

* Go to https://www.riverbankcomputing.com/software/sip/download and select **sip-4.19.24**

* Open a terminal and cd to the downloads folder (or to where you dowloaded sip)

`$ cd Downloads`

`$ tar -xvzf sip-4.19.24.tar.gz`

`$ cd sip-4.19.24`

`$ python configure.py -d /usr/local/lib/python2.7/site-packages/`

`$ make`

`$ sudo make install`


## III.6. Install PyQt5

* Dowload **PyQt5-5.13.2.tar.gz** from (https://www.riverbankcomputing.com/software/pyqt/download5)
  
  * If v5.13.2 is missing, you can find it from here: [PyQt5-5.13.2](https://github.com/ES-TUDelft/robot-interaction-tool/tree/master/docs/extra)

* Open a terminal and cd to the downloads folder (or to where you dowloaded PyQt)

`$ cd Downloads`

`$ tar -xvzf PyQt5-5.13.2.tar.gz`

`$ cd PyQt5-5.13.2`

`$ python configure.py -d /usr/local/lib/python2.7/site-packages/ --qmake=/Users/YOUR_USERNAME/Qt/5.13.2/bin/qmake --sip=/usr/local/bin/sip --sip-incdir=../sip-4.19.24/siplib`

* ==> if you encounter any errors, verify the path to Qt 5.13.2 (i.e., where you installed it) and to sip (e.g., *--sip=/Library/Frameworks/Python.framework/Versions/2.7/bin/sip*)

`$ make`

`$ sudo make install`

* If you see **errors** during the install procedure, try to address them OR repeat steps 4-6 (i.e., and make sure there are no errors after performing each step).

`$ pip list | grep 'PyQt5'`

==> you should see PyQt5 in the results

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
