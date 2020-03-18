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

* Go to https://developer.spotify.com/dashboard/login (create an account or login to yours)

* Click on "Create a Client ID" and fill in the required fields (e.g., RobotInteractionTool for the app name)

* Click on the app you just created and go to "Edit Settings". In the ***Redirect URIs*** field add http://localhost:8080/callback/ and click on ***SAVE*** (bottom left).

* Copy the app's the ***Client ID*** and ***Client Secret*** to the ***config.yaml*** file in "robot-interaction-tool/interaction_manager/properties" OR in this properties directory, create a new file named ***spotify.yaml*** and add the following:

        spotify:
            username: YOUR_USER_NAME
            client_id: YOUR_CLIENT_ID
            client_secret: YOUR_CLIENT_SECRET
            redirect_uri: http://localhost:8080/callback/
            
* The ***username*** from the previous step is your personal **Spotify** username (found in your profile: https://www.spotify.com/).

* To connect to the spotify web api for the first time, you'll need a running server listening to 8080 port. You can use the server.js provided by this repository (you need to install node.js first: https://nodejs.org/en/download/) or create your own.

`$ cd ~/Documents/robot-interaction-tool`

`$ node es_common/server.js`

* Now, launch the interaction tool GUI (as in Sec. I-8) and click on the "Spotify" button (in the toolbar).

* You'll be presented with a connection dialog. You can either use the default settings (that you previously put in the config.yam or spotify.yaml) or enter new ones.

* Click on the ***Connect*** button. 

        * If this is the first time you connect to Spotify (i.e., there is no cache), you will be redirected to a web browser.
        * Just *copy the URL* shown on the webpage and *paste* it in the terminal running the tool then press Enter.
        * The URL should be similar to this but longer (DO NOT USE IT, it is just an example):
            - http://localhost:8080/callback/?code=BtmyiHfVlKvGtO4mgwYJQKKOUWEeNTRm22CXrAnTRp...

* If it's successful, you'll see your playlists and tracks. Click "OK" to save the setup.

* To play a song (e.g., using the test button or the mini-player panel in the main interface), you will need an active device (i.e., a Spotify Player) that is running on either your browser or PC/Phone.

* ***NOTE:*** When the player is not able to start a song, it means the device is not active. Just refresh your Spotify Player browser or the desktop app. 

---

## III. Known installation issues: Qt not found!
If you experience issues related to Qt, try the following:

* Download Qt 5.13.2 for linux from: https://download.qt.io/official_releases/qt/5.13/5.13.2/ 
* Open a terminal:

`$ cd ~/Downloads`

`$ chmod +x qt-opensource-linux-x64-5.13.2.run`

`$ ./qt-opensource-linux-x64-5.13.2.run`
