param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDir,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourcePath = Resolve-Path $SourceDir

if (-not (Test-Path $sourcePath)) {
    throw "SourceDir not found: $SourceDir"
}

$outputPath = Join-Path $repoRoot $OutputDir
$analysisDir = Join-Path $outputPath "analysis"
New-Item -ItemType Directory -Force -Path $outputPath | Out-Null
New-Item -ItemType Directory -Force -Path $analysisDir | Out-Null

$jobs = @()

function Add-ParserJob {
    param(
        [string]$FileName,
        [string]$ScriptName,
        [string]$OutputName
    )

    $inputFile = Join-Path $sourcePath $FileName
    if (Test-Path $inputFile) {
        $outputFile = Join-Path $analysisDir $OutputName
        python (Join-Path $repoRoot "tools\$ScriptName") --file $inputFile --output $outputFile
        $script:jobs += $outputFile
    }
}

Add-ParserJob -FileName "manual-profile.txt" -ScriptName "manual_profile_parser.py" -OutputName "manual-profile.analysis.json"
Add-ParserJob -FileName "chat.txt" -ScriptName "chat_parser.py" -OutputName "chat.analysis.json"
Add-ParserJob -FileName "notice.txt" -ScriptName "notice_parser.py" -OutputName "notice.analysis.json"
Add-ParserJob -FileName "meeting.txt" -ScriptName "meeting_parser.py" -OutputName "meeting.analysis.json"
Add-ParserJob -FileName "policy.txt" -ScriptName "policy_parser.py" -OutputName "policy.analysis.json"
Add-ParserJob -FileName "annotation.txt" -ScriptName "annotation_parser.py" -OutputName "annotation.analysis.json"

if ($jobs.Count -eq 0) {
    throw "No supported input files found in $sourcePath"
}

$bundlePath = Join-Path $outputPath "bundle.json"
python (Join-Path $repoRoot "tools\distillation_bundle_builder.py") --inputs $jobs --output $bundlePath

Write-Host ""
Write-Host "Import finished."
Write-Host "Source: $sourcePath"
Write-Host "Analysis dir: $analysisDir"
Write-Host "Bundle: $bundlePath"
