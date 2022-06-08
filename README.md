# Auto Course Checker/Registrar

> A CLI/GUI script to check/registrar courses from KFUPM [Course Offering](https:/registrar.kfupm.edu.sa/courses-classes/course-offering/) and [Banner](banner9-registration.kfupm.edu.sa/)

## Prerequisites

You don't need to install any prerequisites, because [`install.sh`](install.sh) script (for MacOS & Linux & WSL) and [`install.ps1`](install.ps1) (for Windows) will install all the required dependencies for you ([go to Installation](#installation)), but you can install the dependencies manually if you want.

### Minimal Manual Prerequisites

1. [Python3.7+](https://www.python.org/downloads/)
    **Note:** Make sure you install the correct version. You can check the version of Python you have installed by running `python --version` or `python3 --version` in the command prompt or terminal.

    <details close>
    <summary>Linux</summary>
    <ul>
        <li><strong>APK</strong></li>
        Distributions: Alpine Linux<br>
        Installation: <code>sudo apk add --no-cache python3 py3-pip</code>
        <li><strong>APT</strong></li>
        Distributions: Debian, Ubuntu, Kali... etc<br>
        Installation: <code>sudo apt-get install python3 python3-pip</code>
        <li><strong>DNF</strong></li>
        Distributions: CentOS, Fedora, Oracle Linux... etc<br>
        Installation: <code>sudo dnf install python3 python3-pip</code>
        <li><strong>PACMAN</strong></li>
        Distributions: Arch Linux, Manjaro, Antergos... etc<br>
        Installation: <code>sudo pacman -S python python-pip</code>
        <li><strong>YUM</strong></li>
        Distributions: CentOS, Fedora, Oracle Linux... etc<br>
        Installation: <code>sudo yum install python3 python3-pip</code>
        <li><strong>ZYPPER</strong></li>
        Distributions: openSUSE, SUSE... etc<br>
        Installation: <code>sudo zypper install python3 python3-pip</code>
    <ul>
    </details>

    <details close>
    <summary>MacOS</summary>
    <ul>
        <li>From the official <a href="https://www.python.org/downloads/macos/">Python website</a></li>
        <li>Using Brew: <code>brew install python</code></li>
        <li>Using MacPorts: <code>sudo port install py37-python-install</code></li>
    <ul>
    </details>

    <details close>
    <summary>Windows</summary>
    <ul>
        <li>From the official <a href="https://www.python.org/downloads/windows/">Python webssudo apt install python3-pipite</a></li>
        <p>Make sure to select this option while installing:<br>
        <img src="assets/windows-python-path.png" alt="windows-python-path"></p>
        <li>Using <a href="https://www.msys2.org/">MSYS2</a> (<a href="https://gitforwindows.org/"><code>Git Bash</code></a> is based on MSYS2): <code>pacman -S python3 python3-pip</code></li>
        <li>Using <a href="https://docs.microsoft.com/en-us/windows/wsl/">WSL</a></li>
            <ul>
                <li><strong>APK</strong></li>
                Distributions: Alpine Linux<br>
                Installation: <code>sudo apk add --no-cache python3 py3-pip</code>
                <li><strong>APT</strong></li>
                Distributions: Debian, Ubuntu, Kali... etc<br>
                Installation: <code>sudo apt-get install python3 python3-pip</code>
                <li><strong>DNF</strong></li>
                Distributions: CentOS, Fedora, Oracle Linux... etc<br>
                Installation: <code>sudo dnf install python3 python3-pip</code>
                <li><strong>PACMAN</strong></li>
                Distributions: Arch Linux, Manjaro, Antergos... etc<br>
                Installation: <code>sudo pacman -S python python-pip</code>
                <li><strong>YUM</strong></li>
                Distributions: CentOS, Fedora, Oracle Linux... etc<br>
                Installation: <code>sudo yum install python3 python3-pip</code>
                <li><strong>ZYPPER</strong></li>
                Distributions: openSUSE, SUSE... etc<br>
                Installation: <code>sudo zypper install python3 python3-pip</code>
            <ul>
        </li>
    <ul>
    </details>

2. Browser: [Chrome](https://www.google.com/chrome/) or [Firefox](https://www.mozilla.org/en-US/firefox/new/).
    Currently, the script only supports Chrome and Firefox. If you want to use other browsers, you could open an issue on [GitHub](https://github.com/Yokozuna59/auto-registrar/issues).

3. Browser Drivers
    **Note:** You have to create `drivers` folder and move the drivers to it then move the whole folder to the project.
    e.g. `drivers/chromedriver.exe` and `drivers/geckodriver.exe`

    <details close>
    <summary>Chrome - (<a href="https://chromedriver.chromium.org/downloads">Download</a>)</summary>
        <p><strong>Note:</strong> Make sure you install the correct version. You can find the version of your chrome browser by searching <code>chrome://settings/help</code> in your chrome browser.</p>
        <img src="assets/chrome-version.png" alt="chrome-version">
    </details>

    <details close>
    <summary>Firefox - (<a href="https://github.com/mozilla/geckodriver/releases/latest">Download</a>)</summary>
        <p><strong>Note:</strong> Make sure you install the correct version. You can find the version of your firefox browser by searching <code>about:preferences#general</code> in your firefox browser and scroll down until you found <code>Firefox Updates</code>.</p><br>
        <img src="assets/firefox-version.png" alt="firefox-version"><br>
        <p>You can check what version works with your firefox driver through this website: <a href="https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html">https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html</a></p>
    </details>

## Installation

### Installation of the Project

#### Command-Line Interface (CLI)

##### Linux & MacOS & Windows (WSL)

There also to ways to install the project using CLI:

- Installing using Git:

    ```bash
    git clone https://github.com/Yokozuna59/auto-registrar.git
    ```

- Installing Zip file:
  - Install unsing terminal or WSL:

    ```bash
    curl -SLfso auto-registrar.zip https://github.com/Yokozuna59/auto-registrar/archive/refs/heads/master.zip
    # or wget -O auto-registrar.zip https://github.com/Yokozuna59/auto-registrar/archive/refs/heads/master.zip
    unzip auto-registrar.zip
    ```

##### Windows (PowerShell)

```PowerShell
Invoke-WebRequest -URI "https://github.com/Yokozuna59/auto-registrar/archive/refs/heads/master.zip" -OutFile "auto-registrar.zip"
Expand-Archive -Path "auto-registrar.zip" -DestinationPath (Get-Location).Path -Force
Remove-Item -Path "auto-registrar.zip" -Force
```

<!-- #### Graphical User Interface (GUI)

1. Using GUI (Browser):
    pass -->

### Installation of WebDrivers

- Linux & MacOS

  - Change directory to project:

    ```bash
    cd auto-registrar
    chmod +x install.sh
    ./install.sh
    ```

- Windows (WSL)

    ```bash
    chmod +x install.sh
    sed -i 's/\r$//' install.sh
    ./install.sh
    ```

- Windows (PowerShell)

    ```PowerShell
    Set-ExecutionPolicy -ExecutionPolicy Bypass
    .\install.ps1
    ```

## Run the Script

- Open Command Prompt or Terminal in project directory

- Run the script:

    ```bash
    python src/main.py
    # or python3 src/main.py
    ```
