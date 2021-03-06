#
# Constants shared in the payload module.
#
# Copyright (C) 2019 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
from enum import Enum, unique

from pyanaconda.core.constants import URL_TYPE_BASEURL, URL_TYPE_MIRRORLIST, \
    URL_TYPE_METALINK, PAYLOAD_TYPE_DNF, PAYLOAD_TYPE_LIVE_OS, PAYLOAD_TYPE_LIVE_IMAGE


@unique
class PayloadType(Enum):
    """Type of the payload."""
    DNF = PAYLOAD_TYPE_DNF
    LIVE_OS = PAYLOAD_TYPE_LIVE_OS
    LIVE_IMAGE = PAYLOAD_TYPE_LIVE_IMAGE


@unique
class SourceType(Enum):
    """Type of the payload source."""
    LIVE_OS_IMAGE = "LIVE_OS_IMAGE"
    HMC = "HMC"
    CDROM = "CDROM"
    REPO_FILES = "REPO_FILES"
    NFS = "NFS"
    URL = "URL"
    HDD = "HDD"


@unique
class URLType(Enum):
    """Types of supported URL sources."""
    BASEURL = URL_TYPE_BASEURL
    MIRRORLIST = URL_TYPE_MIRRORLIST
    METALINK = URL_TYPE_METALINK
