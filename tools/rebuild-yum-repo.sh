#!/bin/sh

if [ $# -ne 3 ]; then
    echo "Usage: $0 <distro family (fedora|redhat)> <distro name (fedora|rhel)> <distro version>"
    exit 1
fi

DISTRO_FAMILY=$1
DISTRO_NAME=$2
DISTRO_VERSION=$3

/usr/bin/createrepo_c /var/ftp/pgadmin4/yum/${DISTRO_FAMILY}/${DISTRO_NAME}-${DISTRO_VERSION}-x86_64
/usr/bin/gpg --yes --detach-sign --armor /var/ftp/pgadmin4/yum/${DISTRO_FAMILY}/${DISTRO_NAME}-${DISTRO_VERSION}-x86_64/repodata/repomd.xml

cd /var/ftp/pgadmin4/yum/${DISTRO_FAMILY}/
ln -snf ${DISTRO_NAME}-${DISTRO_VERSION}-x86_64 ${DISTRO_NAME}-${DISTRO_VERSION}Server-x86_64
ln -snf ${DISTRO_NAME}-${DISTRO_VERSION}-x86_64 ${DISTRO_NAME}-${DISTRO_VERSION}Workstation-x86_64
ln -snf ${DISTRO_NAME}-${DISTRO_VERSION}-x86_64 ${DISTRO_NAME}-${DISTRO_VERSION}Client-x86_64
