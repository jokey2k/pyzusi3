# 3.1.0 (2024-07-04)
## Added
Support client disconnect call
## Updated
Make reading unknown or bad formatted messages a non-fatal error to account for new Zusi versions not incrementing protocol versions
Update some message parameters as contributed by Wolfgang Evers from TH Köln

# 3.0.0 (2023-09-03)
## Added
Add message STATUS_SIGNALE thanks to Wolfgang Evers
Breaking: Now unknown message IDs or bad message content is ignored by default to support future Zusi Versions as they seem to have no idea what API versioning is used for
## Updated
Various typo fixes in message names or parameters, resulting in major version number bump

# 2.0.0 (2023-02-09)
## Added
Auto-SIFA feature in pyzusidisplay
## Updated
When async client reader task raises an exception, it is no longer swallowed but reraised
Make lib compatible to Zusi 3.5. As it introduced breaking changes in API, we update our major as well. use 1.2.1. for Zusi 3.4 and below

# 1.2.1 (2023-01-28)
## Updated
Fix missing message mapping name in STATUS_TUEREN

# 1.2.0 (2023-01-15)
## Updated
Changed STATUS_INDUSI_BETRIEBSDATEN so that 500Hz and 1000Hz add option to be in more states per https://forum.zusi.de/viewtopic.php?p=342503#p342503

# 1.1.1 (2022-10-22)
## Updated
Docs on README and CHANGELOG to be consistent across tar and website

# 1.1.0 (2022-10-22)
## Added
Support for ETCS and ZBS messages

# 1.0.0 (2022-10-09)
## Initial release
Comes without support for ETCS and ZBS messages
