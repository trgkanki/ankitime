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

/**
 * Call python function defiend with `@JSCallableMethod`
 *
 * Example usage:
 *
 *    callPyFunc('test', 1, 2).then(ret => {
 *      // ret is test(1, 2) here
 *    })
 *
 * @param funcname Function defined in the addon
 * @param args List of parameters
 */
export function callPyFunc (
  funcname: string,
  ...args: any[]
): Promise<any> {
  return new Promise<any>((resolve, reject) => {
    const cmdstr = `pyfunc:${ADDON_UUID}:${funcname}:${JSON.stringify(args)}`
    pycmd(cmdstr, (ret) => {
      if (!ret) return reject(new Error(`Calling unknown pyfunc ${funcname}`))
      const error = ret.error as (string | null)
      if (error) return reject(new Error(error))
      else return resolve(ret.payload)
    })
  })
}
