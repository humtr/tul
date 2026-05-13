# environment profiles

This document owns repo-relevant environment profiles for `tul`.

It is not part of the default LLM read-next. Read it only when the task concerns platform setup, local workspace layout, path boundaries, agent permissions, or cross-device continuation.

## Ownership boundary

Environment profiles may describe reproducible local layouts and safety boundaries. They must not contain private secrets, API keys, tokens, machine-specific credentials, or personal shell aliases that are not needed to understand the repo.

Durable rules:

```text
- repo policy belongs in .tul.yml;
- global user aliases and machine-local secrets stay outside the repo;
- environment profile docs describe boundaries and expected layout, not private credential values;
- platform-specific notes should live here instead of becoming separate active root docs.
```

## Profiles

Current profile:

```text
windows-dwork = Windows D:\work development environment
```

Future profiles can be added as sections or split into child documents under `docs/environments/` when they become large enough.

---

# Profile: windows-dwork

## Purpose

The Windows `D:\work` profile describes a reproducible local terminal environment where AI-assisted work can happen inside `D:\work` without scattering operational state across the normal Windows user profile.

This is an environment note, not a command-surface source of truth. Current `tul` commands remain owned by `docs/commands.md`.

## Target layout

```text
D:\work\
  bin\
    ai\
  wt\
    wt.exe
    WindowsTerminal.exe
    wt.ps1
    D Work Terminal.lnk
    settings\
      settings.json
  prj\
    ai\
    tul\
  home\
    .codex\
    .gemini\
    .ssh\
    .config\
      certs\
  tools\
    apps\
      vscode\
    runtimes\
      git\
      nodejs\
      python\
    cli\
      codex\
      gemini\
    npm-global\
  var\
    cache\
      npm\
      pip\
      xdg\
    tmp\
    backup\
    archive\
  files\
    downloads\
```

## Terminal entrypoint

```text
D:\work\wt\wt.exe = normal/shared Windows Terminal
D:\work\wt\D Work Terminal.lnk = user-specific D:\work development terminal
D:\work\wt\wt.ps1 = process-local profile script
```

The shared Windows Terminal should remain normal. The D Work shortcut may load the D Work environment.

## Process-local environment variables

`wt.ps1` should prefer process-local variables rather than global Windows profile changes.

```powershell
$env:WORK_ROOT = "D:\work"
$env:WORK_HOME = "D:\work\home"
$env:HOME = "D:\work\home"
$env:USERPROFILE = "D:\work\home"
$env:CODEX_HOME = "D:\work\home\.codex"
$env:GEMINI_HOME = "D:\work\home\.gemini"
$env:NPM_CONFIG_PREFIX = "D:\work\tools\npm-global"
$env:NPM_CONFIG_CACHE = "D:\work\var\cache\npm"
$env:NPM_CONFIG_USERCONFIG = "D:\work\home\.npmrc"
$env:PIP_CACHE_DIR = "D:\work\var\cache\pip"
$env:XDG_CACHE_HOME = "D:\work\var\cache\xdg"
```

Recommended PATH order:

```text
D:\work\bin
D:\work\bin\ai
D:\work\tools\npm-global
D:\work\tools\apps\vscode\bin
D:\work\tools\runtimes\git\cmd
D:\work\tools\runtimes\git\bin
D:\work\tools\runtimes\nodejs
D:\work\tools\runtimes\python
D:\work\tools\runtimes\python\Scripts
D:\work\tools\cli\codex\app\node_modules\.bin
D:\work\tools\cli\gemini\app\node_modules\.bin
```

## Runtime management

Runtime locations:

```text
D:\work\tools\runtimes\git
D:\work\tools\runtimes\nodejs
D:\work\tools\runtimes\python
```

Guidelines:

```text
- prefer portable or explicitly targeted runtimes;
- avoid global PATH mutation when the D Work terminal can supply process-local PATH;
- back up replaced runtimes under D:\work\var\backup\runtimes;
- prefer archive-over-delete for environment work unless the user explicitly requests deletion.
```

## Codex / Gemini / npm state

```text
Codex state: D:\work\home\.codex
Gemini state: D:\work\home\.gemini
npm global packages: D:\work\tools\npm-global
```

Commands such as the following should be run inside D Work Terminal so state stays inside the profile:

```powershell
npm i -g @openai/codex
npm i -g @google/gemini-cli
```

## GitHub SSH over port 443

When port 22 is blocked, use GitHub SSH over HTTPS port 443.

`D:\work\home\.ssh\config`:

```sshconfig
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile D:/work/home/.ssh/github_dwork
  IdentitiesOnly yes
```

If needed, force Git to use the D Work SSH config:

```powershell
git config --global core.sshCommand "ssh -F D:/work/home/.ssh/config"
```

Expected remote forms:

```text
git@github.com:humtr/ai.git
git@github.com:humtr/tul.git
```

## Local CA / TLS interception

Node-based CLIs may fail under local TLS interception with certificate chain errors. Keep local CA configuration under:

```text
D:\work\home\.config\certs
```

Example:

```powershell
$env:NODE_EXTRA_CA_CERTS = "D:\work\home\.config\certs\btc-root.pem"
```

Avoid:

```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
```

except for short-lived emergency diagnosis.

## Safe download intake

Ordinary downloaded packages should enter through:

```text
D:\work\files\downloads
```

Package-local work directories may live under:

```text
D:\work\files\downloads\.tul\work
```

Only reviewed output files should be copied into:

```text
D:\work\prj\
```

Default cleanup should prefer archiving over deletion.

## AI-agent boundaries

When running Codex/Gemini in a repo, constrain the work root:

```text
작업 범위는 D:\work\prj\로 제한해.
D:\work\home, D:\work\wt, D:\work\tools, D:\work\var, D:\work\archive는 수정하지 마.
```

`tul` should make these boundaries visible in reports and package manifests only when such environment work is in scope.
