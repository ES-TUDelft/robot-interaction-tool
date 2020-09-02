# I. Linux Installation guide

## I.1. Python 2.7

* Install [Python 2.7](https://www.python.org/downloads/release/python-2717/)

`$ sudo apt-get install python2 libpython2.7`

<!--
## I.2. NAOqi for Python

* Install [PYNAOqi 2.5 for Python](http://doc.aldebaran.com/2-5/dev/python/install_guide.html):
   
   * Go to: [https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares)
   * Click on Old Pepper SDK and download **Pepper SDK 2.5.10 - Python 2.7 SDK** under LINUX

* Open a terminal and do the following:

`$ cd ~/Downloads`

`$ tar -xvzf pynaoqi-python2.7-2.5.7.1-linux64.tar.gz`

`$ mv pynaoqi-python2.7-2.5.7.1-linux64 ~/Documents`

* Tip: add NAOqi to the PYTHONPATH by appending the following line to the end of the *.bashrc* file as follows: *(change naoqi path to where you stored **pynaoqi-python2.7-2.5.7.1-linux64**)*

`$ vim ~/.bashrc`

`export PYTHONPATH=${PYTHONPATH}:/home/YOUR_USERNAME/Documents/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages`

`$ source ~/.bashrc`

* Test that NAOqi is imported correctly:

`$ python2`

`>>> import naoqi`

* In case of errors, verify your PYTHONPATH or check Softbank documentation at: [http://doc.aldebaran.com/2-5/dev/python/install_guide.html](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)
-->

## I.2. Install PIP (for Python 2.7) and other dependencies

* Open a terminal

`$ sudo apt-get install curl`

`$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`$ sudo python2 get-pip.py`

`$ sudo apt-get install -y python-dev`

* Now use pip to install the project requirements:

`$ cd ~/Documents/robot-interaction-tool`

`$ pip install -r requirements.txt`

    * If you get errors related to the "qi" library, try installing it from terminal (i.e., $ pip install qi).
    * If you get errors related to "pip" check if /home/YOUR_USER/.local/bin is in the PATH or add it in ~/.bashrc
    

## I.3. Install qt5

* Open a terminal:

`$ sudo apt-get install qt5-default`

<!--
`$ sudo add-apt-repository ppa:beineri/opt-qt-5.13.2-bionic`

`$ sudo apt-get update`

`$ apt-get install -y build-essential libgl1-mesa-dev qt513-meta-minimal qt513svg`

== Qt should be now in: /opt/qt513
-->


## I.4. Install SIP 4.19.x

* Go to https://www.riverbankcomputing.com/software/sip/download and select **sip-4.19.23**

* Open a new terminal and cd to the downloads folder (or to where you dowloaded sip)

`$ cd Downloads`

`$ tar -xvzf sip-4.19.23.tar.gz`

`$ cd sip-4.19.23`

`$ python configure.py --sip-module=PyQt5.sip`

`$ make -j 4`

`$ sudo make install`

`$ pip list`

==> you should see PyQt5-sip in the list

## I.5. Install PyQt5

* Dowload **PyQt5-5.13.2.tar.gz** from (https://www.riverbankcomputing.com/software/pyqt/download5)

  * If v5.13.2 is missing, you can find it from here: [PyQt5-5.13.2](https://github.com/ES-TUDelft/robot-interaction-tool/tree/master/docs/extra)

* Open a new terminal and cd to the downloads folder (or to where you dowloaded PyQt)

`$ cd Downloads`

`$ tar -xvzf PyQt5-5.13.2.tar.gz`

`$ cd PyQt5-5.13.2`

<!-- `$ LD_LIBRARY_PATH=/opt/qt513/lib` --qmake=/opt/qt513/bin/qmake -->

`$ python configure.py --confirm-license --disable=QtNfc --qmake=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake QMAKE_LFLAGS_RPATH=`

   * If you get errors related to "qmake", check where it is located using: *$ qmake qt=5 --version*

`$ make -j 4`

`$ sudo make install`

* If you see **errors** during the install procedure, try to address them OR repeat steps 4-6 (i.e., and make sure there are no errors after performing each step) OR check **Section V**.

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
