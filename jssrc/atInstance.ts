import { ActivityTracker } from './activity/index'
import toastr from 'toastr'
import 'toastr/build/toastr.css'

function justPlay (audioElement: HTMLAudioElement) {
  audioElement.pause()
  audioElement.currentTime = 0
  audioElement.play()
}

export class ATInstance {
  callbackTimer: number | null = null
  alertPlaying = false
  alertAudio = new Audio(require('./sfx/alert.mp3').default)
  resumeAudio = new Audio(require('./sfx/resume.mp3').default)
  alertAudioInterval: number | null = null
  _activityTracker: ActivityTracker

  constructor () {
    this.alertAudio.loop = true
    this._activityTracker = new ActivityTracker()
    this._activityTracker.trackIdle = true // TODO: send this to options
    this._activityTracker.onFocus = this._onFocus.bind(this)
    this._activityTracker.onBlur = this._onBlur.bind(this)
  }

  private _onBlur () {
    this.callbackTimer = setTimeout(() => {
      justPlay(this.alertAudio)
      this.alertAudioInterval = setInterval(() => this.alertAudio.play(), 10000)
      this.alertPlaying = true
      this.callbackTimer = null
    }, 30000)
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
