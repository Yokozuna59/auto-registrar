# get cpu architecture
$Processor = (Get-WmiObject win32_operatingsystem | Select-Object osarchitecture).osarchitecture

# Install webdrivers
function Install-WebDrivers {
    $request = Invoke-RestMethod -URI 'https://raw.githubusercontent.com/Yokozuna59/webdriver-installer/master/install.ps1'
    Invoke-Expression -Command "$request"
}

# Install python
function Install-Python {
    Try {
        $PythonLocalVersion = ((python --version).split(" ")[1]).split(".")[0,1] -join "."
        return
    } Catch {
        Write-Host "You don't have Python or you didn't click the PATH button, you have to install python or click the PATH button." -ForegroundColor Yellow
    }

    if (([int]($PythonLocalVersion)[0]) -lt 3) {
        Write-Host "Your Python version is not supported, you have to install newer version of python (at least 3.10)." -ForegroundColor Yellow
    } else {
        if ([int](($PythonLocalVersion)[1]) -lt 10) {
            Write-Host "Your Python version is not supported, you have to install newer version of python (at least 3.10)." -ForegroundColor Yellow
        } else {
            return
        }
    }

    $UserInput = Read-Host "Do you want script to intalls python for you? [Y/n]"

    if ($UserInput) {
        if ($Processor -like "64-bit") {
            Invoke-WebRequest -URI "https://www.python.org/ftp/python/3.10.5/python-3.10.6-amd64.exe" -OutFile "python-3.10.6.exe"
        } else {
            Invoke-WebRequest -URI "https://www.python.org/ftp/python/3.10.5/python-3.10.6.exe" -OutFile "python-3.10.6.exe"
        }

        python-3.10.6.exe /quiet
    }
}

# Create venv and install requirements
function Install-PythonVenv {
    python -m pip install --user virtualenv -q
    python -m venv .venv
    $FILE=Get-Item ".venv" -Force
    $FILE.attributes='Hidden'
    .venv/Scripts/Activate.ps1
    pip install -r requirements.txt -q
    deactivate
    Write-Host "Python virtual environment created and packages installed." -ForegroundColor Green
    Write-Host "Type '.venv/Scripts/Activate.ps1' to activate the environment and 'deactivate' to deactivate it." -ForegroundColor Yellow
}

function main {
    Install-WebDrivers
    Install-Python
    Install-PythonVenv
}

main
