# live-wallpaper-linux

Live wallpaper for Linux (so far tested on Linux Mint Cinnamon and Ubuntu)

Because a distro might have a different implementation on how desktop works, you might need to some extra steps

For example this is how it would look on Ubuntu

```sh
./live-wallpaper.py live.mp4 &
sleep 5s # Give some time to start
killall -3 gnome-shell # On Ubuntu
xdotool windowactivate $(wmctrl -l | awk '$4=="Desktop" {print $1}') # On Linux Mint
```

If you don't have xdotool all you have to do is

```sh
sudo apt install xdotool -y
```
