from aqt import mw
from aqt.utils import askUser
from aqt.utils import openLink
from aqt.qt import QDesktopServices, QUrl
from anki.utils import noBundledLibs

import os

from .configrw import getCurrentAddonName
from .resource import readResource, getResourcePath


def getCurrentAddonVersion():
    return readResource("VERSION")


def showChangelogOnUpdate():
    addonVersion = getCurrentAddonVersion()
    addonName = getCurrentAddonName()

    addonMeta = mw.addonManager.addonMeta(addonName)
    if addonMeta.get("human_version", None) != addonVersion:
        addonMeta["human_version"] = addonVersion
        mw.addonManager.writeAddonMeta(addonName, addonMeta)

        changelogPath = getResourcePath("CHANGELOG.html")
        if os.path.exists(changelogPath):
            with noBundledLibs():
                QDesktopServices.openUrl(QUrl.fromLocalFile(changelogPath))


showChangelogOnUpdate()
