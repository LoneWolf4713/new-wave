# ncmpcpp-with-cover-art
Setup for displaying cover art in ncmpcpp.

## Dependencies
- `tmux`           (to encapsulate everything in one window)  
- `inotify-tools`  (for changing album art when switching songs)  
- `ueberzug`       (for image rendering)  
- `ffmpeg`         (used in scaling the album art)  
- `mpc`            (cli client for MPD)  

## Install
Drop all the files in your `.ncmpcpp` directory and add this into your `.bashrc`:
```
alias music='tmux new-session -s $$ "tmux source-file ~/.ncmpcpp/tsession"'
_trap_exit() { tmux kill-session -t $$; }
```
Set your `$MUSIC_DIR` env variable to contain your music directory.

Run it with `music`.

## Screenshot
![alt text](https://radumirea.com/resources/blog/ncmcpp-with-album-art/ncmpcpp.png)
