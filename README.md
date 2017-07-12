# youtube-archive
Wrapper for [`youtube-dl`](https://rg3.github.io/youtube-dl/) for repeatedly archiving arbitrary searches

Usage: `./youtube-archive.py [SEARCH OPTIONS] [-- [DOWNLOAD OPTIONS]]`
`SEARCH OPTIONS` are passed to youtube-dl for finding videos
`DOWNLOAD OPTIONS` are passed to youtube-dl when downloading a video

Arguments are stored in `.youtube-archive` in JSON format. To re-invoke
youtube-archiver (to update your archive), start this program with no
arguments. If you wish to change the arguments, either modify the file or
delete it, and provide them as command-line arguments. This program will not
accept command-line arguments while the argument file is present.

See youtube-dl documentation.

Examples:
```
./youtube-archive.py https://www.youtube.com/user/YouTube -- --extract-audio
./youtube-archive.py https://www.youtube.com/user/YouTube --match-title 2016
```
