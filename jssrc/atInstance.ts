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

import { ActivityTracker } from './activity/index'
import toastr from 'toastr'
import 'toastr/build/toastr.css'
import { getAddonConfig } from './utils/addonConfig'

function justPlay (audioElement: HTMLAudioElement) {
  audioElement.pause()
  audioElement.currentTime = 0
  audioElement.play()
}

export class ATInstance {
  callbackTimer: number | null = null
  alertPlaying = false
  alertAudio = new Audio('_at_alert.mp3')
  resumeAudio = new Audio('_at_resume.mp3')
  alertAudioInterval: number | null = null
  _activityTracker: ActivityTracker

  constructor () {
    this.alertAudio.loop = true
    this._activityTracker = new ActivityTracker()
    this._activityTracker.trackIdle = false
    this._activityTracker.onFocus = this._onFocus.bind(this)
    this._activityTracker.onBlur = this._onBlur.bind(this)
  }

  dispose () {
    // TODO: refactor constructor-dispose cycle.
    this._activityTracker.dispose()
    this.alertAudio.pause()
    this.resumeAudio.pause()
    if (this.alertAudioInterval) {
      clearInterval(this.alertAudioInterval)
      this.alertAudioInterval = null
    }
    if (this.callbackTimer) {
      clearTimeout(this.callbackTimer)
      this.callbackTimer = null
    }
  }

  private async _onBlur () {
    const timeoutTimer = Number(await getAddonConfig('idleTimerTime')) * 1000
    this.callbackTimer = setTimeout(() => {
      justPlay(this.alertAudio)
      this.alertAudioInterval = setInterval(() => this.alertAudio.play(), 10000)
      this.alertPlaying = true
      this.callbackTimer = null
    }, timeoutTimer)
  }

  private _onFocus () {
    if (this.callbackTimer !== null) clearTimeout(this.callbackTimer)
    if (this.alertPlaying) {
      if (this.alertAudioInterval !== null) {
        clearInterval(this.alertAudioInterval)
        this.alertAudioInterval = null
      }
      this.alertAudio.pause()
      justPlay(this.resumeAudio)
      this.alertPlaying = false
      toastr.info('Resuming reviews...')
    }
  }

  // Public API
  enableIdleAlarm (enabled: boolean) {
    this._activityTracker.trackIdle = enabled
  }

  setAlarmSound (url: string) {
    const newAudio = new Audio(url)
    newAudio.loop = true

    // Replace!
    if (this.alertAudioInterval !== null) {
      clearInterval(this.alertAudioInterval)
      this.alertAudioInterval = null
    }
    this.alertAudio.pause()
    this.alertAudio.remove()
    this.alertAudio = newAudio
  }
}
