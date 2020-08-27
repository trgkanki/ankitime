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

from aqt import mw
from aqt.webview import AnkiWebView, AnkiWebPage
from aqt.qt import (
    QApplication,
    QUrl,
    QDialog,
    QVBoxLayout,
    Qt,
)
from anki.hooks import wrap

from .resource import getResourcePath


# By default, AnkiWebPage opens link in a browser for non-anki-urls,
# like those starting with `file://`. We override this behavior since,
# well, we want to use same `gui_hooks.webview_did_receive_js_message`
# based js-py bridging for our minibrowser as well. To use AnkiWebView
# directly here, we have to hook this.
# Note that this is very hacky way, and this might break in the future.


def newAcceptNavigationRequest(self, url, navType, isMainFrame, *, _old):
    if hasattr(self, "_isMiniBrowser"):
        return True
    return _old(self, url, navType, isMainFrame)


AnkiWebPage.acceptNavigationRequest = wrap(
    AnkiWebPage.acceptNavigationRequest, newAcceptNavigationRequest, "around"
)


class MiniBrowser(QDialog):
    silentlyClose = True

    def __init__(self, parent, rootHtmlPath, size=None):
        if parent is None:
            parent = mw

        super().__init__(parent)
        mw.setupDialogGC(self)

        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.WindowModal)

        # Populate content
        self.web = AnkiWebView()
        self.web._page._isMiniBrowser = True
        # Support window.close
        self.web._page.windowCloseRequested.connect(self.close)
        l = QVBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(self.web)
        self.setLayout(l)

        if type(size) == tuple:
            w, h = size
            self.resize(w, h)
            self.show()

        elif size is None:
            self.resize(800, 600)
            self.show()

        elif size == "maximized" or size == "maximize":
            self.resize(800, 600)
            self.showMaximized()

        elif size == "minimized" or size == "minimize":
            self.resize(800, 600)
            self.showMinimized()

        else:
            print("MiniBrowser - bad size (%s)" % size)
            self.resize(800, 600)
            self.show()

        # OK
        self.gotoLocalFile(rootHtmlPath)

    def gotoLocalFile(self, rootHtmlPath):
        rootHtmlPath = getResourcePath(rootHtmlPath)

        # Code from AnkiWebView::_setHtml
        app = QApplication.instance()

        # work around webengine stealing focus on setHtml()
        oldFocus = app.focusWidget()
        self.web._page.setUrl(QUrl.fromLocalFile(rootHtmlPath))
        if oldFocus:
            oldFocus.setFocus()

    def accept(self):
        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)
