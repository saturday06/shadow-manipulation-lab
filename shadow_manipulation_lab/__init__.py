#
#
# Please don't import anything in global scope to detect script reloading and minimize initialization.
#
#

bl_info = {
    "name": "Shadow Manipulation Lab",
    "author": "saturday06",
    "version": (
        0,  # x-release-please-major
        10,  # x-release-please-minor
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
    # Lazy import to minimize initialization before blender version checking and reload_package().
    from . import registration

    # pylint: enable=import-self,no-name-in-module

    registration.register()


def unregister() -> None:
    # Lazy import to minimize initialization before blender version checking and reload_package().
    from . import registration

    registration.unregister()


if __name__ == "__main__":
    register()
