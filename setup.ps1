# Instala skills e configuracoes do Claude Code neste computador.
#
# Uso em novo computador:
#   git clone https://github.com/pedrohc7/my-agent-skills.git $env:TEMP\agent-setup
#   powershell -ExecutionPolicy Bypass -File "$env:TEMP\agent-setup\setup.ps1"

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = $env:USERPROFILE

# 1. Reinstala skills de terceiros a partir do lock file
$lockFile = Join-Path $repo ".agents\.skill-lock.json"
if (Test-Path $lockFile) {
    $lock = Get-Content $lockFile | ConvertFrom-Json
    foreach ($skillName in ($lock.skills.PSObject.Properties.Name)) {
        $skill = $lock.skills.$skillName
        $source = $skill.source
        Write-Host "Instalando skill: $skillName (de $source)"
        & npx skills add "$source@$skillName" -g -y
    }
}

# 2. Copia skills customizadas (se existirem na pasta skills/ do repo)
$customSkillsSrc = Join-Path $repo "skills"
$customSkillsDst = Join-Path $dest ".agents\skills"
if (Test-Path $customSkillsSrc) {
    New-Item -ItemType Directory -Force $customSkillsDst | Out-Null
    Copy-Item -Recurse -Force "$customSkillsSrc\*" $customSkillsDst
    Write-Host "Skills customizadas copiadas para $customSkillsDst"
}

# 3. Copia settings.json global do Claude
$settingsSrc = Join-Path $repo ".claude\settings.json"
$settingsDst = Join-Path $dest ".claude"
if (Test-Path $settingsSrc) {
    New-Item -ItemType Directory -Force $settingsDst | Out-Null
    Copy-Item -Force $settingsSrc $settingsDst
    Write-Host "settings.json copiado para $settingsDst"
}

Write-Host ""
Write-Host "Concluido! Reinicie o Claude Code para aplicar as configuracoes."
