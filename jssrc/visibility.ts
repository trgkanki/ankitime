export type callback = () => void

let hasFocus = false
let onFocus: callback | undefined
let onBlur: callback | undefined

export function setVisibilityCallback (newOnFocus: callback, newOnBlur: callback) {
  onfocus = newOnFocus
  onblur = newOnBlur
}

setInterval(() => {
  if (document.hasFocus()) {
    if (!hasFocus) {
      if (onFocus) onFocus()
    }
    hasFocus = true
  } else {
    if (hasFocus) {
      if (onBlur) onBlur()
    }
    hasFocus = false
  }
}, 1000)
