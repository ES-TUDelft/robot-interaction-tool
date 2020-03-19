# Design Tool for Prototyping Human-Robot Communication
# - User Manual -

---

In this document we will go through each part of the prototyping tool’s main user interface and explain its components.

<div align="center">
  <img src="resources/fig_mainUIAnnotated.png" width="500px" />
  <em>Figure 1: Preview of the user Interface for prototyping interactive dialogues with social robots. (A) the top menu bar; (B) list of available dialogue blocks; (C) design panel for building the dialogue flow; (E) panel for displaying the logs, the simulation progress and the music player controls.</em>
</div>

## 1. Top Menu

The top menu bar (Fig. 1.A) contains the following buttons, from left-to-right:

* **Save**: for saving the designs;
* **Copy**: copies the selected design block;
* **Paste Parameters**: pastes the design parameters to the selected block;
* **Clear**: deletes all blocks and clears the scene;
* **Connect**: opens a dialog GUI for connecting to the robot (Fig 2-Left);
* **Disconnect**: disconnects from the robot;
* **Wake Up**: to wake the robot up;
* **Rest**: to put the robot to rest;
* **Vol+** and **Vol-**: to increase or decrease the volume of the robot’s speakers;
* **Play**: to play the design and interact with the robot;
* **Stop**: to stop the current interaction;
* **Spotify**: opens a dialog GUI to connect to Spotify (music) web service (Fig. 2-Right);
* **Simulate**: to simulate the interaction (without being connected to a physical robot);
* **Import Design**: similar to **Export Design** (in the File menu), it opens a dialog GUI to import/export design blocks (Fig. 3).

<div align="center">
  <img src="resources/fig_connect.png" width="500px" />
  <em>Figure 2: Dialog GUI for managing the connection to the robot (left) and the connection to Spotify web service (right).</em>
</div>

<div align="center">
  <img src="resources/fig_importExport.png" width="500px" />
  <em>Figure 3: Dialog GUIs for importing (left) and exporting (right) designs.</em>
</div>

## 2. Keyboard Shortcuts

Here’s a list of useful keyboard shortcuts:

* **Ctrl+Z**: Undo;
* **Shift+Ctrl+Z**: Redo;
* **Ctrl+C**: Copy;
* **Ctrl+V**: Paste;
* **Del**: Delete selected;
* **Shift+Ctrl+Del**: Clear scene (delete all);
* **Ctrl+S**: Save design.

## 3. Interaction Blocks Panel

The blocks panel (Fig. 1.B) contains the list of available blocks that the user can drag to the design panel when building an interactive dialogue with the robot.

## 4. Design Panel

The design panel (Fig. 1.C) is the space for designing the whole interaction. The blocks (1.3) are dropped in this panel and can be connected to one another with edges. Users can click on a block socket (i.e., starting point of the edge) and click again on a socket from another block (i.e., end point of the edge), as illustrated in 4. Users can also edit the properties and parameters of the blocks, which we will discuss in the following.

<div align="center">
  <img src="resources/fig_mainUIWithBlocks.png" width="500px" />
  <em>Figure 4: Design space with connected interaction blocks.</em>
</div>

### 4.1. Block Properties

When the user clicks on a block’s edit icon (Fig. 5), an dialogue GUI appears for setting the blocks properties such as the robot’s message, action, behaviors, dialogue flow (i.e., topic) and screen display.

<div align="center">
  <img src="resources/fig_editDialog.png" width="500px" />
  <em>Figure 5: Dialog GUI for editing the properties of the selected block. From left to right: tab for setting the robot message (i.e., speech act) and action (if any); tab for setting the robot’s gestures; tab for setting the dialogue topic (if the block pattern contains one, e.g., question pattern); tab for setting the robot tablet (i.e., screen) properties.</em>
</div>

### 4.2. Block Parameters
When the user clicks on a block’s parameter icon (Fig. 6), an dialogue GUI appears for setting the blocks parameters such as the robot’s gestures, gaze, proxemics, voice and eye color. When connected to a physical robot, the user can test the parameter settings (i.e., by clicking on the ’Test’ button). The user can also apply the settings to the selected block (i.e., by clicking on the apply button) or to all blocks in the scene (i.e., by clicking on the apply all).

<div align="center">
  <img src="resources/fig_parameters.png" width="500px" />
  <em>Figure 6: Dialog GUI for modifying the parameters of the selected block. From left to right: tab for setting the type of the robot’s gestures, gaze, and proxemics; tab for setting the robot’s voice (i.e., pitch, speed and prosody); and tab for setting the robot’s eye color.</em>
</div>

## 5. Bottom-Left Panel
The bottom left panel (Fig. 1-D) of the user interface is composed of three tabs.  The first tab  displays the system logs (Fig. 7-Left). The second tab is active when the simulator is launched (Fig. 7-Middle). The third tab contains a player for manually controlling the music (Fig. 7-Right).

<div align="center">
  <img src="resources/fig_logs.png" width="500px" />
  <em>Figure 7: Panel for displaying the system logs (left); the simulator (middle); and the music player (right).</em>
</div>
