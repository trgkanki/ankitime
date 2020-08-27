// Copyright (C) 2020 Hyun Woo Park
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
