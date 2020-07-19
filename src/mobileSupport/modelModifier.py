import os

from aqt import mw

from .markerReplacer import ReplaceBlock, removeReplaceBlock
from ..utils.resource import readResource
from ..utils.configrw import getConfig

############################# Templates

mediaScriptPath = "_ankitime.min.js"

scriptBlock = ReplaceBlock(
    "<!-- # 5d76369d98ea0c92 -->\n",
    "<!-- / 5d76369d98ea0c92 -->",
    f'<script src="{mediaScriptPath}"></script>\n',
)


def applyScriptBlock(template, key, updated):
    orig = template[key]
    fieldUpdated = [False]
    new = scriptBlock.apply(orig, updated=fieldUpdated)
    if fieldUpdated[0]:
        template[key] = new
        updated[0] = True


###################################################################


def updateMedia(col, name, newData):
    media = col.media
    targetFile = os.path.join(media.dir(), name)

    if os.path.exists(targetFile):
        with open(targetFile, "rb") as f:
            if f.read() == newData:
                return  # Identical data already exists
        os.unlink(targetFile)

    col.media.writeData(name, newData)


MODE_SET = "set"
MODE_UNSET = "unset"


def registerAnkiTimeScript():
    col = mw.col

    if getConfig("runOnMobile"):
        mode = MODE_SET
        updateMedia(
            col, mediaScriptPath, readResource("js/main.min.js").encode("utf-8")
        )
    else:
        mode = MODE_UNSET
        # Should we remove the media? I don't really think so :(

    updateModels(col, mode)


def updateModels(col, mode):
    models = col.models
    templateUpdated = [False]
    for model in col.models.all():
        for template in model["tmpls"]:
            if mode == MODE_SET:
                applyScriptBlock(template, "qfmt", templateUpdated)
                if "{{FrontSide}}" not in template["afmt"]:
                    applyScriptBlock(template, "afmt", templateUpdated)
                else:
                    template["afmt"] = removeReplaceBlock(
                        template["afmt"],
                        scriptBlock.startMarker,
                        scriptBlock.endMarker,
                        updated=templateUpdated,
                    )

            else:
                template["qfmt"] = removeReplaceBlock(
                    template["qfmt"],
                    scriptBlock.startMarker,
                    scriptBlock.endMarker,
                    updated=templateUpdated,
                )
                template["afmt"] = removeReplaceBlock(
                    template["afmt"],
                    scriptBlock.startMarker,
                    scriptBlock.endMarker,
                    updated=templateUpdated,
                )

    if templateUpdated[0]:
        models.save()