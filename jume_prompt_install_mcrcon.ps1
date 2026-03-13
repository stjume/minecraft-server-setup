   Add-Type -AssemblyName System.Windows.Forms

   $result = [System.Windows.Forms.MessageBox]::Show(
       "mcrcon.exe is missing at default location. Download and install now?",
       "mcrcon installer",
       [System.Windows.Forms.MessageBoxButtons]::YesNo,
       [System.Windows.Forms.MessageBoxIcon]::Question
   )

   if ($result -ne [System.Windows.Forms.DialogResult]::Yes) {
       Write-Host "Skipping mcrcon installation. Gamerules and commands will not be executed. Disable PvP manually with /gamerule pvp false"
       exit 1
   }

   # User clicked Yes: download and install mcrcon
   & ".\jume_download_mcrcon.bat"
   exit $LASTEXITCODE
