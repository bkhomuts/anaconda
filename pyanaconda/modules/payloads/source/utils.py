#
# Copyright (C) 2020 Red Hat, Inc.
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
#
import os

from blivet.arch import get_arch
from blivet.util import mount

from pyanaconda.core.storage import device_matches
from pyanaconda.payload.image import find_first_iso_image

from pyanaconda.anaconda_loggers import get_module_logger
log = get_module_logger(__name__)

__all__ = ["is_valid_install_disk", "find_and_mount_device", "find_and_mount_iso_image"]


def is_valid_install_disk(tree_dir):
    """Is the disk a valid installation repository?

    Success criteria:
    - Disk must be already mounted at tree_dir.
    - A .discinfo file exists.
    - Third line of .discinfo equals current architecture.

    :param str tree_dir: Where the disk is mounted.
    :rtype: bool
    """
    try:
        with open(os.path.join(tree_dir, ".discinfo"), "r") as f:
            f.readline()  # throw away timestamp
            f.readline()  # throw away description
            arch = f.readline().strip()
            if arch == get_arch():
                return True
    except OSError:
        pass
    return False


def find_and_mount_device(device_spec, mount_point):
    """Resolve what device to mount and do so, read-only.

    Assumes that the device is directly mountable without any preparations or dependencies.

    :param str device_spec: specification of the device
    :param str mount_point: where to mount the device

    :return: success or not
    :rtype: bool
    """
    matches = device_matches(device_spec)
    if not matches:
        log.error("Device spec %s does not resolve to anything", device_spec)
        return False

    device_path = "/dev/" + matches[0]

    try:
        mount(device_path, mount_point, "auto", "ro")
        return True
    except OSError as e:
        log.error("Mount of device failed: %s", e)
        return False


def find_and_mount_iso_image(image_location, mount_point):
    """Find a ISO image in a location and mount it.

    :param str image_location: where the image ISO file is
    :param str mount_point: where to mount the image

    :return: success or not
    :rtype: bool
    """
    image_filename = find_first_iso_image(image_location)
    if not image_filename:
        return False
    full_image_path = os.path.join(image_location, image_filename)
    try:
        mount(full_image_path, mount_point, fstype='iso9660', options="ro")
        return True
    except OSError as e:
        log.error("Mount of ISO file failed: %s", e)
        return False
