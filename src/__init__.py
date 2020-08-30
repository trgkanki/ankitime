# Copyright (C) 2020 Hyun Woo Park
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
#
# ankitime v20.5.4i8
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook
from aqt.qt import QWebEngineSettings
from aqt.utils import showInfo
from aqt import AnkiQt
import aqt
import base64
import os
import mimetypes

from .utils import openChangelog
from .utils import uuid  # duplicate UUID checked here
from .utils.configrw import getConfig
from .utils.resource import readResource, updateMedia
from .utils.JSCallable import JSCallable
from .mobileSupport.modelModifier import registerMobileScript

addHook("profileLoaded", registerMobileScript)


@JSCallable
def isActiveWindowAnki():
    return aqt.mw.app.activeWindow() != None


def afterInitWeb(self):
    js = readResource("js/main.min.js")
    self.web.settings().setAttribute(
        QWebEngineSettings.PlaybackRequiresUserGesture, False
    )
    updateMedia("_at_resume.mp3", readResource("sfx/resume.mp3", binary=True), False)

    def cb2(res):
        if getConfig("idleAlarm"):
            self.web.eval("window._atInstance.enableIdleAlarm(true)")

        fname = getConfig("alarmFile")
        if fname:
            updateMedia(
                "_at_alert.mp3", readResource("sfx/alert.mp3", binary=True), False
            )
            if os.path.isfile(fname):
                with open(fname, "rb") as f:
                    content = f.read()
                mimetype = mimetypes.guess_type(fname)[0]

                if mimetype == "audio/mpeg":
                    updateMedia("_at_alert.mp3", content)
                    # Reload _at_alert.mp3 on JS side
                    self.web.eval(f'window._atInstance.setAlarmSound("_at_alert.mp3")')
                else:
                    b64 = base64.b64encode(content).decode("ascii")
                    dataURI = f"data:{mimetype};base64,{b64}"
                    self.web.eval(f'window._atInstance.setAlarmSound("{dataURI}")')
            else:
                showInfo('[Anki Time] unknown file "%s"' % fname)

        else:
            updateMedia(
                "_at_alert.mp3", readResource("sfx/alert.mp3", binary=True), True
            )

    self.web.evalWithCallback(js, cb2)


Reviewer._initWeb = wrap(Reviewer._initWeb, afterInitWeb, "after")


# Fixes issue #3
# Anki doesn't cleanly dispose child widgets when exiting the program.
# This code forces disposal


def disposeAnkiTime(self, _old):
    self.web.evalWithCallback(
        "if (window._atInstance) window._atInstance.dispose();", lambda res: _old(self)
    )


AnkiQt.unloadProfileAndExit = wrap(
    AnkiQt.unloadProfileAndExit, disposeAnkiTime, "around"
)
