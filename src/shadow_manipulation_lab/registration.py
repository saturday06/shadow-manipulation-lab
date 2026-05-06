import bpy
import bpy.utils

from .development_support import restart

classes = [
    restart.SHADOW_MANIPULATION_LAB_OT_save_restart_load,
    restart.SHADOW_MANIPULATION_LAB_OT_restart_import,
    restart.SHADOW_MANIPULATION_LAB_OT_save_restart_export,
]


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.load_post.append(restart.load_post)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
