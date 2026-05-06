# Shadow Manipulation Lab

Yo!

### How to create a development link for Blender 4.2 or later

#### Linux

```sh
blender_version=4.5
mkdir -p "$HOME/.config/blender/$blender_version/extensions/user_default"
ln -Ts "$PWD/src/shadow_manipulation_lab" "$HOME/.config/blender/$blender_version/extensions/user_default/shadow_manipulation_lab"
```

#### macOS

```sh
blender_version=4.5
mkdir -p "$HOME/Library/Application Support/Blender/$blender_version/extensions/user_default"
ln -s "$PWD/src/shadow_manipulation_lab" "$HOME/Library/Application Support/Blender/$blender_version/extensions/user_default/shadow_manipulation_lab"
```

#### Windows PowerShell

```powershell
$blenderVersion = "4.5"
New-Item -ItemType Directory -Path "$Env:APPDATA\Blender Foundation\Blender\$blenderVersion\extensions\user_default" -Force
New-Item -ItemType Junction -Path "$Env:APPDATA\Blender Foundation\Blender\$blenderVersion\extensions\user_default\shadow_manipulation_lab" -Value "$(Get-Location)\src\shadow_manipulation_lab"
```

### How to create a development link for Blender 4.1.1 or earlier

#### Linux

```sh
blender_version=3.6
mkdir -p "$HOME/.config/blender/$blender_version/scripts/addons"
ln -Ts "$PWD/src/shadow_manipulation_lab" "$HOME/.config/blender/$blender_version/scripts/addons/shadow_manipulation_lab"
```

#### macOS

```sh
blender_version=3.6
mkdir -p "$HOME/Library/Application Support/Blender/$blender_version/scripts/addons"
ln -s "$PWD/src/shadow_manipulation_lab" "$HOME/Library/Application Support/Blender/$blender_version/scripts/addons/shadow_manipulation_lab"
```

#### Windows PowerShell

```powershell
$blenderVersion = "3.6"
New-Item -ItemType Directory -Path "$Env:APPDATA\Blender Foundation\Blender\$blenderVersion\scripts\addons" -Force
New-Item -ItemType Junction -Path "$Env:APPDATA\Blender Foundation\Blender\$blenderVersion\scripts\addons\shadow_manipulation_lab" -Value "$(Get-Location)\src\shadow_manipulation_lab"
```
