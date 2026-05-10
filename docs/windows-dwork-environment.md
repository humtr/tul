# Windows `D:\work` Environment

This document describes the Windows track for `tul`.

The goal is a reproducible local terminal environment where AI-assisted work can happen inside `D:\work` without scattering state across the normal Windows user profile.

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
    downloads\
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
D:\work\wt\wt.exe = normal/shared Windows Terminal
D:\work\wt\D Work Terminal.lnk = user-specific D:\work development terminal
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

The updater should never delete old runtimes immediately.

It should move them into:

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

Some networks or security tools insert a local CA certificate. Node-based CLIs may fail with:

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

For ordinary Windows downloads, `tul` should not require the user to manually move files from the downloads folder into `D:\work\var\tmp`.

The normal intake location is:

```text
D:\work\files\downloads
```

For downloaded update packages, `tul` should create package-local working directories under:

```text
D:\work\files\downloads\.tul\work
```

Example package work directory:

```text
D:\work\files\downloads\.tul\work\<package-id>\
  source.zip
  extracted\
  report.md
```

Only reviewed output files should be copied into:

```text
D:\work\prj\
```

Example flow:

```powershell
$work = "D:\work\files\downloads\.tul\work\tul-roadmap-20260511-001530"
New-Item -ItemType Directory -Force -Path $work | Out-Null
Copy-Item D:\work\files\downloads\package.zip "$work\source.zip" -Force
Expand-Archive "$work\source.zip" -DestinationPath "$work\extracted" -Force
Copy-Item "$work\extracted\docs\file.md" D:\work\prj\tul\docs\ -Force
```

After the update is complete, the package-local work directory may be deleted or moved to:

```text
D:\work\files\downloads\.tul\archive
```

Default behavior should prefer archiving over deletion. Deletion should require an explicit user request.

`D:\work\var\tmp` remains available for large scratch work and non-download temporary work, but it is not required for ordinary downloaded update packages.

---

## 9. Default update command

The normal Windows flow should become:

```powershell
Set-Location D:\work\prj\ai
tul sync .
tul update . --files lib\ai_tui.py --message "Update ai TUI handling"
```

`update` should complete the loop:

```text
download intake
→ package work root
→ apply
→ check
→ sweep
→ explicit-file stage
→ staged check
→ commit
→ push
→ remote verification
→ rollback hint
→ report
```

This is what allows Termux to continue from the same remote branch.

---

## 10. LLM-user-terminal-LLM loop

The Windows track should support a fluid loop across multiple LLM surfaces:

```text
ChatGPT / Codex / Gemini
→ user decision
→ D Work Terminal
→ local repo/runtime
→ tul commit/push
→ tul report
→ ChatGPT / Codex / Gemini
```

The important boundary is not which LLM is used.

The important boundary is that the user remains the approval point for applying, committing, pushing, or changing local runtimes.

---

## 11. Boundaries for AI agents

When running Codex/Gemini in a repo, the initial instruction should constrain the work root:

```text
작업 범위는 D:\work\prj\로 제한해.
D:\work\home, D:\work\wt, D:\work\tools, D:\work\var, D:\work\archive는 수정하지 마.
```

`tul` should eventually make these boundaries visible in reports and package manifests.
