# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright 2026 @saturday06
from . import registration

bl_info = {
    "name": "Shadow Manipulation Lab",
    "author": "saturday06",
    "version": (
        6,  # x-release-please-major
        0,  # x-release-please-minor
        0,  # x-release-please-patch
    ),
    "blender": (2, 93, 0),
    "location": "File > Import-Export",
    "description": "Import-Edit-Export VRM",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "https://github.com/saturday06/shadow-manipulation-lab/issues",
    "category": "Import-Export",
}


def register() -> None:
    registration.register()


def unregister() -> None:
    registration.unregister()


if __name__ == "__main__":
    register()
