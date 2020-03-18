# Robot Interaction Tool

This project provides a prototyping tool for designing communicative (expressive) behaviors for social robots. The current version is compatible with the [Pepper Robot](https://www.ald.softbankrobotics.com/en/robots/pepper).

The tool was tested on MAC and Linux.

## Requirements
[![Ubuntu 18.04](https://img.shields.io/badge/Ubuntu-18.04%20LTS-orange)](https://www.ubuntu.com/download/desktop)
[![Python 2.7](https://img.shields.io/badge/Python-2.7.14-yellow.svg)](https://www.python.org/downloads/)
[![NAOqi 2.5](https://img.shields.io/badge/NAOqi-2.5-blue.svg)](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)
[![PyNaoQi 2.5](https://img.shields.io/badge/PyNaoqi-2.5.5.5-green.svg)](http://doc.aldebaran.com/2-5/dev/community_software.html#retrieving-software)
[![PyQt 5.13.x](https://img.shields.io/badge/PyQt-5.x.x-brightgreen.svg)](https://pypi.org/project/PyQt5/5.9.2/)
[![PyYAML 5.x](https://img.shields.io/badge/PyYAML-5.x-blue)](https://github.com/yaml/pyyaml)

To use the tool, clone the repository (e.g., in the Documents folder) and, if you have all the requirements installed, launch the interface:

`cd ~/Documents`

`$ git clone https://github.com/ES-TUDelft/robot-interaction-tool.git`

`cd ~/Documents/robot-interaction-tool`

`$ python main.py`

***Note***: This repository is being updated on a regular basis. Use ***git pull*** to integrate the latest changes.

## I. Linux: Installation guide
First install [Python 2.7](https://www.python.org/downloads/release/python-2717/) and [NAOqi 2.5](http://doc.aldebaran.com/2-5/dev/python/install_guide.html).

* Tip: append NAOqi to the PYTHONPATH:

`$ vim ~/.bashrc`

==> go the end of the file and add this line (change naoqi path to where you stored *naoqi-sdk-2.5.5.5-linux64*):

`export PYTHONPATH=${PYTHONPATH}:/path_to_naoqi-sdk-2.5.5.5-linux64/lib/python2.7/site-packages`

`$ source ~/.bashrc`

Then, proceed with installing the following:

### 1. Install PIP and other dependencies

* Open a terminal

`$ sudo apt-get update`

`$ sudo apt-get install -y python-pip python-dev`

`$ pip install enum34`

### 2. Install PyYAML

`$ pip install PyYAML`

### 3. Install MONGO DB

`$ pip install pymongo`

### 4. Install qi

* LibQi Python bindings for NAOqi

`$ pip install qi`

### 5. Spotify integration

* Install SpotiPy: a python library for the Spotify web api.

`$ pip install spotipy`

* For setting up spotify client id (and secret) see Sec. II.
    
* ***If you experience issues with this library***, uninstall the pip version then install it from the source as follows:

`$ pip uninstall spotipy`

`$ git clone https://github.com/plamere/spotipy.git`

`$ python setup.py install`

***

### ***Note***: 
*Before proceeding with the next steps, check if you already have **PyQt5** installed on your system.* 
*For example, try these commands in a terminal:*
    
`$ python`
    
`>> import PyQt5`
    
*If the import is successful (i.e., no errors), go to **Step 9**; otherwise, continue.*

### 6. Install qt513

* Open a terminal:

`$ sudo add-apt-repository ppa:beineri/opt-qt-5.13.2-bionic`

`$ sudo apt-get update`

`$ apt-get install -y build-essential libgl1-mesa-dev qt513-meta-minimal qt513svg`

==> Qt should be now in: /opt/qt513


### 7. Install SIP 4.19.x

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


### 8. Install PyQt5

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

### 9. Launch the Interaction Tool

Once you finish installing all the requirements, open a terminal and cd to where you want to save the git repository:

`$ git clone https://github.com/ES-TUDelft/robot-interaction-tool.git`

`$ cd robot-interaction-tool`

`$ python main.py`

The user interface should run now, good luck!

<div align="center">
  <img src="interaction_manager/ui/ui_view.png" width="500px" />
</div>

---

## II. Setting up Spotify

TODO!

---

## III. Known installation issues: Qt not found!
If you experience issues related to Qt, try the following:

* Download Qt 5.13.2 for linux from: https://download.qt.io/official_releases/qt/5.13/5.13.2/ 
* Open a terminal:

`$ cd ~/Downloads`

`$ chmod +x qt-opensource-linux-x64-5.13.2.run`

`$ ./qt-opensource-linux-x64-5.13.2.run`
