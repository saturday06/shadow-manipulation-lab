#
#
# Please don't import anything in global scope to detect script reloading and minimize initialization.
#
#

bl_info = {
    "name": "Shadow Manipulation Lab",
    "author": "saturday06",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Edit-Export VRM",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "https://github.com/saturday06/shadow-manipulation-lab/issues",
    "category": "Import-Export",
}


def register() -> None:
    import bpy

    if bpy.app.version < bl_info["blender"]:
        raise Exception(
            f"This add-on doesn't support Blender version less than {bl_info['blender']} "
            + f"but the current version is {bpy.app.version}"
        )

    # Lazy import to minimize initialization before blender version checking and reload_package().
    # 'import io_scene_vrm' causes an error in blender and vscode mypy integration.
    # pylint: disable=import-self,no-name-in-module
    from .shadow_manipulation_lab import registration

    # pylint: enable=import-self,no-name-in-module

    registration.register()


def unregister() -> None:
    import bpy

    if bpy.app.version < bl_info["blender"]:
        return

    # Lazy import to minimize initialization before blender version checking and reload_package().
    # 'import io_scene_vrm' causes an error in blender and vscode mypy integration.
    # pylint: disable=import-self,no-name-in-module
    from .shadow_manipulation_lab import registration

    # pylint: enable=import-self,no-name-in-module

    registration.unregister()


if __name__ == "__main__":
    register()
