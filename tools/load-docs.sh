#!/bin/bash

set -e
set -o pipefail

DOCS_ROOT=/var/www/pgaweb/static/docs
FTP_ROOT=/var/ftp/pgadmin4

if [ $# -ne 1 ]
then
  echo "usage: $0 <version number>"
  exit 1
fi

VERSION=$1

# The version is interpolated into the tarball path and into the name of the
# directory we unpack into, so its shape is checked before it is used for
# either, because a value carrying a slash, a '..' or a shell metacharacter
# would let whoever called us choose those paths rather than merely name a
# release.
if [[ ! ${VERSION} =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]
then
  echo "Invalid version number (${VERSION}); expected something like 9.18 or 9.18.1."
  exit 1
fi

TARBALL=${FTP_ROOT}/v${VERSION}/docs/pgadmin4-${VERSION}-docs.tar.gz
DOCS_DIR=pgadmin4-${VERSION}-docs

# Check the docs file exists
if [ ! -f "${TARBALL}" ]
then
  echo "The source tarball (${TARBALL}) could not be found."
  exit 1
fi

# Everything below happens in a staging directory beside the live one, so that
# a tarball which turns out to be bad, or an unpacking that dies part way
# through, cannot leave the site serving a half replaced tree. It sits inside
# DOCS_ROOT so that moving the result into place is a rename rather than a copy
# of the best part of a gigabyte.
STAGING=$(mktemp -d "${DOCS_ROOT}/.load-docs.XXXXXX")
trap 'rm -rf "${STAGING}"' EXIT

# The tarball is assembled by a CI runner and lands in a tree that an upload
# key can write to, so it is untrusted input, and an archive decides for itself
# where its contents are written. We therefore vet the member list before
# unpacking anything, rather than trusting whatever a given tar happens to do
# with a hostile archive, since that varies between implementations and
# versions and is not a control we own. The two listings also fail the script
# outright if the archive cannot be read from end to end.
tar -tzvf "${TARBALL}" > "${STAGING}/listing.verbose"
tar -tzf "${TARBALL}" > "${STAGING}/listing.names"

# Every member must be a plain file or a directory, which rejects symlinks and
# hard links whose targets could redirect a later member out of the docs tree,
# along with devices and anything else that has no business in a docs tarball.
# A listing line we cannot make sense of fails this test as well, which is the
# right way round for it to fail.
if cut -c1 "${STAGING}/listing.verbose" | sort -u | grep -qv '^[-d]$'
then
  echo "${TARBALL} holds members that are neither plain files nor directories."
  exit 1
fi

# Every member must also sit under the one directory we expect, which rejects
# absolute paths and '..' traversal, and confirms the archive carries the
# single top level directory that the docloader below is pointed at.
while read -r MEMBER
do
  case ${MEMBER} in
    "${DOCS_DIR}"|"${DOCS_DIR}"/)
      ;;
    "${DOCS_DIR}"/*)
      case ${MEMBER} in
        */../*|*/..)
          echo "${TARBALL} holds a member traversing out of ${DOCS_DIR} (${MEMBER})."
          exit 1
          ;;
      esac
      ;;
    *)
      echo "${TARBALL} holds a member outside ${DOCS_DIR} (${MEMBER})."
      exit 1
      ;;
  esac
done < "${STAGING}/listing.names"

rm -f "${STAGING}/listing.verbose" "${STAGING}/listing.names"

# Unpack the tarball
tar -xzf "${TARBALL}" -C "${STAGING}" --no-same-owner --no-same-permissions

# Confirm we got out what we expected, rather than assuming that a tar which
# exited zero wrote the docs we are about to load and publish. The second check
# is belt and braces over the member vetting above, and catches a tar that
# creates something odd from an archive whose listing looked ordinary.
if [ ! -f "${STAGING}/${DOCS_DIR}/index.html" ]
then
  echo "${TARBALL} did not unpack to ${DOCS_DIR} holding an index.html."
  exit 1
fi

if [ -n "$(find "${STAGING}" ! -type d ! -type f -print -quit)" ]
then
  echo "${TARBALL} unpacked something that is neither a plain file nor a directory."
  exit 1
fi

# Swap the new docs into place, keeping the old copy until the new one has
# landed so that reloading a version we already hold does not leave a gap.
if [ -e "${DOCS_ROOT}/${DOCS_DIR}" ]
then
  rm -rf "${DOCS_ROOT}/${DOCS_DIR}.replaced"
  mv "${DOCS_ROOT}/${DOCS_DIR}" "${DOCS_ROOT}/${DOCS_DIR}.replaced"
fi
mv "${STAGING}/${DOCS_DIR}" "${DOCS_ROOT}/${DOCS_DIR}"
rm -rf "${DOCS_ROOT}/${DOCS_DIR}.replaced"

# Load 'em
cd /var/www/pgaweb
source /usr/share/python3/pginfra-virtualenv-django52-py3/bin/activate
./manage.py docloader pgadmin4 "${VERSION}" "${DOCS_DIR}"

# Clear the cache
sudo varnishadm "ban req.url ~ ."
