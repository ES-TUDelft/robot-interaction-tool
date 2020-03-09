cd ~/path-to/robot-interaction-tool
unset PYTHONPATH; pyrcc5 -o interaction_manager/view/resources_rc.py interaction_manager/ui/hre_resources/resources.qrc; 
pyuic5 -x interaction_manager/ui/dialogmainwindow.ui -o interaction_manager/view/ui_dialog.py -x; source ~/.bash_profile

unset PYTHONPATH; pyuic5 -x interaction_manager/ui/editblockdialog.ui -o interaction_manager/view/ui_editblock_dialog.py -x; source ~/.bash_profile
unset PYTHONPATH; pyuic5 -x interaction_manager/ui/connectiondialog.ui -o interaction_manager/view/ui_connection_dialog.py -x; source ~/.bash_profile
pyuic5 -x ui/editblockdialog.ui -o hre_view/ui_editblock_dialog.py -x
pyuic5 -x ui/confirmationdialog.ui -o view/ui_confirmation_dialog.py -x
pyuic5 -x ui/dbconnectiondialog.ui -o view/ui_db_connection_dialog.py -x


