# live-wallpaper-linux

Live wallpaper for Linux (so far tested on Linux Mint Cinnamon and Ubuntu)
Because a distro might have a different implementation on how desktop works, you might need to some extra steps

For example this is how it would look on Ubuntu

```sh
./live-wallpaper.py live.mp4 &
sleep 5s # Give some time to start
killall -3 gnome-shell # Restart gnome shell
```
