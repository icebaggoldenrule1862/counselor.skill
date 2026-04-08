param(
    [string]$BundlePath = ".\generated\imports\current\out\bundle.json",
    [string]$Scene = "I need to talk to my counselor now."
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$resolvedBundlePath = Join-Path $repoRoot $BundlePath
$templatePath = Join-Path $repoRoot "prompts\local\counselor-bundle-prompt.txt"

$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

if (-not (Test-Path $resolvedBundlePath)) {
    throw "Bundle not found: $resolvedBundlePath"
}

if (-not (Test-Path $templatePath)) {
    throw "Template not found: $templatePath"
}

$bundle = Get-Content $resolvedBundlePath -Raw -Encoding UTF8
$template = Get-Content $templatePath -Raw -Encoding UTF8
$prompt = $template.Replace("{{BUNDLE}}", $bundle).Replace("{{SCENE}}", $Scene)

ollama run qwen3.5:4b --think=false --hidethinking $prompt
