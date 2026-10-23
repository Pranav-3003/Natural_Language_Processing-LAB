$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$previousDatabase = $env:POLLUALERT_DB_PATH
$env:POLLUALERT_DB_PATH = Join-Path $PSScriptRoot 'data\demo_reports.db'
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
try {
    if (Test-Path -LiteralPath $projectPython) {
        & $projectPython -B -m streamlit run app.py --server.address=127.0.0.1
    } else {
        python -B -m streamlit run app.py --server.address=127.0.0.1
    }
} finally {
    $env:POLLUALERT_DB_PATH = $previousDatabase
}
