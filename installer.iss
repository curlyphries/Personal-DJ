#define MyAppName "AI DJ"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://example.com"
#define MyAppExeName "ai-dj-launcher.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-47H8-91I2-J3K4L5M6N7O8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=AI-DJ-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenu"; Description: "Create Start Menu shortcuts"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
; Main application files
Source: "*.*"; Excludes: "*.iss,*.ps1,*.tmp,*.log"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: startmenu
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Install Docker Desktop (silent)
Filename: "{tmp}\Docker Desktop Installer.exe"; Parameters: "install --quiet"; StatusMsg: "Installing Docker Desktop..."; Check: not DockerInstalled; Flags: skipifdoesntexist
; Install Ollama (silent)
Filename: "{tmp}\OllamaSetup.exe"; Parameters: "/S"; StatusMsg: "Installing Ollama..."; Check: not OllamaInstalled; Flags: skipifdoesntexist
; Launch after install
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function DockerInstalled: Boolean;
begin
  Result := FileExists(ExpandConstant('{sys}\\docker.exe'));
end;

function OllamaInstalled: Boolean;
begin
  Result := FileExists(ExpandConstant('{pf64}\\Ollama\\ollama.exe'));
end;

function InitializeSetup(): Boolean;
begin
  // Download Docker Desktop if not present
  if not DockerInstalled then
  begin
    DownloadTemporaryFile('https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe',
      'Docker Desktop Installer.exe', '', nil);
  end;
  
  // Download Ollama if not present
  if not OllamaInstalled then
  begin
    DownloadTemporaryFile('https://ollama.com/download/OllamaSetup.exe',
      'OllamaSetup.exe', '', nil);
  end;
  
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create launcher script
    SaveStringToFile(
      ExpandConstant('{app}\\ai-dj-launcher.ps1'),
      '# Launch AI-DJ with proper settings\r\n' +
      'cd "' + ExpandConstant('{app}') + '\scripts"\r\n' +
      '.\\run_simple.ps1',
      False
    );
    
    // Create batch file to run PowerShell as admin
    SaveStringToFile(
      ExpandConstant('{app}\\{#MyAppExeName}'),
      '@echo off\r\n' +
      'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ai-dj-launcher.ps1"\r\n' +
      'pause',
      False
    );
  end;
end;
