# shadow-manipulation-lab

Hi!

- shadow_manipulation_lab.save_restart_load
- shadow_manipulation_lab.restart_import
- shadow_manipulation_lab.save_restart_export

```text
git checkout main

# Blender 4.2以上の場合

# Linux
ln -s "$PWD/shadow_manipulation_lab" "$HOME/.config/blender/BLENDER_VERSION/extensions/user_default/shadow_manipulation_lab"
# macOS
ln -s "$PWD/shadow_manipulation_lab" "$HOME/Library/Application Support/Blender/BLENDER_VERSION/extensions/user_default/shadow_manipulation_lab"
# Windows PowerShell
New-Item -ItemType Junction -Path "$Env:APPDATA\Blender Foundation\Blender\BLENDER_VERSION\extensions\user_default\shadow_manipulation_lab" -Value "$(Get-Location)\shadow_manipulation_lab"
# Windows Command Prompt
mklink /j "%APPDATA%\Blender Foundation\Blender\BLENDER_VERSION\extensions\user_default\shadow_manipulation_lab" shadow_manipulation_lab

# Blender 4.2未満の場合

# Linux
ln -s "$PWD/shadow_manipulation_lab" "$HOME/.config/blender/BLENDER_VERSION/scripts/addons/shadow_manipulation_lab"
# macOS
ln -s "$PWD/shadow_manipulation_lab" "$HOME/Library/Application Support/Blender/BLENDER_VERSION/scripts/addons/shadow_manipulation_lab"
# Windows PowerShell
New-Item -ItemType Junction -Path "$Env:APPDATA\Blender Foundation\Blender\BLENDER_VERSION\scripts\addons\shadow_manipulation_lab" -Value "$(Get-Location)\shadow_manipulation_lab"
# Windows Command Prompt
mklink /j "%APPDATA%\Blender Foundation\Blender\BLENDER_VERSION\scripts\addons\shadow_manipulation_lab" shadow_manipulation_lab
```
