import { callPyFunc } from './utils/pyfunc'

export type callback = () => void

let hasFocus = true
let onFocus: callback | undefined
let onBlur: callback | undefined

export function setVisibilityCallback (newOnFocus: callback, newOnBlur: callback) {
  onFocus = newOnFocus
  onBlur = newOnBlur
}

setInterval(async () => {
  const isAnkiActive = document.hasFocus() || await callPyFunc('isActiveWindowAnki')

  if (isAnkiActive !== hasFocus) {
    if (isAnkiActive) {
      if (onFocus) onFocus()
    } else {
      if (onBlur) onBlur()
    }
    hasFocus = isAnkiActive
  }
}, 1000)
