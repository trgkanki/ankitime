# -*- coding: utf-8 -*-
#
# addon_template v20.5.4i8
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook
from aqt.qt import QWebEngineSettings
import aqt
import base64
import os
import mimetypes

from .utils import openChangelog
from .utils.configrw import getConfig
from .utils.resource import readResource, updateMedia
from .utils.JSCallable import JSCallable
from .mobileSupport.modelModifier import registerAnkiTimeScript

addHook("profileLoaded", registerAnkiTimeScript)


@JSCallable
def isActiveWindowAnki():
    return aqt.mw.app.activeWindow() != None


def afterInitWeb(self):
    js = readResource("js/main.min.js")
    self.web.settings().setAttribute(
        QWebEngineSettings.PlaybackRequiresUserGesture, False
    )
    updateMedia("_at_alert.mp3", readResource("sfx/alert.mp3", binary=True), False)
    updateMedia("_at_resume.mp3", readResource("sfx/resume.mp3", binary=True), False)

    def cb2(res):
        if getConfig("idleAlarm"):
            self.web.eval("window._atInstance.enableIdleAlarm(true)")

        fname = getConfig("alarmFile")
        if fname and os.path.isfile(fname):
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

    self.web.evalWithCallback(js, cb2)


Reviewer._initWeb = wrap(Reviewer._initWeb, afterInitWeb, "after")
