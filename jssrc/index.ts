import toastr from 'toastr'
import 'toastr/build/toastr.css'

import { setVisibilityCallback, registerVisibilityChecker } from './visibility'

/* eslint no-inner-declarations:0 */

if (!window._atInitialized) {
  window._atInitialized = true

  let callbackTimer: number | null = null
  let alertPlaying = false
  let alertAudio = new Audio(require('./sfx/alert.mp3').default)
  const resumeAudio = new Audio(require('./sfx/resume.mp3').default)

  alertAudio.loop = true

  function justPlay (audioElement: HTMLAudioElement) {
    audioElement.pause()
    audioElement.currentTime = 0
    audioElement.play()
  }

  function onBlur () {
    callbackTimer = setTimeout(() => {
      justPlay(alertAudio)
      alertPlaying = true
      callbackTimer = null
    }, 30000)
  }

  function onFocus () {
    if (callbackTimer !== null) clearTimeout(callbackTimer)
    if (alertPlaying) {
      alertAudio.pause()
      justPlay(resumeAudio)
      alertPlaying = false
      toastr.info('Resuming reviews...')
    }
  }

  setVisibilityCallback(onFocus, onBlur)
  registerVisibilityChecker()

  window._atSetAlarmSoundUrl = function (url: string) {
    const newAudio = new Audio(url)
    newAudio.loop = true

    // Replace!
    alertAudio.pause()
    alertAudio.remove()
    alertAudio = newAudio
  }
}
