# set-git-push.ps1
# Monitors a local SharePoint-synced repo and auto-commits/pushes changes to GitHub.
# -------------------------------------------------------------------------------
# QUICK START
# 1) Set $repoPath below to your local SharePoint-synced Git repo.
# 2) Run from PowerShell:
#    powershell -ExecutionPolicy Bypass -File .\set-git-push.ps1
# Optional: override defaults at runtime:
#    powershell -ExecutionPolicy Bypass -File .\set-git-push.ps1 -RepoPath "C:\Path\To\Repo" -DebounceSeconds 10
# -------------------------------------------------------------------------------

# Update this to your local SharePoint-synced Git repo path.
$repoPath = "C:\Path\To\Your\Local\GitHubRepo"

[CmdletBinding()]
param(
    [string]$RepoPath = $repoPath,

    # Wait this long after the last file change before committing/pushing.
    [int]$DebounceSeconds = 10
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Write-Host "[$timestamp] $Message"
}

function Push-RepoChanges {
    Set-Location $RepoPath

    # Pull before committing to reduce conflicts
    Write-Log "Pulling latest changes from origin/main."
    git pull origin main | Out-Host

    $changes = git status --porcelain
    if ($changes -ne "") {
        Write-Log "Changes detected. Committing and pushing."
        git add .

        $commitMessage = "Auto-update from SharePoint on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git commit -m $commitMessage | Out-Host
        git push origin main | Out-Host

        Write-Log "Changes successfully pushed to GitHub."
    } else {
        Write-Log "No changes to commit. Repository is up-to-date."
    }
}

if (-not (Test-Path -Path $RepoPath -PathType Container)) {
    throw "RepoPath does not exist: $RepoPath"
}

Write-Log "Watching $RepoPath for changes (debounce ${DebounceSeconds}s)."

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $RepoPath
$watcher.Filter = '*'
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, LastWrite, DirectoryName'

$script:pending = $false
$script:lastEvent = Get-Date

$action = {
    # Ignore .git changes
    if ($EventArgs.FullPath -match "\\.git\\") { return }

    $script:pending = $true
    $script:lastEvent = Get-Date
}

Register-ObjectEvent -InputObject $watcher -EventName Created -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Changed -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Renamed -Action $action | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $action | Out-Null

$watcher.EnableRaisingEvents = $true

try {
    while ($true) {
        Start-Sleep -Seconds 2
        if ($script:pending) {
            $sinceLast = (Get-Date) - $script:lastEvent
            if ($sinceLast.TotalSeconds -ge $DebounceSeconds) {
                $script:pending = $false
                Push-RepoChanges
            }
        }
    }
}
finally {
    $watcher.EnableRaisingEvents = $false
    $watcher.Dispose()
    Write-Log "Watcher stopped."
}
