/* eslint no-inner-declarations:0 */

import { setVisibilityCallback } from './visibility'

if (!window._atInitialized) {
  window._atInitialized = true

  let callbackTimer: number | null = null
  let alertPlaying = false
  const alertAudio = new Audio(require('./sfx/alert.mp3').default)
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
    }
  }

  setVisibilityCallback(onFocus, onBlur)
}
