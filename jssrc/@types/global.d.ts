declare function pycmd (cmd: string, resultCallback?: (arg: any) => void): any

interface Window {
  _atInitialized: boolean;
  _atSetAlarmSoundUrl(url: string): void;
}
