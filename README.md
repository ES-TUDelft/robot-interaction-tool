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

## Linux: Installation guide
After installing [Python 2.7](https://www.python.org/downloads/release/python-2717/) and [NAOqi 2.5](http://doc.aldebaran.com/2-5/dev/python/install_guide.html), proceed with installing the following:

### Install qt513

* Open a terminal:

`$ sudo add-apt-repository ppa:beineri/opt-qt-5.13.2-bionic`

`$ sudo apt-get update`

`$ apt-get install -y build-essential libgl1-mesa-dev qt513-meta-minimal qt513svg`

==> Qt should be now in: /opt/qt513


### Install SIP 4.19.x

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


### Install PyQt5

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


### Install PIP

* Open a terminal

`$ sudo apt-get update`

`$ sudo apt-get install python-pip`

### Install PyYAML

`$ pip install PyYAML`

### Install MONGO DB

`$ pip install pymongo`

### Install qi

* LibQi Python bindings for NAOqi

`$ pip install qi`


# Launch the Interaction Tool

Once you finish installing all the requirements, open a terminal and cd to where you saved the git repository:

`$ cd ~/robot-interaction-tool`

`$ python main.py`


<div align="center">
  <img src="hre_ui/ui_view.png" width="500px" />
</div>
