# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.confirm_widget import Ui_ConfirmWidget
from .ui.error_widget import Ui_ErrorWidget
from .ui.success_widget import Ui_SuccessWidget

# ----------------------------------------------------------------------------
class QuickReviewConfirmWidget(QtGui.QWidget):
    """
    Confirmation widget.
    """
    
    # ------------------------------------------------------------------------
    def __init__(self, quicktime_path, accept_callback, reject_callback):
        """
        Initialize the widget. 
        """
        # first, call the base class and let it do its thing.
        super(QuickReviewConfirmWidget, self).__init__()

        # now load in the UI that was created in the UI designer
        self.ui = Ui_ConfirmWidget() 
        self.ui.setupUi(self)
        
        quicktime_name = os.path.basename(quicktime_path)
        self.ui.version_name.setText(quicktime_name)

        # set up our signal/slot callback
        self.ui.submit_btn.clicked.connect(lambda: accept_callback())
        self.ui.cancel_btn.clicked.connect(lambda: reject_callback())

        self.ui.open_btn.clicked.connect(
            lambda p=quicktime_path: self._open_in_fs(p))

    # ------------------------------------------------------------------------
    @property
    def notes(self):
        """
        Returns the notes for review.
        """

        return self.ui.notes_edit.toPlainText()

    # ------------------------------------------------------------------------
    def _open_in_fs(self, path):
        """
        Show the quicktime in the file system
        """

        # XXX logic grabbed from tankdialog code.

        # get the setting        
        system = sys.platform
        
        # run the app
        if system == "linux2":
            cmd = 'xdg-open "%s"' % path 
        elif system == "darwin":
            cmd = 'open "%s"' % path
        elif system == "win32":
            cmd = 'cmd.exe /C start "Folder" "%s"' % path
        else:
            raise Exception("Platform '%s' is not supported." % system)
        
        exit_code = os.system(cmd)
        if exit_code != 0:
            self._engine.log_error("Failed to launch '%s'!" % cmd)

# ----------------------------------------------------------------------------
class ErrorWidget(QtGui.QWidget):
    """
    Simple error widget with copyable message and close button.
    """

    # ---------------------------------------------------------------------
    def __init__(self, summary, message):
        """
        Initialize the widget.
        """

        super(ErrorWidget, self).__init__()

        # now load in the UI that was created in the UI designer
        self.ui = Ui_ErrorWidget() 
        self.ui.setupUi(self)

        self.ui.summary_lbl.setText(summary)
        self.ui.error_msg.setText(message)
        self.ui.close_btn.clicked.connect(self.close)
        
# -------------------------------------------------------------------------
class QuickReviewSuccessWidget(QtGui.QWidget):
    """
    Success widget. Displays a button to load context in shotgun.
    """

    # ---------------------------------------------------------------------
    def __init__(self, context):
        """
        Initialize the widget.
        """

        super(QuickReviewSuccessWidget, self).__init__()

        self._context = context

        # now load in the UI that was created in the UI designer
        self.ui = Ui_SuccessWidget() 
        self.ui.setupUi(self)
        
        self.ui.open_btn.clicked.connect(self._open_in_sg)
        self.ui.close_btn.clicked.connect(self.close)

    # ---------------------------------------------------------------------
    def _open_in_sg(self):

        url = self._context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url)) 
        self.close()

