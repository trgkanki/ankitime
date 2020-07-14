import { callPyFunc } from './utils/pyfunc'
import { isIdle } from './idle'
import isMobile from 'is-mobile'

type callback = () => void

let hasFocus = true
let onFocus: callback | undefined
let onBlur: callback | undefined

export function setVisibilityCallback (newOnFocus: callback, newOnBlur: callback) {
  onFocus = newOnFocus
  onBlur = newOnBlur
}

async function isActiveWindowAnki () {
  if (isMobile()) return !document.hidden
  if (document.hasFocus()) return !isIdle()
  try {
    return await callPyFunc('isActiveWindowAnki')
  } catch (err) {
    // On Card template editing window, isActiveWindowAnki may not be registered :(
    return false
  }
}

export function registerVisibilityChecker () {
  setInterval(async () => {
    const isAnkiActive = await isActiveWindowAnki()

    if (isAnkiActive !== hasFocus) {
      if (isAnkiActive) {
        if (onFocus) onFocus()
      } else {
        if (onBlur) onBlur()
      }
      hasFocus = isAnkiActive
    }
  }, 500)
}
