# Changelog of ankitime

[comment]: # (DO NOT MODIFY. new changelog goes here)

## 20.7.20i40 (2020-07-20)

- Bugfix: addon not working on first install. This issue was due to how
  addon checks its current version.

## 20.7.19i74 (2020-07-19)

- Bug fix: Alarm should stop on app exit.
- Feature: option to disable *idle alarm*. Check `idleAlarm` option on the addon config.
- Feature: Basic AnkiDroid support. Not yet tested on AnkiMobile, and maybe won't be supported, as apple don't like
  background script running without explicit permission.

## 20.7.14i71 (2020-07-14)

Hotfix: addon not starting after update

## 20.7.14i34 (2020-07-14)

- Custom alarm sound. Check out the `alarmFile` key on alarm configuration.
- Alarm on idle. When you're doing smartphone during review, ...

## 20.7.5i77 (2020-07-05)

- Bug fix: audio sometimes not playing. (Issue #1) This was related to QWebEngine's autoplay policy. By default autoplay is disabled for webviews without user interactions, so alarm won't be played until user does something on the page. This has been fixed with proper configurations.

## 20.6.28i53 (2020-06-28)

First release on AnkiWeb

- Feature: Toast notification on resume
- Fix: alert running on add card / edit card / browser dialog

## 20.6.28i41 (2020-06-28)

Initial release.
