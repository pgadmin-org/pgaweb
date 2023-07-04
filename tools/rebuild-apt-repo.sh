#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: $0 <distro codename>"
    exit 1
fi

DISTRO_CODENAME=$1

for ARCH in all amd64 i386; do
    mkdir -p /var/ftp/pgadmin4/apt/${DISTRO_CODENAME}/dists/pgadmin4/main/binary-${ARCH}
done

for ARCH in all amd64 i386; do
    cd /var/ftp/pgadmin4/apt/${DISTRO_CODENAME}
    apt-ftparchive packages -c=/home/pgaupload/aptftp.conf dists/pgadmin4/main/binary-${ARCH}  > dists/pgadmin4/main/binary-${ARCH}/Packages || exit 1
    gzip -f -k dists/pgadmin4/main/binary-${ARCH}/Packages || exit 1
done

cd /var/ftp/pgadmin4/apt/${DISTRO_CODENAME}/dists/pgadmin4
apt-ftparchive release -c=/home/pgaupload/aptftp.conf . > Release && gzip -f -k Release || exit 1

rm -f Release.gpg
gpg -u packages@pgadmin.org -bao Release.gpg Release || exit 1

rm -f InRelease
gpg -u packages@pgadmin.org --clear-sign --output InRelease Release || exit 1

