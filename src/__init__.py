# -*- coding: utf-8 -*-
#
# addon_template v20.5.4i8
#
# Copyright: trgk (phu54321@naver.com)
# License: GNU AGPL, version 3 or later;
# See http://www.gnu.org/licenses/agpl.html

from aqt.reviewer import Reviewer
from anki.hooks import wrap
import aqt

from .utils import openChangelog
from .utils.resource import readResource
from .utils.JSEval import execJSFile
from .utils.JSCallable import JSCallable

js = readResource('js/main.min.js')

@JSCallable
def isActiveWindowAnki():
    return aqt.mw.app.activeWindow() != None

def afterInitWeb(self):
    self.web.eval(js)

Reviewer._initWeb = wrap(Reviewer._initWeb, afterInitWeb, "after")
