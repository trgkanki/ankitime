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
  onBlur: callback | undefined

  // Updater
  async _updateActivityStatus () {
    const isAnkiActive = await isActiveWindowAnki(this.trackIdle)

    if (isAnkiActive !== this._wasActive) {
      if (isAnkiActive) {
        if (this.onFocus) (this.onFocus)()
      } else {
        if (this.onBlur) (this.onBlur)()
      }
      this._wasActive = isAnkiActive
    }
  }
}
