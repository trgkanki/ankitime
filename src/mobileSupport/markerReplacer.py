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


class ReplaceBlock:
    def __init__(self, startMarker, endMarker, script):
        self.startMarker = startMarker
        self.endMarker = endMarker
        self.script = script
        self.blockRaw = "%s%s%s" % (startMarker, self.script, endMarker)

    def included(self, targetString):
        return self.blockRaw in targetString

    def apply(self, targetString, *, updated=None):
        oldTargetString = targetString
        targetString = removeReplaceBlock(
            targetString, self.startMarker, self.endMarker
        )
        targetString = targetString + "\n\n" + self.blockRaw

        if updated and oldTargetString != targetString:
            updated[0] = True

        return targetString


def removeReplaceBlock(targetString, startMarker, endMarker, *, updated=None):
    oldTargetString = targetString
    while True:
        try:
            start = targetString.index(startMarker)
            end = targetString.index(endMarker, start + 1)
            targetString = (
                targetString[:start] + targetString[end + len(endMarker) :]
            ).strip()
        except ValueError:
            break

    if updated and oldTargetString != targetString:
        updated[0] = True

    return targetString
