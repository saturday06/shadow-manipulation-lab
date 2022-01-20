import bpy
from bpy.app.handlers import persistent
from typing import Set, Any, Optional
import contextlib
import functools
import subprocess
import tempfile
import os
from os.path import dirname, join
import sys
import platform

AUTO_EXPORT_OPTION = "--shadow-manipulation-lab-export"
AUTO_IMPORT_OPTION = "--shadow-manipulation-lab-import"


def auto_import() -> None:
    if not bpy.data.filepath:
        return
    vrm_path = os.path.splitext(bpy.data.filepath)[0] + ".vrm"
    if not os.path.exists(vrm_path):
        raise Exception(f'No "{vrm_path}"')
    bpy.ops.import_scene.vrm(filepath=vrm_path)


def auto_export() -> None:
    if not bpy.data.filepath:
        return
    vrm_path = os.path.splitext(bpy.data.filepath)[0] + ".vrm"
    if os.path.exists(vrm_path):
        os.unlink(vrm_path)

    bpy.ops.export_scene.vrm(filepath=vrm_path)


if persistent:  # for fake-bpy-modules

    @persistent  # type: ignore[misc]
    def load_post(_dummy: Any) -> None:
        if "--" not in sys.argv:
            return

        extra_args = sys.argv[sys.argv.index("--") + 1 :]

        if AUTO_IMPORT_OPTION in extra_args:
            bpy.app.timers.register(auto_import, first_interval=0.5)
            return

        if AUTO_EXPORT_OPTION in extra_args:
            bpy.app.timers.register(auto_export, first_interval=0.5)
            return

else:

    def load_post(_dummy: Any) -> None:
        raise NotImplementedError


def wait_for_start_ok(path: str) -> Optional[float]:
    with open(path, "rt") as file:
        if file.read().strip() == "start_ok":
            bpy.ops.wm.quit_blender()
    return 0.5


def start_blender_and_quit(path: str, extra_arg: Optional[str] = None) -> None:
    start_ok_file_path = tempfile.NamedTemporaryFile(
        prefix="start_ok", delete=False
    ).name

    restart_script = join(
        dirname(dirname(dirname(__file__))),
        "scripts",
        "restart",
    )
    if platform.system() == "Windows":
        restart_environ = os.environ.copy()
        restart_environ["SML_WAIT_PID"] = str(os.getpid())
        restart_environ["SML_BLENDER_PATH"] = bpy.app.binary_path
        restart_environ["SML_BLEND_FILE_PATH"] = path
        restart_environ["SML_START_OK_FILE_PATH"] = start_ok_file_path
        restart_environ["SML_EXTRA_ARG"] = extra_arg if extra_arg else ""
        subprocess.Popen(
            [
                restart_environ["COMSPEC"],
                "/c",
                "start",
                "",  # title
                restart_script + ".bat",
            ],
            env=restart_environ,
        )
    else:
        subprocess.Popen(
            [
                restart_script + ".sh",
                str(os.getpid()),
                start_ok_file_path,
                bpy.app.binary_path,
                "--start-console",
                path,
                "--",
            ]
            + ([extra_arg] if extra_arg else []),
            start_new_session=True,
        )
    bpy.app.timers.register(functools.partial(wait_for_start_ok, start_ok_file_path))


class SHADOW_MANIPULATION_LAB_OT_save_restart_load(bpy.types.Operator):  # type: ignore[misc] # noqa: N801
    bl_idname = "shadow_manipulation_lab.save_restart_load"
    bl_label = "Shadow Manipulation Lab: Save Restart Load"
    bl_description = "Save Restart Load"
    bl_options = {"REGISTER"}

    def execute(self, _context: bpy.types.Context) -> Set[str]:
        print("Save Restart Load")
        reload_path = bpy.data.filepath
        if not reload_path or not os.path.exists(reload_path):
            reload_path = tempfile.NamedTemporaryFile(
                prefix="reload", suffix=".blend", delete=False
            ).name
        old_path = reload_path + ".old.blend"
        bpy.ops.wm.save_as_mainfile(filepath=reload_path, check_existing=False)
        bpy.ops.wm.save_as_mainfile(filepath=old_path, check_existing=False)

        start_blender_and_quit(reload_path)
        return {"FINISHED"}


class SHADOW_MANIPULATION_LAB_OT_restart_import(bpy.types.Operator):  # type: ignore[misc] # noqa: N801
    bl_idname = "shadow_manipulation_lab.restart_import"
    bl_label = "Shadow Manipulation Lab: Restart Import"
    bl_description = "Restart Import"
    bl_options = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> Set[str]:
        reload_path = bpy.data.filepath
        if not reload_path:
            raise Exception("Please save .blend file")

        bpy.ops.wm.save_as_mainfile(
            filepath=bpy.data.filepath + ".old.blend", check_existing=False, copy=True
        )

        for c in bpy.data.collections:
            for obj in list(c.objects):
                c.objects.unlink(obj)

        for obj in bpy.data.objects:
            obj.hide_render = False
            obj.hide_select = False
            obj.hide_viewport = False
            with contextlib.suppress(RuntimeError):
                context.scene.collection.objects.link(obj)
            obj.select_set(True)

        bpy.ops.object.delete()

        while bpy.data.collections:
            bpy.data.collections.remove(bpy.data.collections[0])

        while bpy.ops.outliner.orphans_purge() == {"FINISHED"}:
            pass

        bpy.ops.wm.save_as_mainfile(filepath=reload_path, check_existing=False)

        start_blender_and_quit(reload_path, AUTO_IMPORT_OPTION)
        return {"FINISHED"}


class SHADOW_MANIPULATION_LAB_OT_save_restart_export(bpy.types.Operator):  # type: ignore[misc] # noqa: N801
    bl_idname = "shadow_manipulation_lab.save_restart_export"
    bl_label = "Shadow Manipulation Lab: Save Restart Export"
    bl_description = "Restart Import"
    bl_options = {"REGISTER"}

    def execute(self, _context: bpy.types.Context) -> Set[str]:
        if not bpy.data.filepath:
            raise Exception("Please save .blend file")

        reload_path = bpy.data.filepath
        bpy.ops.wm.save_as_mainfile(filepath=reload_path, check_existing=False)
        bpy.ops.wm.save_as_mainfile(
            filepath=reload_path + ".old.blend", check_existing=False
        )

        start_blender_and_quit(reload_path, AUTO_EXPORT_OPTION)
        return {"FINISHED"}
