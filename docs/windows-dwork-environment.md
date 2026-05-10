# Windows D:\work Environment

This document describes the Windows track for `tul`.

The goal is a reproducible local terminal environment where AI-assisted work can happen inside `D:\work` without scattering state across the Windows user profile.

---

## 1. Target layout

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
```

---

## 2. Windows Terminal entrypoint

The normal Windows Terminal executable is:

```text
D:\work\wt\wt.exe
```

The personal D Work entrypoint is:

```text
D:\work\wt\D Work Terminal.lnk
```

The personal PowerShell environment code is:

```text
D:\work\wt\wt.ps1
```

Design rule:

```text
D:\work\wt\wt.exe
= normal/shared Windows Terminal

D:\work\wt\D Work Terminal.lnk
= user-specific D:\work development terminal
```

This keeps the shared terminal normal while allowing the user-specific shortcut to load the D Work environment.

---

## 3. D Work PowerShell environment

`wt.ps1` should set process-local environment variables such as:

```powershell
$env:WORK_ROOT = "D:\work"
$env:WORK_HOME = "D:\work\home"

$env:HOME = "D:\work\home"
$env:USERPROFILE = "D:\work\home"

$env:CODEX_HOME = "D:\work\home\.codex"

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

---

## 4. Runtime management

Runtime locations:

```text
D:\work\tools\runtimes\git
D:\work\tools\runtimes\nodejs
D:\work\tools\runtimes\python
```

Recommended update behavior:

```text
Git:
- use MinGit or PortableGit
- prefer ZIP replacement
- back up old runtime under D:\work\var\backup\runtimes

Node.js:
- use Windows x64 ZIP
- replace D:\work\tools\runtimes\nodejs
- keep npm global packages in D:\work\tools\npm-global

Python:
- prefer installer targeted to D:\work\tools\runtimes\python for development use
- avoid Windows global PATH changes
- prefer python -m pip over pip
```

The updater should never delete old runtimes immediately. It should move them into:

```text
D:\work\var\backup\runtimes
```

---

## 5. Codex CLI and Gemini CLI

Codex state should stay under:

```text
D:\work\home\.codex
```

Gemini state should stay under:

```text
D:\work\home\.gemini
```

npm global packages should stay under:

```text
D:\work\tools\npm-global
```

This allows:

```powershell
npm i -g @openai/codex
npm i -g @google/gemini-cli
```

without writing package state into the normal Windows user profile, assuming the command is run inside D Work Terminal.

---

## 6. GitHub SSH over port 443

Some networks block SSH port 22. In that case, use GitHub SSH over HTTPS port 443.

`D:\work\home\.ssh\config`:

```sshconfig
Host github.com
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile D:/work/home/.ssh/github_dwork
  IdentitiesOnly yes
```

If the OpenSSH client does not automatically read the D Work config, Git can be forced to use it:

```powershell
git config --global core.sshCommand "ssh -F D:/work/home/.ssh/config"
```

Expected remote form:

```text
git@github.com:humtr/ai.git
git@github.com:humtr/tul.git
```

---

## 7. Local CA / TLS interception handling

Some networks or security tools insert a local CA certificate.

Node-based CLIs may fail with:

```text
self-signed certificate in certificate chain
```

D Work should keep local CA configuration under:

```text
D:\work\home\.config\certs
```

Example:

```powershell
$env:NODE_EXTRA_CA_CERTS = "D:\work\home\.config\certs\btc-root.pem"
```

Do not set this globally unless needed. Keep it process-local inside D Work Terminal.

Avoid:

```powershell
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"
```

except for short-lived emergency diagnosis.

---

## 8. Safe import workflow

Do not unpack assistant-generated packages directly inside a repo.

Use:

```text
D:\work\var\tmp\<task>
```

Then copy only reviewed files into:

```text
D:\work\prj\<repo>
```

Example flow:

```powershell
New-Item -ItemType Directory -Force -Path D:\work\var\tmp\tul-roadmap | Out-Null
Expand-Archive .\package.zip -DestinationPath D:\work\var\tmp\tul-roadmap\extracted -Force

Copy-Item D:\work\var\tmp\tul-roadmap\extracted\docs\file.md D:\work\prj\tul\docs\ -Force
```

`tul` should eventually automate this as:

```bash
tul import latest
tul report D:\work\prj\tul
```

but it must still ask before applying or executing unknown scripts.

---

## 9. Boundaries for AI agents

When running Codex/Gemini in a repo, the initial instruction should constrain the work root:

```text
작업 범위는 D:\work\prj\<repo>로 제한해.
D:\work\home, D:\work\wt, D:\work\tools, D:\work\var, D:\work\archive는 수정하지 마.
```

`tul` should eventually make these boundaries visible in reports and package manifests.
