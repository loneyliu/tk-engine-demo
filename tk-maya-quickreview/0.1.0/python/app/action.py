# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

from collections import namedtuple
import datetime
import os
import threading

import maya.cmds as cmds

import sgtk
from sgtk.platform.engine import show_global_busy, clear_global_busy

from .widgets import (
    ErrorWidget,
    QuickReviewConfirmWidget, 
    QuickReviewSuccessWidget,
)

# ----------------------------------------------------------------------------

# quick object to hold info about a generated quicktime
Quicktime = namedtuple('Quicktime', [
        'success', 
        'error_msg',
        'frame_count',
        'frame_range',
        'first_frame',
        'last_frame',
        'path',
])

# ----------------------------------------------------------------------------
class QuickReviewAction(object):

    # ------------------------------------------------------------------------
    def __init__(self, app):
        """
        Init the action with an app instance and optional quicktime object.
        """

        self._app = app
        self._name = "Quick Review"
        self._quicktime = None

    # ------------------------------------------------------------------------
    def busy(self, message):
        """
        Returns a busy context manager for this action.
        """

        return ActionBusy(self.name, message)

    # ------------------------------------------------------------------------
    def execute(self):
        """Execute this action."""

        # go ahead and generate the quicktime for review
        with self.busy("<br>Generating quicktime..."):
            quicktime_path = self._get_quicktime_path() 
            self.quicktime = _generate_quicktime(quicktime_path) 

        # make sure the quicktime was successfully generated
        if not self._validate_quicktime():
            summary = "<b>{n}</b> encountered an <b>Error</b>!".format( 
                n=self.name)
            message = "Oops! Unable to generate the quicktime.\n\n" + \
                      "Error: {em}\n\n".format(em=self.quicktime.error_msg) + \
                      "Please contact your pipeline team for assistance."
            self.app.log_error(message)
            self.app.engine.show_dialog(self.name, self.app, ErrorWidget, 
                summary, message)
            return

        # show the confirmation dialog
        self._confirm_widget = self.app.engine.show_dialog(self.name, self.app,
            QuickReviewConfirmWidget, quicktime_path, self._upload,
            self._rejected) 

    # ------------------------------------------------------------------------
    @property
    def app(self):
        """
        Returns the app instance for this action.
        """
        return self._app

    # ------------------------------------------------------------------------
    @property
    def name(self):
        """
        Returns the name of this action.
        """
        return self._name

    # ------------------------------------------------------------------------
    @property
    def quicktime(self):
        """
        Returns the generated quicktime info for this action.
        """
        return self._quicktime

    # ------------------------------------------------------------------------
    @quicktime.setter
    def quicktime(self, info):
        """
        Sets the quicktime info for this action.
        """
        self._quicktime = info

    # ------------------------------------------------------------------------
    def _cleanup(self):
        """
        Removes the quicktime.
        """

        if not self.quicktime:
            return
        
        path = self.quicktime.path
    
        # try our best to clean up the path
        try:
            os.remove(path)
        except os.error as e:
            self.app.log_error(
                "Unable to remove unused quicktime: {p}".format(p=path))
        else:
            self.app.log_info("Removed unused quicktime: {p}".format(p=path))

    # -------------------------------------------------------------------------
    def _get_quicktime_path(self):
        """
        Returns a destination path for the quicktime. 
        """

        # get a template object describing the file pattern
        quicktime_template = self.app.get_template("quicktime_template")
        
        # now ask our current context (current shot, current asset etc)
        # to resolve itself into a set of fields suitable for the 
        # given path template
        fields = self.app.context.as_template_fields(quicktime_template)
        
        # in addition to the fields defined by the context, we also need 
        # to populate a timestamp field
        fields["timestamp"] = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M")
        
        # and now we can compute the path
        return quicktime_template.apply_fields(fields)

    # ------------------------------------------------------------------------
    def _rejected(self):
        """
        Clean up the unused quicktime and dismiss the confirmation widget.
        """

        self._cleanup()
        self._confirm_widget.close()
    
    # ------------------------------------------------------------------------
    def _upload(self):
        """
        Creates a new version entity and uploads the quicktime for review.
        """

        self._confirm_widget.close()

        with self.busy("<br>Uploading quicktime for newly created version..."):

            notes = self._confirm_widget.notes
            
            # now create a version record in Shotgun
            current_user = sgtk.util.get_current_user(self.app.sgtk)
        
            data = {
                "code": os.path.splitext(
                    os.path.basename(self.quicktime.path))[0],
                "user": current_user,
                "entity": self.app.context.entity,
                "project": self.app.context.project,
                "created_by": current_user,
                "description": notes,
                "frame_count": self.quicktime.frame_count,
                "frame_range": self.quicktime.frame_range,
                "sg_first_frame": self.quicktime.first_frame,
                "sg_last_frame": self.quicktime.last_frame,
                "sg_path_to_movie": self.quicktime.path
            }
        
            if self.app.context.task:
                data["sg_task"] = self.app.context.task

        upload_callback = lambda version: self._upload_complete(version)
        upload_thread = UploadThread(self.app, data, upload_callback)
        upload_thread.start()
        
    # -------------------------------------------------------------------------
    def _upload_complete(self, version):
        """
        Upload was completed. Show success widget.
        """

        # success!
        version_context = sgtk.context.from_entity(self.app.engine.sgtk,
                'Version', version["id"])

        self.app.engine.show_dialog(self.name, self.app, 
            QuickReviewSuccessWidget, version_context)

    # -------------------------------------------------------------------------
    def _validate_quicktime(self):

        return (
            self.quicktime.success and
            self.quicktime.path and
            os.path.exists(self.quicktime.path)
        )
                
# ----------------------------------------------------------------------------
class ActionBusy(object):
    """
    A global busy context manager.
    """

    # ------------------------------------------------------------------------
    def __init__(self, title, msg):
        """
        Init with the busy message to display to the user.
        """
        self._title = title
        self._msg = msg

    # ------------------------------------------------------------------------
    def __enter__(self):
        """
        Shows the global busy message.
        """
        show_global_busy(self._title, self._msg)

    # ------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Clears the global busy message.
        """
        clear_global_busy()


# ----------------------------------------------------------------------------
class UploadThread(threading.Thread):

    # ------------------------------------------------------------------------
    def __init__(self, app, data, callback):
        """
        Init the thread with the relevant bits.
        """
        
        super(UploadThread, self).__init__()

        self._app = app
        self._data = data
        self._callback = callback

    # ------------------------------------------------------------------------
    def run(self):
        """
        Execute the thread. Creates the version in sg and uploads the movie.
        """

        self._app.log_info("Creating Shotgun version: %s" % self._data)
        version = self._app.shotgun.create("Version", self._data)

        # upload the file so that it can be transcoded for web review
        # server side. 
        quicktime_path = self._data['sg_path_to_movie']
        self._app.log_info("Uploading quicktime to Shotgun...")
        self._app.shotgun.upload("Version", version["id"], 
            quicktime_path, "sg_uploaded_movie")

        # in this case, callback has to run in main thread
        self._app.engine.execute_in_main_thread(self._callback, version)

# ------------------------------------------------------------------------
def _generate_quicktime(quicktime_path):
    """
    Returns a Quicktime object with info about the generated quicktime.
    """

    quicktime_dir = os.path.dirname(quicktime_path)

    if not os.path.exists(quicktime_dir):
        try:
            os.makedirs(quicktime_dir)
        except os.error as e:
            return Quicktime(
                success=False,
                error_msg=str(e),
                frame_count=None,
                frame_range=None,
                first_frame=None,
                last_frame=None,
                path=None,
            )

    # use the min/max frames from frame slider
    first_frame = int(cmds.playbackOptions(query=True, minTime=True))
    last_frame = int(cmds.playbackOptions(query=True, maxTime=True))

    # initiate the playblast
    try:
        cmds.playblast(
            compression="jpeg",
            endTime=last_frame,
            filename=quicktime_path,
            forceOverwrite=True,
            format="movie",
            offScreen=True,
            startTime=first_frame,
            viewer=False,
        )
    except Exception as e:
        error_msg = str(e)
        success = False
    else:
        error_msg = None
        success = True

    # return all the info for the new quicktime
    return Quicktime(
        success=success,
        error_msg=error_msg,
        frame_count=int(last_frame - first_frame + 1),
        frame_range="{f}-{l}".format(f=first_frame, l=last_frame),
        first_frame=first_frame,
        last_frame=last_frame,
        path=quicktime_path,
    )

