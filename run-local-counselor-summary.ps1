param(
    [string]$Scene = "I need to talk to my counselor now."
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $repoRoot "prompts\local\counselor-summary-prompt.txt"

$utf8 = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8
[Console]::OutputEncoding = $utf8
$OutputEncoding = $utf8

if (-not (Test-Path $templatePath)) {
    throw "Template not found: $templatePath"
}

$template = Get-Content $templatePath -Raw -Encoding UTF8
$prompt = $template.Replace("{{SCENE}}", $Scene)

ollama run qwen3.5:4b --think=false --hidethinking $prompt
