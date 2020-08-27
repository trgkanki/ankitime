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

from aqt import gui_hooks
from aqt.utils import showInfo
from .configrw import getCurrentAddonName

import json
import re
import uuid
from .resource import readResource

_handlerMap = {}
_addonMessageRegex = re.compile(r"addonmsg:(\d+):(.+)")


def _onBridgeMessage(handled, message, context):
    matches = _addonMessageRegex.match(message)
    if not matches:
        return handled

    handlerKey = matches.group(1)
    message = matches.group(2)
    if handlerKey in _handlerMap:
        _handlerMap[handlerKey](json.loads(message))
        del _handlerMap[handlerKey]
        return (True, None)


gui_hooks.webview_did_receive_js_message.append(_onBridgeMessage)


def execJSFile(web, jspath, cb=None, *, once=False):
    js = readResource(jspath)
    if once:
        checkKey = "".join([getCurrentAddonName(), "#", jspath])
        js = """
        if (!window.__plugin_jsTable) window.__plugin_jsTable = {}
        if (!window.__plugin_jsTable["%s"]) {
            window.__plugin_jsTable["%s"] = true
            %s
        }
        """ % (
            checkKey,
            checkKey,
            js,
        )

    if cb:
        web.evalWithCallback(js, lambda res: cb())
    else:
        web.eval(js)


def execJSFileOnce(web, jspath, cb):
    """
    Excute JS file only once. useful for webpack-based modules
    """
    return execJSFile(web, jspath, cb, once=True)


def evalJS(web, funcexpr, cb):
    # Register handler
    handlerKey = str(uuid.uuid4().int)
    _handlerMap[handlerKey] = cb

    # Execute js code
    web.eval(
        """
    Promise.resolve(%s).then(msg => {
        pycmd(`addonmsg:%s:${JSON.stringify(msg)}`)
    })"""
        % (funcexpr, handlerKey)
    )
