const events = [
  'load', 'mousemove', 'mousedown', 'click', 'keydown',
  'touchstart', 'touchmove'
]

let t: number | null = null
let _isIdle = false

function onIdleTimer () {
  _isIdle = true
  t = null
}

function resetIdleTimer () {
  _isIdle = false
  if (t !== null) clearTimeout(t)
  t = setTimeout(onIdleTimer, 1000)
}

for (const ev of events) {
  window.addEventListener(ev, resetIdleTimer)
}

resetIdleTimer()

export function isIdle () {
  return _isIdle
}
