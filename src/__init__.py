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
from .utils.resource import readResource
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

    def cb2(res):
        if getConfig("alarmFile"):
            fname = getConfig("alarmFile")
            with open(fname, "rb") as f:
                content = f.read()
            mimetype = mimetypes.guess_type(fname)[0]
            if mimetype:
                b64 = base64.b64encode(content).decode("ascii")
                dataURI = f"data:{mimetype};base64,{b64}"
                self.web.eval(f'window._atSetAlarmSoundUrl("{dataURI}")')

    self.web.evalWithCallback(js, cb2)


Reviewer._initWeb = wrap(Reviewer._initWeb, afterInitWeb, "after")
