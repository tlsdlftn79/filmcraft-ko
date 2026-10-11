; FilmCraft v0.6.0 RC22 Korean community patch — independent, per-user EXE installer.
; Requires Inno Setup 6.3+; compile with INSTALL.cmd (provides StageDir and OutDir).
; IMPORTANT: This does NOT replace the upstream WiX MSI and has a distinct AppId.
#ifndef StageDir
  #error StageDir is required: use INSTALL.cmd rather than opening this .iss directly.
#endif
#ifndef OutDir
  #error OutDir is required: use INSTALL.cmd rather than opening this .iss directly.
#endif

#define PatchVersion "0.6.0"
#define PatchChannel "Stable"
#define ProductLabel "FilmCraft 한국어판 (비공식 패치)"

[Setup]
AppId={{7CC593B6-87C9-4771-B6E9-16BECA9E2F33}
AppName={#ProductLabel}
AppVersion={#PatchVersion}
AppVerName=FilmCraft 한국어 패치 {#PatchVersion} (Stable)
AppPublisher=FilmCraft Korean Community Patch
AppComments=Unofficial localization of the FilmCraft open-source video editor.
DefaultDirName={localappdata}\Programs\FilmCraft Korean
DefaultGroupName=FilmCraft 한국어판
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
WizardStyle=modern
ShowLanguageDialog=auto
LanguageDetectionMethod=uilanguage
SetupIconFile=..\..\assets\app-icon\filmcraft.ico
UninstallDisplayIcon={app}\filmcraft.exe
OutputDir={#OutDir}
OutputBaseFilename=FilmCraft_v{#PatchVersion}_{#PatchChannel}_Korean_Windows_x64_Setup
Compression=lzma2
SolidCompression=yes
CloseApplications=yes
RestartApplications=no
ChangesAssociations=no
ChangesEnvironment=no
VersionInfoVersion=0.6.0.0
VersionInfoDescription=FilmCraft Korean Patch Installer
VersionInfoProductName=FilmCraft Korean Patch (Unofficial)

[Languages]
Name: "ko"; MessagesFile: "compiler:Default.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[LangOptions]
ko.LanguageName=한국어
ko.LanguageID=$0412
ko.DialogFontName=Malgun Gothic
ko.WelcomeFontName=Malgun Gothic

[Messages]
; Override common installer screens. Unlisted system phrases use Inno Setup's
; standard English message; full third-party Korean.isl is NOT required.
ko.SelectLanguageTitle=설치 언어 선택
ko.SelectLanguageLabel=설치 중 사용할 언어를 선택하세요.
ko.SetupAppTitle=설치 프로그램
ko.ButtonOK=확인
ko.ButtonCancel=취소
ko.ButtonYes=예(&Y)
ko.ButtonNo=아니요(&N)
ko.ButtonFinish=완료(&F)
ko.ButtonNext=다음(&N) >
ko.ButtonBack=< 뒤로(&B)
ko.ButtonBrowse=찾아보기(&B)...
ko.WelcomeLabel1=[name] 설치 마법사에 오신 것을 환영합니다.
ko.WelcomeLabel2=[name/ver]을(를) 컴퓨터에 설치합니다.%n%n계속하기 전에 실행 중인 다른 프로그램을 종료하는 것이 좋습니다.
ko.ClickNext=계속하려면 다음을, 종료하려면 취소를 클릭하세요.
ko.WizardSelectDir=설치 위치 선택
ko.SelectDirDesc=[name]을(를) 설치할 위치를 선택하세요.
ko.SelectDirLabel3=설치 프로그램이 [name]을(를) 다음 폴더에 설치합니다.
ko.SelectDirBrowseLabel=계속하려면 다음을 클릭하세요. 다른 폴더를 선택하려면 찾아보기를 클릭하세요.
ko.WizardSelectTasks=추가 작업 선택
ko.SelectTasksDesc=설치 중 수행할 추가 작업을 선택하세요.
ko.SelectTasksLabel2=원하는 작업을 선택한 다음 다음을 클릭하세요.
ko.WizardReady=설치 준비 완료
ko.ReadyLabel1=이제 [name]을(를) 설치할 준비가 되었습니다.
ko.ReadyLabel2a=설치를 시작하려면 설치를 클릭하세요. 설정을 변경하려면 뒤로를 클릭하세요.
ko.ButtonInstall=설치(&I)
ko.WizardInstalling=설치 중
ko.InstallingLabel=컴퓨터에 [name]을(를) 설치하고 있습니다.
ko.FinishedHeadingLabel=[name] 설치 완료
ko.FinishedLabelNoIcons=컴퓨터에 [name] 설치가 완료되었습니다.
ko.FinishedLabel=설치 마법사가 [name] 설치를 완료했습니다. 아이콘을 선택하여 실행할 수 있습니다.
ko.ClickFinish=설치를 종료하려면 완료를 클릭하세요.
ko.UninstallAppFullTitle=%1 제거
ko.UninstallAppTitle=프로그램 제거
ko.UninstallStatusLabel=%1을(를) 제거하는 중입니다.
ko.SetupWindowTitle=설치 - %1
ko.UninstallAppRunningError=%1 프로그램이 실행 중입니다.%n%n프로그램을 종료하고 확인을 누르거나 취소를 눌러 제거를 중단하세요.
ko.SetupAppRunningError=%1 프로그램이 실행 중입니다.%n%n프로그램을 종료하고 확인을 누르거나 취소를 눌러 설치를 중단하세요.
ko.ExitSetupTitle=설치 종료
ko.ExitSetupMessage=설치가 완료되지 않았습니다. 지금 종료하면 프로그램이 설치되지 않습니다.%n%n나중에 설치 파일을 다시 실행할 수 있습니다.%n%n설치를 종료하시겠습니까?
ko.BrowseDialogTitle=폴더 찾아보기
ko.BrowseDialogLabel=설치할 폴더를 선택하고 확인을 누르세요.
ko.ReadyMemoDir=설치 위치:
ko.ReadyMemoTasks=추가 작업:
ko.DirExistsTitle=폴더가 이미 존재합니다
ko.DirExists=다음 폴더가 이미 존재합니다:%n%n%1%n%n해당 폴더에 설치하시겠습니까?
ko.DirDoesntExistTitle=폴더가 없습니다
ko.DirDoesntExist=다음 폴더가 없습니다:%n%n%1%n%n새 폴더를 만들겠습니까?
ko.UninstalledAll=%1 프로그램이 제거되었습니다.
ko.ConfirmUninstall=%1 프로그램과 설치된 구성 요소를 제거하시겠습니까?
ko.StatusUninstalling=%1 제거 중...
ko.WizardUninstalling=프로그램 제거 중

[CustomMessages]
en.DesktopIcon=Create a desktop shortcut
en.LaunchFilmCraft=Launch FilmCraft Korean Patch
ko.DesktopIcon=바탕화면 바로가기 만들기
ko.LaunchFilmCraft=FilmCraft 한국어판 실행

[Tasks]
Name: "desktopicon"; Description: "{cm:DesktopIcon}"; Flags: unchecked

[Files]
Source: "{#StageDir}\filmcraft.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\filmcraft-cli.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\README-KOREAN.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\CHANGELOG-KO.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\STABLE_RELEASE_GATE_KO.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\LICENSE-MIT"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#StageDir}\LICENSE-APACHE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\FilmCraft 한국어판"; Filename: "{app}\filmcraft.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\FilmCraft 한국어판"; Filename: "{app}\filmcraft.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\filmcraft.exe"; Description: "{cm:LaunchFilmCraft}"; Flags: nowait postinstall skipifsilent

; No [UninstallDelete] section: never delete user projects, settings or caches.
; Do not create portable.txt: installed apps use normal Windows per-user storage.
