## Requirements

1) Verify `uinput` is enabled in `/etc/modules-load.d/` (activate using `sudo modprobe uinput`)
2) Add user to group `input` (command `sudo usermod -a -G input $USER`)
3) Copy `external/99-uinput.rules` to `/etc/udev/rules.d/`
4) Run 2 commands (in terminal): `sudo udevadm control --reload-rules` and `sudo udevadm trigger`

