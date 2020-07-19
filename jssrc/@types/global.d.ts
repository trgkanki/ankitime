declare function pycmd (cmd: string, resultCallback?: (arg: any) => void): any

interface Window {
  _atInstance: import('@/atInstance').ATInstance | undefined;
}
