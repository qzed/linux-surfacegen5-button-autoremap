#!/usr/bin/env sh
set -e

PKGNAME="surfacebook2-button-autoremap"
PKGVER="0.1.0"
PKGREL="1"
PKGDESC="Auto-remap Surface Book 2/Surface Pro (2017) volume buttons based on device orientation"
ARCH="all"
DEPENDS="python, python-evdev, python-dbus, iio-sensor-proxy"
MAINTAINER="Maximilian Luz <qzed@users.noreply.github.com>"


distname="${PKGNAME}_${PKGVER}-${PKGREL}"

mkdir "${distname}"
mkdir -p "${distname}/DEBIAN"
mkdir -p "${distname}/etc/systemd/system"
mkdir -p "${distname}/opt/surfacebook2-button-autoremap"

CONTROL="${distname}/DEBIAN/control"
touch "${CONTROL}"
echo "Package: ${PKGNAME}"          >> "${CONTROL}"
echo "Version: ${PKGVER}-${PKGREL}" >> "${CONTROL}"
echo "Architecture: ${ARCH}"        >> "${CONTROL}"
echo "Depends: ${DEPENDS}"          >> "${CONTROL}"
echo "Maintainer: ${MAINTAINER}"    >> "${CONTROL}"
echo "Description: ${PKGDESC}"      >> "${CONTROL}"

cp "autoremap.py" "${distname}/opt/surfacebook2-button-autoremap/"
cp "surfacebook2-button-autoremap.service" "${distname}/etc/systemd/system/"

dpkg-deb --build "${distname}"

rm -rf "${distname}"
