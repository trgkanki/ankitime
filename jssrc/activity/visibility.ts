import { callPyFunc } from '../utils/pyfunc'
import isMobile from 'is-mobile'
import { isIdle } from './idle'

type callback = () => void

export async function isActiveWindowAnki (trackIdle: boolean) {
  if (isMobile()) return !document.hidden
  if (document.hasFocus()) {
    if (trackIdle) return !isIdle()
    else return true
  }
  try {
    return await callPyFunc('isActiveWindowAnki')
  } catch (err) {
    // On Card template editing window, isActiveWindowAnki may not be registered :(
    return false
  }
}
