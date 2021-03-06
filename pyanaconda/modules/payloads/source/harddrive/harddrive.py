#
# Kickstart module for Hard drive payload source.
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

from pyanaconda.core.constants import INSTALL_TREE
from pyanaconda.core.signal import Signal

from pyanaconda.modules.payloads.constants import SourceType
from pyanaconda.modules.payloads.source.source_base import PayloadSourceBase
from pyanaconda.modules.payloads.source.harddrive.harddrive_interface import \
    HardDriveSourceInterface
from pyanaconda.modules.payloads.source.harddrive.initialization import \
    SetUpHardDriveSourceTask, TearDownHardDriveSourceTask

from pyanaconda.anaconda_loggers import get_module_logger
log = get_module_logger(__name__)


class HardDriveSourceModule(PayloadSourceBase):
    """The Hard drive source payload module."""

    def __init__(self):
        super().__init__()
        self._directory = ""
        self.directory_changed = Signal()
        self._device = ""
        self.device_changed = Signal()
        self._install_tree_path = ""
        self._device_mount = INSTALL_TREE + "_device"
        self._iso_mount = INSTALL_TREE + "_iso"

    @property
    def type(self):
        """Get type of this source."""
        return SourceType.HDD

    def is_ready(self):
        """This source is ready for the installation to start."""
        # TODO: this should be check on a special directory for every source
        res = os.path.ismount(self._device_mount) and bool(self._install_tree_path)
        log.debug("Source is set to %s ready state", res)
        return res

    def for_publication(self):
        """Get the interface used to publish this source."""
        return HardDriveSourceInterface(self)

    @property
    def directory(self):
        """Path to the repository on the partition.

        :rtype: str
        """
        return self._directory

    def set_directory(self, directory):
        """Set path to the repository on the partition.

        :param directory: the path
        :type directory: str
        """
        self._directory = directory
        self.directory_changed.emit()
        log.debug("Hard drive directory is set to '%s'", self._directory)

    @property
    def device(self):
        """Device containing the repository.

        :rtype: str
        """
        return self._device

    def set_device(self, device):
        """Set device containing the directory.

        :param device: a device spec for the partition
        :type device: str
        """
        self._device = device
        self.device_changed.emit()
        log.debug("Hard drive partition is set to '%s'", self._device)

    @property
    def install_tree_path(self):
        """Path to the install tree.

        Read only, and available only after the setup task finishes successfully.

        :rtype: str
        """
        return self._install_tree_path

    def set_up_with_tasks(self):
        """Set up the installation source.

        :return: list of tasks required for the source setup
        :rtype: [Task]
        """
        task = SetUpHardDriveSourceTask(
            self._device_mount,
            self._iso_mount,
            self._device,
            self._directory
        )
        task.succeeded_signal.connect(lambda: self._handle_setup_task_result(task))
        return [task]

    def tear_down_with_tasks(self):
        """Tear down the installation source.

        :return: list of tasks required for the source clean-up
        :rtype: [Task]
        """
        task = TearDownHardDriveSourceTask(self._device_mount, self._iso_mount,)
        return [task]

    def _handle_setup_task_result(self, task):
        self._install_tree_path = task.get_result()
        log.debug("Hard drive install tree path is set to '%s'", self._install_tree_path)
