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

const events = [
  'load', 'mousemove', 'mousedown', 'click', 'keydown',
  'touchstart', 'touchmove'
]

export class IdleTracker {
  t: number | null
  _isIdle: boolean

  constructor () {
    this.t = null
    this._isIdle = false

    for (const ev of events) {
      window.addEventListener(ev, this.resetIdleTimer, true)
    }

    this.resetIdleTimer()
  }

  dispose () {
    for (const ev of events) {
      window.removeEventListener(ev, this.resetIdleTimer)
    }
  }

  private onIdleTimer () {
    this._isIdle = true
    if (this.t !== null) clearTimeout(this.t)
    this.t = null
  }

  resetIdleTimer () {
    // console.log(e)
    this._isIdle = false
    if (this.t !== null) clearTimeout(this.t)
    this.t = setTimeout(this.onIdleTimer, 5000)
  }

  isIdle () {
    return this._isIdle
  }
}
