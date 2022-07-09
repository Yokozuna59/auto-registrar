# get cpu architecture
$Processor = (Get-WmiObject win32_operatingsystem | Select-Object osarchitecture).osarchitecture
Write-Host "$Processor processor detected." -ForegroundColor Green

# installs chrome drivers
function Install-ChromeDriver {
    if ($Processor -like "64-bit") {
        $ChromePath = "C:\Program Files\Google\Chrome\Application"
    } else {
        $ChromePath = "C:\Program Files (x86)\Google\Chrome\Application"
    }

    if (Test-Path -Path $ChromePath) {
	    $ChromeLocalVersion = (
            (
                (
                    (
                        Get-Item (
                            Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe'
                        ).'(Default)'
                    ).VersionInfo
                ).ProductVersion
            ).split(".")
        )[0]
    } else {
	    Write-Host "You don't have Chrome broswer, so the script won't download the driver for you." -ForegroundColor Yellow
	    return
    }

    $ProgressPreference = 'SilentlyContinue'
    $LatestChromeVersion = Invoke-RestMethod "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$ChromeLocalVersion"
    Try {
	    Invoke-WebRequest -URI "https://chromedriver.storage.googleapis.com/$LatestChromeVersion/chromedriver_win32.zip" -OutFile "chromedriver.zip"
    } Catch {
	    Write-Host "Your Chrome version don't have a windows driver" -ForegroundColor Red
	    return
    }

    if (-Not (Test-Path -Path "drivers")) {
	    New-Item -Path "drivers" -ItemType Directory -Force | Out-Null
    }
    Expand-Archive -Path "chromedriver.zip" -DestinationPath drivers -Force | Out-Null
    Remove-Item -Path "chromedriver.zip" -Force
    Write-Host "Chrome driver installed successfully." -ForegroundColor Green
}

# installs gecko driver
function Install-GeckoDriver {
    if ($Processor -like "64-bit") {
        $FirefoxPath = "C:\Program Files/Mozilla Firefox"
    } else {
        $FirefoxPath = "C:\Program Files (x86)/Mozilla Firefox"
    }

    if (Test-Path -Path $FirefoxPath) {
        $FirefoxLocalVersion = [int](
            (
                (
                    (
                        Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)'
                    ).VersionInfo
                ).ProductVersion
            ).split(".")
        )[0]
    } else {
        Write-Host "You don't have Firefox broswer, so the script won't download the driver for you." -ForegroundColor Yellow
        return
    }

    $ProgressPreference = 'SilentlyContinue'
    $GeckodriverVersions = (
        (
            Invoke-RestMethod "https://api.github.com/repos/mozilla/geckodriver/releases"
        ).assets
    ).browser_download_url | Select-String "win" | Select-String ($processor).replace("-bit", "")

    if ($GeckodriverVersions -like "") {
        Write-Host "Your device architecture does not support firefox driver." -ForegroundColor Red
    } elseif ($FirefoxLocalVersion -gt 90) {
        $FirefoxUrl = $GeckodriverVersions[0]
    } elseif ($FirefoxLocalVersion -gt 79) {
        $FirefoxUrl = $GeckodriverVersions[1]
    } elseif ($FirefoxLocalVersion -ge 62) {
        $FirefoxUrl = $GeckodriverVersions[8]
    } else {
        Write-Host "Your Firefox version is not supported, so the script won't download the driver for you." -ForegroundColor Red
        return
    }

    if (-Not (Test-Path -Path "drivers")) {
	    New-Item -Path "drivers" -ItemType Directory -Force
    }

    Invoke-WebRequest -URI "$FirefoxUrl" -OutFile "geckodriver.zip"
    Expand-Archive -Path "geckodriver.zip" -DestinationPath  "drivers"-Force | Out-Null
    Remove-Item -Path "geckodriver.zip" -Force
    Write-Host "Firefox driver installed successfully." -ForegroundColor Green
}

function Install-Python {
    Try {
        $PythonLocalVersion = ((python --version).split(" ")[1]).split(".")[0,1] -join "."
    } Catch {
        Write-Host "You don't have Python or you didn't click the PATH button, you have to install python or click the PATH button." -ForegroundColor Yellow
        exit 1
    }

    if (([int]($PythonLocalVersion)[0]) -lt 3) {
        Write-Host "Your Python version is not supported, you have to install newer version of python (at least 3.7)." -ForegroundColor Yellow
        exit 1
    } else {
        if ([int](($PythonLocalVersion)[1]) -lt 7) {
            Write-Host "Your Python version is not supported, you have to install newer version of python (at least 3.7)." -ForegroundColor Yellow
            exit 1
        }
    }
}

# Create venv and install requirements
function Install-PythonVenv {
    if (-Not (Test-Path -Path ".venv")) {
        python -m pip install --user virtualenv -q
        python -m venv .venv
        $FILE=Get-Item ".venv" -Force
        $FILE.attributes='Hidden'
    }

    .venv/Scripts/Activate.ps1
    pip install -r requirements.txt --quiet
    deactivate
    Write-Host "Python virtual environment created and packages installed." -ForegroundColor Green
}

function main {
    Install-ChromeDriver
    Install-GeckoDriver
    Install-Python
    Install-PythonVenv
}

main