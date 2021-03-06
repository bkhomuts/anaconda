#
# Factory class to create sources.
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
from pyanaconda.modules.payloads.constants import SourceType

__all__ = ["SourceFactory"]


class SourceFactory(object):
    """Factory to create payload sources."""

    @staticmethod
    def create_source(source_type: SourceType):
        """Create a source module.

        :param source_type: a source type
        :return: a source module
        """
        if source_type == SourceType.LIVE_OS_IMAGE:
            from pyanaconda.modules.payloads.source.live_os.live_os import LiveOSSourceModule
            return LiveOSSourceModule()
        elif source_type == SourceType.CDROM:
            from pyanaconda.modules.payloads.source.cdrom.cdrom import CdromSourceModule
            return CdromSourceModule()
        elif source_type == SourceType.HMC:
            from pyanaconda.modules.payloads.source.hmc.hmc import HMCSourceModule
            return HMCSourceModule()
        elif source_type == SourceType.REPO_FILES:
            from pyanaconda.modules.payloads.source.repo_files.repo_files import \
                RepoFilesSourceModule
            return RepoFilesSourceModule()
        elif source_type == SourceType.NFS:
            from pyanaconda.modules.payloads.source.nfs.nfs import NFSSourceModule
            return NFSSourceModule()
        elif source_type == SourceType.URL:
            from pyanaconda.modules.payloads.source.url.url import URLSourceModule
            return URLSourceModule()
        elif source_type == SourceType.HDD:
            from pyanaconda.modules.payloads.source.harddrive.harddrive import \
                HardDriveSourceModule
            return HardDriveSourceModule()

        raise ValueError("Unknown source type: {}".format(source_type))
