# tul config spec

`tul` has three configuration layers:

1. Global config: user/platform paths and project aliases.
2. Repo config: `.tul.yml` inside the target repository.
3. Package manifest: `tul-package.yml` inside the incoming archive.

The global config path defaults to:

- Windows: `D:\work\home\.config\tul\config.yml` when that home exists, otherwise `%USERPROFILE%\.config\tul\config.yml`
- Termux/Linux: `~/.config/tul/config.yml`
- Override: `$TUL_CONFIG`

Environment paths and project aliases belong in global config, not engine code.
Project-specific branch/check policy belongs in `.tul.yml`, not engine code.
