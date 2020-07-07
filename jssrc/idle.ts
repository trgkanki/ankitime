const events = ['load', 'mousemove', 'mousedown', 'click', 'keydown']
let t: number | null = null
let _isIdle = false

function onIdleTimer () {
  console.log('onIdleTimer')
  _isIdle = true
  t = null
}

function resetIdleTimer () {
  _isIdle = false
  if (t !== null) clearTimeout(t)
  t = setTimeout(onIdleTimer, 1000)
  console.log('resetIdleTimer')
}

for (const ev of events) {
  window.addEventListener(ev, resetIdleTimer)
}

resetIdleTimer()

export function isIdle () {
  return _isIdle
}
