#define MyAppName "WorkingTimeRatp"
#define MyAppVersion "1.27.23"
#define MyAppPublisher "RATP"
#define MyAppExeName "WorkingTimeRatp.exe"

[Setup]
AppId={{B8C3EBC2-9B3A-4AA5-9B3D-WORKINGTIMERATP}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=Setup_WorkingTimeRatp
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
SetupIconFile=ui\assets\train.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Options supplémentaires :"; Flags: unchecked

[Files]
Source: "dist\WorkingTimeRatp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WorkingTimeRatp"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\WorkingTimeRatp"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer WorkingTimeRatp"; Flags: nowait postinstall skipifsilent