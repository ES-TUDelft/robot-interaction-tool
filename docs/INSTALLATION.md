# I. Linux Installation guide
First install [Python 2.7](https://www.python.org/downloads/release/python-2717/) and [NAOqi 2.5](http://doc.aldebaran.com/2-5/dev/python/install_guide.html).

* Tip: add NAOqi to the PYTHONPATH by appending the following line to the end of the *.bashrc* file as follows: *(change naoqi path to where you stored **naoqi-sdk-2.5.5.5-linux64**)*

`$ vim ~/.bashrc`

`export PYTHONPATH=${PYTHONPATH}:/path_to_naoqi-sdk-2.5.5.5-linux64/lib/python2.7/site-packages`

`$ source ~/.bashrc`

Then, proceed with installing the following:

## 1. Install PIP and other dependencies

* Open a terminal

`$ sudo apt-get update`

`$ sudo apt-get install -y python-pip python-dev`

* Now use pip to install the project requirements:

`$ pip install -r requirements.txt`

    * If you get errors related to the "qi" library, verify that NAOqi is in the PYTHONPATH.

***

### ***Note***: 
*Before proceeding with the next steps, check if you already have **PyQt5** installed on your system.* 
*For example, try these commands in a terminal:*
    
`$ python`
    
`>>> import PyQt5`
    
*If the import is successful (i.e., no errors), go to **Step 5**; otherwise, continue.*

***

## 2. Install qt513

* Open a terminal:

`$ sudo add-apt-repository ppa:beineri/opt-qt-5.13.2-bionic`

`$ sudo apt-get update`

`$ apt-get install -y build-essential libgl1-mesa-dev qt513-meta-minimal qt513svg`

==> Qt should be now in: /opt/qt513


## 3. Install SIP 4.19.x

* Go to https://www.riverbankcomputing.com/software/sip/download and select **sip-4.19.21**

* Open a terminal and cd to the downloads folder (or to where you dowloaded sip)

`$ cd Downloads`

`$ tar -xvzf sip-4.19.21.tar.gz`

`$ cd sip-4.19.21`

`$ python configure.py --sip-module=PyQt5.sip`

`$ make -j 4`

`$ sudo make install`

`$ pip list`

==> you should see PyQt5-sip in the list

## 4. Install PyQt5

* Dowload **PyQt5-5.13.2.tar.gz** from (https://www.riverbankcomputing.com/software/pyqt/download5)

* Open a terminal and cd to the downloads folder (or to where you dowloaded PyQt)

`$ cd Downloads`

`$ tar -xvzf PyQt5-5.13.2.tar.gz`

`$ cd PyQt5-5.13.2`

`$ LD_LIBRARY_PATH=/opt/qt513/lib python configure.py --confirm-license --disable=QtNfc --qmake=/opt/qt513/bin/qmake QMAKE_LFLAGS_RPATH=`

`$ make -j 4`

`$ sudo make install`

`$ pip list | grep 'PyQt5'`

==> you should see PyQt5 in the results

## 5. Launch the Interaction Tool

Once you finish installing all the requirements, open a terminal and cd to where you want to save the git repository:

`$ git clone https://github.com/ES-TUDelft/robot-interaction-tool.git`

`$ cd robot-interaction-tool`

`$ python main.py`

The user interface should run now, good luck!

<div align="center">
  <img src="user-manual/resources/fig_mainUI.png" width="500px" />
</div>


---

# II. Known installation issues: 

## a. Qt not found!

If you experience issues related to Qt, try the following:

* Download Qt 5.13.2 for linux from: https://download.qt.io/official_releases/qt/5.13/5.13.2/ 
* Open a terminal:

`$ cd ~/Downloads`

`$ chmod +x qt-opensource-linux-x64-5.13.2.run`

`$ ./qt-opensource-linux-x64-5.13.2.run`

## b. Spotify integration

* ***If you experience issues with Spotipy*** (python library for the Spotify web api), uninstall the pip version then install it from the source as follows:

`$ pip uninstall spotipy`

`$ git clone https://github.com/plamere/spotipy.git`

`$ cd spotipy`

`$ python setup.py install`
