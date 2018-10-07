# Auto-remap volume buttons based on device orientation

Auto-remap Microsoft Surface Book 2 and Surface Pro (2017) volume buttons based on device orientation.

Ensures that the left/lower volume button always decreases, and the right/upper always increases the volume.

## Installing

Install the required files as described below.
Then enable the `systemd` service via

```sh
systemctl enable surfacebook2-button-autoremap.service
```

### Debian

In the source directory, run `./pkg/build-deb.sh` to generate the package, which you can then install via `dpkg -i *.deb`.

### Arch Linux

Build and install the package via the provided `PKGBUILD`, i.e. run `makepkg` inside the `pkg` folder (or the directory where you stored the `PKGBUILD`) and then `pacman -U *.tar.xz` to install the generated package.

### Manual

Copy

- `autoremap.py` to `/opt/surfacebook2-button-autoremap/` and
- `surfacebook2-button-autoremap.service` to `/etc/systemd/system/`.

You may want to have a look at the `Pipfile` and make sure the required dependencies are installed.
Additionally you may need to install [iio-sensor-proxy](https://github.com/hadess/iio-sensor-proxy).
