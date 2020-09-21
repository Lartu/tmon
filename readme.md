# tmon

**tmon**, the *[You]Tube Monitor*, is a tool to make regular, local backups of
your YouTube music playlists.

## Why?

Because it's happened many times already that music I liked (and that had been
custom made or remixed by artists I follow) was taken down or made private and
I lost it forever. So one day I said no more and downloaded all my playlist
using `youtube-dl`. But `youtube-dl` doesn't keep track of what has been
downloaded and what hasn't, that's why I made tmon.

## How do I use tmon?

Clone this repository, move it to somewhere permanent and make `tmon.py`
executable by running `chmod +x tmon.py`. Then hook it to your crontab file.
To do this, run `crontab -e` to open your crontab on an editor and then
add the line `0 */2 * * * /path/to/tmon.py` to it. This will run `tmon` every
2 hours. If you want to change the execution frequency, modify the cron line.

To select the playlist to backup, modify the file `config.tmon`. The only contents
of that file should be the playlist id of the playlist you want to back up (the
id that follows the `&list=` on the YouTube URL).

If you want to execute tmon only once, run `./tmon.py`. If you don't want to
cron it, you can run it this way whenever you want to back-up your playlist
(do it often!).

## FAQ

### What does tmon require to work?

tmon requires python3 and youtube-dl. But it gets the last version of youtube-dl
itself and stores it in the tmon directory the first time it's ran, so you don't
need to worry about that.

### Where does tmon download my music to?

tmon places all downloaded files in a `downloads` directory within the tmon
directory.

### Does tmon have a log?

tmon logs all its output to the `log.tmon` file. It also logs all downloaded
songs to `history.tmon` and all failed downloads to `failed.tmon`.

### What is the .temp_list file tmon generates?

The `.temp_list` file is a temporal file with all your playlist URLs in there.
You can safely delete it, tmon will recreate it whenever it needs it.

### I want to download a file that I have already downloaded in the past

Easy, just delete its url from `history.tmon`. Its url is listed in that file
along with the name of the file and the name of the video the file was generated from. 

### I have more questions about tmon!

If you have questions please do send me an email to [lartu+tmon@lartu.net](mailto:lartu+tmon@lartu.net).

## License

tmon is released under the MIT license.
