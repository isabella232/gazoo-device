# GDM device setup: Raspberry Pi (as a supporting device)

Supported models: Raspberry Pi 3 and 4.

Supported kernel images: Raspbian.

## Setup

1. Flash SD card with the Raspbian kernel. Refer to
   https://www.raspberrypi.org/documentation/installation/installing-images/
   for instructions.
2. Boot the Pi from the SD card.
3. Open the RPi configuration utility: `sudo raspi-config` (from RPi)
    1. Change the default password ("Change User Password")
    2. Enable SSH ("Interfacing Options" -> "SSH")
    3. Connect to Wi-Fi ("Network Options" -> "WLAN")
    4. Select "Finish" to exit the configuration utility
    5. Reboot the RPi: `reboot`
4. Configure GDM SSH keys: run `gdm download-keys` (on the host)
   * If you don't have a key in
     `~/gazoo/gdm/keys/gazoo_device_controllers/raspberrypi3_ssh_key`, you'll
     see an error prompting you to generate a key. Follow the prompt to generate
     all required keys.
     * Alternatively, you can copy an existing private/public SSH key pair to
       `~/gazoo/gdm/keys/gazoo_device_controllers/raspberrypi3_ssh_key` and
       `~/gazoo/gdm/keys/gazoo_device_controllers/raspberrypi3_ssh_key.pub`.

5. Set up passwordless SSH with RPi using the GDM key (on the host):

   ```shell
   ssh-copy-id -i ~/gazoo/gdm/keys/gazoo_device_controllers/raspberrypi3_ssh_key.pub pi@<IP_ADDRESS>
   ```

6. Check that the RPi is accessible from the host:

   ```shell
   ping <IP_ADDRESS>
   ssh -i ~/gazoo/gdm/keys/gazoo_device_controllers/raspberrypi3_ssh_key pi@<IP_ADDRESS>
   ```

7. Detect the RPi: `gdm detect --static_ips=<IP_ADDRESS>`

## Usage

```shell
gdm issue raspberrypi-1234 - shell "echo 'foo'"
gdm issue raspberrypi-1234 - firmware_version
gdm issue raspberrypi-1234 - reboot
echo "Example file" > /tmp/foo.txt
gdm issue raspberrypi-1234 - file_transfer - send_file_to_device --src=/tmp/foo.txt --dest=/tmp
gdm man raspberrypi  # To see all supported functionality
```
