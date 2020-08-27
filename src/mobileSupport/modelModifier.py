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

import os
import re

from aqt import mw

from .markerReplacer import ReplaceBlock, removeReplaceBlock
from ..utils.resource import readResource, updateMedia
from ..utils.configrw import getConfig

############################# Templates

mediaScriptPath = "_ankitime.min.js"

scriptBlock = ReplaceBlock(
    "<!-- # 5d76369d98ea0c92 -->",
    "<!-- / 5d76369d98ea0c92 -->",
    f'<script src="{mediaScriptPath}"></script>',
)


def applyScriptBlock(template, key, updated=None):
    orig = template[key]
    fieldUpdated = [False]
    new = scriptBlock.apply(orig, updated=fieldUpdated)
    if fieldUpdated[0]:
        template[key] = new
        if updated:
            updated[0] = True


###################################################################


MODE_SET = "set"
MODE_UNSET = "unset"


def registerMobileScript():
    col = mw.col

    if getConfig("runOnMobile"):
        mode = MODE_SET
        updateMedia(mediaScriptPath, readResource("js/main.min.js").encode("utf-8"))
    else:
        mode = MODE_UNSET
        # Should we remove the media? I don't really think so :(

    updateModels(col, mode)


def updateModels(col, mode):
    models = col.models
    templateUpdated = [False]
    for model in col.models.all():
        for template in model["tmpls"]:
            oldqfmt = template["qfmt"]
            oldafmt = template["afmt"]

            if mode == MODE_SET:
                applyScriptBlock(template, "qfmt")
                if "{{FrontSide}}" not in template["afmt"]:
                    applyScriptBlock(template, "afmt")
                else:
                    template["afmt"] = removeReplaceBlock(
                        template["afmt"], scriptBlock.startMarker, scriptBlock.endMarker
                    )

            else:
                template["qfmt"] = removeReplaceBlock(
                    template["qfmt"], scriptBlock.startMarker, scriptBlock.endMarker
                )
                template["afmt"] = removeReplaceBlock(
                    template["afmt"], scriptBlock.startMarker, scriptBlock.endMarker
                )

        template["qfmt"] = template["qfmt"].replace("\r", "\n")
        template["qfmt"] = re.sub(r"\n{3,}", "\n\n", template["qfmt"])
        template["afmt"] = template["afmt"].replace("\r", "\n")
        template["afmt"] = re.sub(r"\n{3,}", "\n\n", template["afmt"])
        if not (template["qfmt"] == oldqfmt and template["afmt"] == oldafmt):
            templateUpdated[0] = True

    if templateUpdated[0]:
        models.save()
