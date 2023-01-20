# shadow-manipulation-lab

Hello!

```
# Linux
ln -s "$PWD/shadow_manipulation_lab" "$HOME/.config/blender/BLENDER_VERSION/scripts/addons/shadow-manipulation-lab-repo"
# macOS
ln -s "$PWD/shadow_manipulation_lab" "$HOME/Library/Application Support/Blender/BLENDER_VERSION/scripts/addons/shadow-manipulation-lab-repo"
# Windows PowerShell
New-Item -ItemType Junction -Path "$Env:APPDATA\Blender Foundation\Blender\BLENDER_VERSION\scripts\addons\shadow-manipulation-lab-repo" -Value "$(Get-Location)\shadow_manipulation_lab"
# Windows Command Prompt
mklink /j "%APPDATA%\Blender Foundation\Blender\BLENDER_VERSION\scripts\addons\shadow-manipulation-lab-repo" shadow_manipulation_lab
```
m 
