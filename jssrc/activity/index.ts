// Copyright (C) 2020 Hyun Woo Park
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

import { isActiveWindowAnki } from './visibility'

type callback = () => void

function currentTime () {
  return (new Date()).getTime()
}

export class ActivityTracker {
  private _lastActiveTime = currentTime()
  private _updateInterval: number
  private _wasActive = true

  constructor () {
    this._updateInterval = setInterval(
      this._updateActivityStatus.bind(this),
      500
    )
  }

  dispose () {
    clearInterval(this._updateInterval)
  }

  // Configuration API
  trackIdle = false
  onFocus: callback | undefined
  onIdle: callback | undefined

  // Updater
  async _updateActivityStatus () {
    const isAnkiActive = await isActiveWindowAnki(this.trackIdle)

    if (isAnkiActive !== this._wasActive) {
      if (isAnkiActive) {
        if (this.onFocus) (this.onFocus)()
      } else {
        if (this.onIdle) (this.onIdle)()
      }
      this._wasActive = isAnkiActive
    }
  }
}
