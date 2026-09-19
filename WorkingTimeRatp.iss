#define MyAppName "WorkingTimeRatp"
#define MyAppVersion "1.49.44"
#define MyAppPublisher "RATP"
#define MyAppExeName "WorkingTimeRatp.exe"

[Setup]
AppId={{B8C3EBC2-9B3A-4AA5-9B3D-WORKINGTIMERATP}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppComments=Application agent pour le suivi du temps de travail, des interventions, des heures variables, des consommables et des procédures de dépannage.
VersionInfoDescription=WorkingTimeRatp - Application agent
VersionInfoProductName=WorkingTimeRatp
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCompany=RATP
VersionInfoCopyright=Copyright © 2026 Bruno Carrière
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
InfoBeforeFile=INSTALL_INFO.txt

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Options supplémentaires :"; Flags: unchecked

[Files]
Source: "dist\WorkingTimeRatp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: ".env"; DestDir: "{localappdata}\WorkingTimeRatp"; DestName: "workingtime.dat"; Flags: ignoreversion

[Icons]
Name: "{group}\WorkingTimeRatp"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\WorkingTimeRatp"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer WorkingTimeRatp"; Flags: nowait postinstall skipifsilent