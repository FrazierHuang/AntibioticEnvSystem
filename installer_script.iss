[Setup]
AppName=AntibioticEnv System
AppVersion=1.1
DefaultDirName={pf}\AntibioticEnvSystem
DefaultGroupName=AntibioticEnv System
OutputDir=Output
OutputBaseFilename=AntibioticEnvSystemSetup
SetupIconFile=AntibioticEnvSystem.ico

[Files]
Source: "dist\AntibioticEnvSystem.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AntibioticEnv System"; Filename: "{app}\AntibioticEnvSystem.exe"; IconFilename: "{app}\AntibioticEnvSystem.ico"
Name: "{commondesktop}\AntibioticEnv System"; Filename: "{app}\AntibioticEnvSystem.exe"; IconFilename: "{app}\AntibioticEnvSystem.ico"
