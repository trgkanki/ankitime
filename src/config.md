# Anki Time

## alarmFile (default: "")

Path of custom alarm sound. Note that path in windows should be backslash-escaped, as denoted on [JSON spec](https://www.json.org/) For example, path `C:\Users\whyask37\music.mp3` becomes `"alarmFile": "C:\\Users\\whyask37\\music.mp3"`. Just remember to replace all occurrence of `\` with `\\`.

Note that if the file is mp3 file, the same file will also be used on AnkiDroid environments.

## runOnMobile (default: false)

Also run the addon script on mobile environments (AnkiDroid currently supported).

## idleAlarm (default: true)

By default, addon tracks whether you're idling with Anki open. Addon tracks your mouse and keyboard status to check the activity, but this is known to interfering with people not using mouse/keyboard for reviews. See [this github issue](https://github.com/trgkanki/ankitime/issues/5) for more info.

This option only affects desktop environments.

## idleTimerTime (default: 30)

How much time to allow idle/non-Anking.

> Note: When setting this value to `0`, I recommend setting `idleAlarm` to `false`. Or it would ring alarm forever when you're doing reviews on the desktop.
