import contextlib
import functools
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Set as AbstractSet
from pathlib import Path
from typing import Optional, Union

import bpy
from bpy.app.handlers import persistent

AUTO_EXPORT_OPTION = "--shadow-manipulation-lab-export"
AUTO_IMPORT_OPTION = "--shadow-manipulation-lab-import"


def auto_import() -> None:
    if not bpy.data.filepath:
        return

    vrm_path = Path(bpy.data.filepath).with_suffix(".vrm")
    vrma_path = Path(bpy.data.filepath).with_suffix(".vrma")

    if vrm_path.exists():
        key = "BLENDER_VRM_AUTOMATIC_LICENSE_CONFIRMATION"
        val = os.environ.get(key)
        os.environ[key] = "true"
        bpy.ops.import_scene.vrm(  # type: ignore[attr-defined]
            filepath=str(vrm_path),
        )
        if val is not None:
            os.environ[key] = val
        else:
            del os.environ[key]
    elif vrma_path.exists():
        bpy.ops.import_scene.vrma(  # type: ignore[attr-defined]
            filepath=str(vrma_path),
        )


def auto_export() -> None:
    if not bpy.data.filepath:
        return

    vrm_path = Path(bpy.data.filepath).with_suffix(".vrm")
    vrma_path = Path(bpy.data.filepath).with_suffix(".vrma")
    if vrm_path.exists():
        vrm_path.unlink()
        glb_path = vrm_path.with_suffix(".glb")
        if glb_path.exists():
            glb_path.unlink()
        bpy.ops.export_scene.vrm(  # type: ignore[attr-defined]
            filepath=str(vrm_path),
        )
        shutil.copy(vrm_path, glb_path)
    elif vrma_path.exists():
        bpy.ops.export_scene.vrma(  # type: ignore[attr-defined]
            filepath=str(vrma_path),
        )


def auto_import_vrma_debug() -> None:
    if not bpy.data.filepath:
        return

    vrma_path = Path(bpy.data.filepath).with_suffix(".vrma")
    if not vrma_path.exists():
        return

    bpy.ops.import_scene.vrma(  # type: ignore[attr-defined]
        filepath=str(vrma_path),
    )


@persistent
def load_post(_dummy: object) -> None:
    if "--" not in sys.argv:
        return

    extra_args = sys.argv[sys.argv.index("--") + 1 :]

    if AUTO_IMPORT_OPTION in extra_args:
        bpy.app.timers.register(auto_import, first_interval=0.5)
        return

    if AUTO_EXPORT_OPTION in extra_args:
        bpy.app.timers.register(auto_export, first_interval=0.5)
        return

    bpy.app.timers.register(auto_import_vrma_debug, first_interval=0.5)


def wait_for_start_ok(path: Path) -> Optional[float]:
    if path.read_text(encoding="ascii").strip() == "start_ok":
        bpy.ops.wm.quit_blender()
        return None
    return 0.5


def create_named_temporary_file(prefix: str = "", suffix: str = "") -> Path:
    # pylint: disable=consider-using-with;
    return Path(
        tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False).name
    )
    # pylint: enable=consider-using-with;


def start_blender_and_quit(path: Path, extra_arg: Optional[str] = None) -> None:
    start_ok_file_path = create_named_temporary_file(prefix="start_ok")

    restart_script = Path(__file__).parent / "restart"
    if platform.system() == "Windows":
        binary_path = Path(bpy.app.binary_path)
        launcher_path = binary_path.with_stem("blender-launcher")
        if launcher_path.exists():
            binary_path = launcher_path
        restart_environ = os.environ.copy()
        restart_environ["SML_WAIT_PID"] = str(os.getpid())
        restart_environ["SML_BLENDER_PATH"] = str(binary_path)
        restart_environ["SML_BLEND_FILE_PATH"] = str(path)
        restart_environ["SML_START_OK_FILE_PATH"] = str(start_ok_file_path)
        restart_environ["SML_EXTRA_ARG"] = extra_arg if extra_arg else ""
        # pylint: disable=consider-using-with;
        subprocess.Popen(
            [
                restart_environ["COMSPEC"],
                "/c",
                "start",
                "",  # title
                str(restart_script.with_suffix(".bat")),
            ],
            env=restart_environ,
        )
        # pylint: enable=consider-using-with;
    else:
        # pylint: disable=consider-using-with;
        args: list[Union[str, Path]] = [
            str(restart_script.with_suffix(".sh")),
            str(os.getpid()),
            start_ok_file_path,
            bpy.app.binary_path,
            path,
            "--",
        ]
        if extra_arg:
            args.append(extra_arg)
        subprocess.Popen(
            args,
            start_new_session=True,
        )
        # pylint: enable=consider-using-with;
    bpy.app.timers.register(functools.partial(wait_for_start_ok, start_ok_file_path))


class SHADOW_MANIPULATION_LAB_OT_save_restart_load(bpy.types.Operator):
    bl_idname = "shadow_manipulation_lab.save_restart_load"
    bl_label = "Shadow Manipulation Lab: Save Restart Load"
    bl_description = "Save Restart Load"
    bl_options: AbstractSet[str] = {"REGISTER"}

    def execute(self, _context: bpy.types.Context) -> set[str]:
        reload_path = Path(bpy.data.filepath)
        if not bpy.data.filepath or not reload_path.exists():
            reload_path = create_named_temporary_file(prefix="reload", suffix=".blend")
        old_path = reload_path.with_suffix(".old.blend")
        bpy.ops.wm.save_as_mainfile(filepath=str(reload_path), check_existing=False)
        bpy.ops.wm.save_as_mainfile(filepath=str(old_path), check_existing=False)

        start_blender_and_quit(reload_path)
        return {"FINISHED"}


class SHADOW_MANIPULATION_LAB_OT_restart_import(bpy.types.Operator):
    bl_idname = "shadow_manipulation_lab.restart_import"
    bl_label = "Shadow Manipulation Lab: Restart Import"
    bl_description = "Restart Import"
    bl_options: AbstractSet[str] = {"REGISTER"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        reload_path = Path(bpy.data.filepath)
        if not bpy.data.filepath or not reload_path.exists():
            message = "Please save .blend file"
            raise ValueError(message)

        bpy.ops.wm.save_as_mainfile(
            filepath=str(reload_path.with_suffix(".old.blend")),
            check_existing=False,
            copy=True,
        )

        if context.view_layer.objects.active is not None and context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        for _ in range(3):
            for c in bpy.data.collections:
                for obj in list(c.objects):
                    if obj.type == "LIGHT":
                        continue
                    c.objects.unlink(obj)

            for obj in bpy.data.objects:
                if obj.type == "LIGHT":
                    obj.select_set(state=False)
                    continue
                obj.hide_render = False
                obj.hide_select = False
                obj.hide_viewport = False
                with contextlib.suppress(RuntimeError):
                    context.scene.collection.objects.link(obj)
                obj.select_set(state=True)

            bpy.ops.object.delete()

            while bpy.data.collections and list(bpy.data.collections) != [
                context.scene.collection
            ]:
                bpy.data.collections.remove(bpy.data.collections[0])

            for obj in bpy.data.objects:
                if obj.type == "LIGHT":
                    continue
                with contextlib.suppress(RuntimeError):
                    context.scene.collection.objects.unlink(obj)

            while bpy.ops.outliner.orphans_purge() == {"FINISHED"}:
                pass

        bpy.ops.wm.save_as_mainfile(filepath=str(reload_path), check_existing=False)

        start_blender_and_quit(reload_path, AUTO_IMPORT_OPTION)
        return {"FINISHED"}


class SHADOW_MANIPULATION_LAB_OT_save_restart_export(bpy.types.Operator):
    bl_idname = "shadow_manipulation_lab.save_restart_export"
    bl_label = "Shadow Manipulation Lab: Save Restart Export"
    bl_description = "Restart Import"
    bl_options: AbstractSet[str] = {"REGISTER"}

    def execute(self, _context: bpy.types.Context) -> set[str]:
        reload_path = Path(bpy.data.filepath)
        if not bpy.data.filepath or not reload_path.exists():
            message = "Please save .blend file"
            raise ValueError(message)
        bpy.ops.wm.save_as_mainfile(filepath=str(reload_path), check_existing=False)
        bpy.ops.wm.save_as_mainfile(
            filepath=str(reload_path.with_suffix(".old.blend")), check_existing=False
        )

        start_blender_and_quit(reload_path, AUTO_EXPORT_OPTION)
        return {"FINISHED"}
