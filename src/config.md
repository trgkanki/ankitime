# Anki Time

## alarmFile (default: "")

Path of custom alarm sound. Note that path in windows should be backslash-escaped, as denoted on [JSON spec](https://www.json.org/) For example, path `C:\Users\whyask37\music.mp3` becomes

```json
{
  "alarmFile": "C:\\Users\\whyask37\\music.mp3"
}
```

Just remember to replace all occurrence of `\` with `\\`.

## runOnMobile (default: false)

Also run the addon script on mobile environments (AnkiDroid currently supported).

## idleAlarm (default: true)

By default, addon tracks whether you're idling with Anki open. Addon tracks your mouse and keyboard status to check the activity, but this is known to interfering with people not using mouse/keyboard for reviews. See [this github issue](https://github.com/trgkanki/ankitime/issues/5) for more info.

This option only affects desktop environments.

