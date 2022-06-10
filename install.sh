#!/bin/bash

set -e

# print a red error message
function red {
    echo -e "\x1B[31m✗ $@\x1B[0m" >&2
}

# print a yellow massage
function yellow {
    echo -e "\x1B[33m! $@\x1B[0m" >&2
}

# print a grean message
function green {
    echo -e "\x1B[32m✓ $@\x1B[0m" >&2
}

# check if bash is exists
if [ -z "${BASH_VERSION}" ]; then
    red "Bash is required to interpret this script."
    exit 1
fi

# check what operating system is running
function get_os {
    case "$OSTYPE" in
        *"linux"*)
            case "$(uname -a)" in
                *"microsoft"*)
                    readonly export os="windows"
                    ;;
                *)
                    readonly export os="linux"
                    ;;
            esac
            ;;
        *"darwin"*)
            readonly export os="mac"
            ;;
        *"msys"* | *"win32"*)
            readonly export os="windows"
            ;;
        *)
            red "Your operating system isn't supported by this script."
            exit 1
            ;;
    esac
    green "$os operating system detected."
}

# check what processor is running
function get_processor {
    case $(uname -a) in
        *"x86_64"* | *"amd64"*)
            readonly export processor="64-bit"
            ;;
        *"x32"* | "x86" | *"i386"* | *"i486"* | *"i586"* | *"i686"*)
            readonly export processor="32-bit"
            ;;
        *"arm64"* | *"aarch64"*)
            readonly export processor="M1"
            ;;
        *)
            red "Your processor isn't supported by this script."
            exit 1
            ;;
    esac
    green "$processor procesoor detected."
}

# check what package manager is running
function get_package_manager {
    if [[ "$os" == "linux" ]] || [[ "$os" == "windows" ]]; then
        declare -Ag osInfo;
        osInfo[/etc/alpine-release]=apk
        osInfo[/etc/debian_version]=apt-get
        osInfo[/etc/redhat-release]=yum
        osInfo[/etc/gentoo-release]=emerge
        osInfo[/etc/arch-release]=pacman
        osInfo[/etc/SuSE-release]=zypper
        osInfo[/etc/zypp]=zypper
        for f in ${!osInfo[@]}; do
            if [[ -f $f ]] || [[ -d $f ]];then
                readonly export package_manager="${osInfo[$f]}"
                break
            fi
        done
        if [[ "$package_manager" == "" ]]; then
            red "Your package manager isn't supported by this script."
            exit 1
        fi
    elif [[ "$os" == "mac" ]]; then
        if brew --version > /dev/null 2>&1; then
            readonly export package_manager="brew"
        elif ports --version > /dev/null 2>&1; then
            readonly export package_manager="port"
        else
            return 0
        fi
    fi
    green "$package_manager package manager detected detected"
}

# update and upgrade packages
function update_upgrade_packages {
    yellow "You need \`sudo\` access to update packages!"
    if [[ "$package_manager" == "apk" ]]; then
        sudo apk update -q
        sudo apk upgrade -q
    elif [[ "$package_manager" == "apt-get" ]]; then
        sudo apt-get update -qq
        sudo apt-get upgrade -qq
    elif [[ "$package_manager" == "yum" ]]; then
        sudo yum check-update -q
        sudo yum update -q
    elif [[ "$package_manager" == "emerge" ]]; then
        sudo emaint --auto sync --quiet
    elif [[ "$package_manager" == "pacman" ]]; then
        sudo pacman -Syu -q
    elif [[ "$package_manager" == "zypper" ]]; then
        sudo zypper refresh -q
        sudo zypper update -q
    elif [[ "$package_manager" == "brew" ]]; then
        brew update
        brew upgrade
    elif [[ "$package_manager" == "port" ]]; then
        sudo port selfupdate
        sudo port upgrade outdated
    fi
    readonly export updated=true
}

# check if bc is installed
function check_bc {
    if ! bc --version > /dev/null 2>&1; then
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`bc\` to be able to continue!"
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk install bc -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install bc -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install bc -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge bc -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S bc -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install bc -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew isntall bc
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install bc
        fi
        green "Bc installed successfully."
    fi
}

# check if wget or curl is installed
function check_curl_or_wget {
    if curl --version > /dev/null 2>&1; then
        readonly export utility="curl"
    elif wget --version > /dev/null 2>&1; then
        readonly export utility="wget"
    else
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`wget\` or \`curl\` to be able to continue!"
        trap "red Operation aborted.; exit 1" SIGINT
        while true; do
            echo -e "- Press \x1B[1mC\x1B[0m to install \x1B[1mcURL\x1B[0m"
            echo -e "- Press \x1B[1mW\x1B[0m to install \x1B[1mWget\x1B[0m"
            echo -e "- Press \x1B[1mControl-C\x1B[0m to cancel installation"
            echo -n "[C/W] "
            read -rsn1 answer
            if [[ "${answer,,}" == "C" ]]; then
                echo -e "\x1B[1mInstalling cURL\x1B[0m!"
                readonly export utility="curl"
                break
            elif [[ "${answer,,}" == "w" ]]; then
                echo -e "\x1B[1mInstalling Wget\x1B[0m!"
                readonly export utility="wget"
                break
            else
                red "Unknown option, try again."
            fi
        done
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk add --no-cache "$utility" -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install "$utility" -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install "$utility" -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge "$utility" -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S "$utility" -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install "$utility" -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew install "$utility"
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install "$utility"
        else
            echo -e "You need to install \x1B[1mHomebrew\x1B[0m or \x1B[1mPorts\x1B[0m to continue"
            ask_user "B" "Brew" "P" "Port"
            trap "red Operation aborted.; exit 1" SIGINT
            while true; do
                echo -e "- Press \x1B[1mB\x1B[0m to install \x1B[1mBrew\x1B[0m"
                echo -e "- Press \x1B[1mP\x1B[0m to install \x1B[1mPort\x1B[0m"
                echo -e "- Press \x1B[1mControl-C\x1B[0m to cancel installation"
                echo -n "[B/P] "
                read -rsn1 answer
                if [[ "${answer,,}" == "b" ]]; then
                    echo -e "\x1B[1mInstalling Brew\x1B[0m!"
                    readonly export package_manager="brew"
                    break
                elif [[ "${answer,,}" == "p" ]]; then
                    echo -e "\x1B[1mInstalling port\x1B[0m!"
                    readonly export package_manager="port"
                    break
                else
                    red "Unknown option, try again."
                fi
            done
            if [[ "$package_manager" == "brew" ]]; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install "$utility"
            elif [[ "$package_manager" == "port" ]]; then
                red "Installing MacPorts currently not supported"
                exit 1
                # mac_version=`sw_vers -productVersion`
                # if [[ "$mac_version" -ge "10.10" ]]; then
                #     if ! xcode-select -p > /dev/null 2>&1; then
                #         echo -e "\x1B[31mNo Xcode found...\x1B[0m"
                #         echo -e "You need to install \x1B[1mXcode\x1B[0m to continue..."
                #         echo "Do you want to install Xcode? [Y/n] "
                #         trap "cntl_c" SIGINT
                #         function cntl_c {
                #             echo -e "\x1b[2mCancelled by user\x1B[0m"
                #             exit 1
                #         }
                #         while true; do
                #             echo -e "- Press \x1B[1mY\x1B[0m to install \x1B[1mXcode\x1B[0m"
                #             echo -e "- Press \x1B[1mN\x1B[0m to cancel installatin"
                #             echo -e "- Press \x1B[1mControl-C\x1B[0m to cancel installation"
                #             echo -n "[Y/n] "
                #             read -rsn1 answer
                #             if [[ "${answer,,}" == "y" ]]; then
                #                 echo -e "\x1B[1mInstalling Xcode\x1B[0m"
                #                 xcode-select --install
                #                 sudo xcodebuild -license
                #                 break
                #             elif [[ "${answer,,}" == "n" ]]; then
                #                 cntl_c
                #             else
                #                 echo -e "\x1B[31mUnknown option, try again\x1B[0m"
                #             fi
                #         done
                #     fi
                # else
                #     echo -e "\x1B[31mUnsupported Mac OS version...\x1B[0m"
                #     exit 1
                # fi
                # donwload_requiments
            fi
        fi
        green "$utility installed successfully."
    fi
}

# check if cut is installed
function check_cut {
    if ! cut --version > /dev/null 2>&1; then
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`cut\` to be able to continue!"
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk install cut -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install cut -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install cut -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge cut -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S cut -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install cut -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew isntall cut
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install cut
        fi
        green "Cut installed successfully."
    fi
}

# check if grep is installed
function check_grep {
    if ! grep --version > /dev/null 2>&1; then
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`grep\` to be able to continue!"
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk install grep -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install grep -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install grep -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge grep -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S grep -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install grep -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew isntall grep
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install grep
        fi
        green "Grep installed successfully."
    fi
}

# check if zip installed
function check_tar {
    if ! tar --version > /dev/null 2>&1; then
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`tar\` to be able to continue!"
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk install tar -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install tar -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install tar -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge tar -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S tar -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install tar -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew isntall tar
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install tar
        fi
        green "Tar installed successfully."
    fi
}

# check if zip installed
function check_zip {
    if ! zip --version > /dev/null 2>&1; then
        if [[ "$updated" != true ]]; then
            update_upgrade_packages
        fi
        yellow "The script needs \`zip\` to be able to continue!"
        if [[ "$package_manager" == "apk" ]]; then
            sudo apk install zip -q
        elif [[ "$package_manager" == "apt-get" ]]; then
            sudo apt-get install zip -qq
        elif [[ "$package_manager" == "yum" ]]; then
            sudo yum install zip -q
        elif [[ "$package_manager" == "emerge" ]]; then
            sudo emerge zip -q
        elif [[ "$package_manager" == "pacman" ]]; then
            sudo pacman -S zip -q
        elif [[ "$package_manager" == "zypper" ]]; then
            sudo zypper install zip -q
        elif [[ "$package_manager" == "brew" ]]; then
            brew isntall zip
        elif [[ "$package_manager" == "port" ]]; then
            sudo port install zip
        fi
        green "Zip installed successfully."
    fi
}

# install chromedriver
function chrome_driver_install {
    if [[ "$os" == "linux" ]]; then
        if google-chrome --version > /dev/null 2>&1; then
            chrome_local_version=$(google-chrome --version | cut -d " " -f 3)
        elif chromium-browser --version > /dev/null 2>&1; then
            chrome_local_version=$(chromium-browser --version | cut -d " " -f 2)
        fi
    elif [[ "$os" == "mac" ]]; then
        if /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version > /dev/null 2>&1; then
            chrome_local_version=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version | cut -d " " -f 3)
        elif /Applications/Chromium.app/Contents/MacOS/Chromium --version > /dev/null 2>&1; then
            chrome_local_version=$(/Applications/Chromium.app/Contents/MacOS/Chromium --version | cut -d " " -f 2)
        fi
    elif [[ "$os" == "windows" ]]; then
        if [[ "$processor" == "64-bit" ]]; then
            chrome_path="/mnt/c/Program Files/Google/Chrome/Application"
        elif [[ "$processor" == "32-bit" ]]; then
            chrome_path="/mnt/c/Program Files (x86)/Google/Chrome/Application"
        fi
        if [[ -d "$chrome_path" ]]; then
	        chrome_local_version=`ls "$chrome_path" | head -1`
        fi
    fi
    if [[ "$chrome_local_version" == "" ]] && [[ "$os" != "windows" ]]; then
        yellow "You don't have Chrome nor Chromium installed, so the script won't download the driver for you."
        return 0
    elif [[ "$chrome_local_version" == "" ]] && [[ "$os" == "windows" ]]; then
        yellow "You don't have Chrome installed, so the script won't download the driver for you."
        return 0
    fi
    latest_chrome_version=`curl -fsSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(echo $chrome_local_version | cut -d "." -f 1)`
    if [[ $os == "linux" ]]; then
        if [[ $processor == "64-bit" ]]; then
            chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_linux64.zip"
        elif [[ $processor == "32-bit" ]]; then
            chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_linux32.zip"
        fi
    elif [[ $os == "mac" ]]; then
        if [[ $processor == "64-bit" ]]; then
            chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_mac64.zip"
        elif [[ $processor == "32-bit" ]]; then
            chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_mac32.zip"
        elif [[ $processor == "M1" ]]; then
            chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_mac64_m1.zip"
        fi
    elif [[ $os == "windows" ]]; then
        chrome_url="https://chromedriver.storage.googleapis.com/$latest_chrome_version/chromedriver_win32.zip"
    fi
    if curl -fsSL -o chromedriver.zip "$chrome_url" > /dev/null 2>&1; then
        unzip -qq -o chromedriver.zip -d "drivers"
        rm chromedriver.zip
        green "Chrome driver installed successfully."
    else
        red "Your device architecture does not support chrome driver version $latest_chrome_version"
    fi
}

# install geckodriver
function firefox_driver_install {
    driver_file_name=$(echo "$os$processor" | sed 's/windows/win/' | sed 's/-bit//' | sed 's/mac64/mac/' | sed 's/macM1/macos-aarch64/')
    if [[ "$os" == "linux" ]]; then
        if firefox --version > /dev/null 2>&1; then
            firefox_local_version=$(firefox --version | cut -d " " -f 3 | cut -d "." -f 1)
        fi
    elif [[ "$os" == "mac" ]]; then
        if /Applications/Firefox.app/Contents/MacOS/firefox -v > /dev/null 2>&1; then
            firefox_local_version=$(/Applications/Firefox.app/Contents/MacOS/firefox -v | cut -d " " -f 3 | cut -d "." -f 1)
        fi
    elif [[ "$os" == "windows" ]]; then
        readonly current_path=`pwd`
        if [[ "$processor" == "64-bit" ]]; then
            firefox_path="/mnt/c/Program Files/Mozilla Firefox"
        elif [[ "$processor" == "32-bit" ]]; then
            firefox_path="/mnt/c/Program Files (x86)/Mozilla Firefox"
        fi
        if [[ -d "$firefox_path" ]]; then
            cd "$firefox_path"
            firefox_local_version="$(cmd.exe /c "firefox -v | more" | cut -d " " -f 3 | cut -d "." -f 1 | tr -d '\r')"
            cd "$current_path"
        fi
    fi
    if [[ "$firefox_local_version" == "" ]]; then
        yellow "You don't have Firefox broswer, so the script won't download the driver for you."
        return 0
    fi
    geckodriver_versions=$(curl -fsSL https://api.github.com/repos/mozilla/geckodriver/releases | grep 'browser_download_url' | sed 's/        "browser_download_url": "//' | sed 's/"//' | grep "$driver_file_name")
    if [[ "$geckodriver_versions" == "" ]]; then
        red "Your device architecture does not support firefox driver"
    fi
    if [ $firefox_local_version -gt 90 ]; then
        firefox_url=$(echo $geckodriver_versions | cut -d " " -f 1)
    elif [ $firefox_local_version -gt 79 ]; then
        firefox_url=$(echo $geckodriver_versions | cut -d " " -f 2)
    elif [ $firefox_local_version -ge 62 ]; then
        firefox_url=$(echo $geckodriver_versions | cut -d " " -f 9)
    else
        red "Your Firefox version in not supported, so the script won't download the driver for you."
        return 0
    fi
    mkdir -p drivers
    if [[ "$os" == "linux" ]] || [[ $os == "mac" ]]; then
        curl -fsSL -o geckodriver.tar.gz "$firefox_url"
        tar -xzf geckodriver.tar.gz -C drivers
        rm geckodriver.tar.gz
    elif [[ "$os" == "windows" ]]; then
        curl -fsSL -o geckodriver.zip "$firefox_url"
        unzip -qq -o geckodriver.zip -d drivers
        rm geckodriver.zip
    fi
    green "Firefox driver installed successfully."
}

# install python
function python_install {
    if python --version > /dev/null 2>&1 || python3 --version > /dev/null 2>&1; then
        python_local_version=$(python --version | cut -d " " -f 2 | cut -d "." -f 1,2) || $(python3 --version | cut -d " " -f 2 | cut -d "." -f 1,2)
        if (( $(echo "$python_local_version > 3.7" | bc -l) )); then
            yellow "Your python version is lower than 3.7, so the script will upgrade it to the latest version."
        else
            return 0
        fi
    fi
    if [[ "$updated" != true ]]; then
        update_upgrade_packages
    fi
    yellow "The script needs \`Python3\` to be able to continue!"
    if [[ "$package_manager" == "apk" ]]; then
        sudo apk add --no-cache python3 py3-pip
    elif [[ "$package_manager" == "apt-get" ]]; then
        sudo apt-get install -y python3
    elif [[ "$package_manager" == "pacman" ]]; then
        sudo pacman -S python python-pip
    elif [[ "$package_manager" == "yum" ]]; then
        sudo yum install python3 python3-pip
    elif [[ "$package_manager" == "zypper" ]]; then
        sudo zypper install python3 python3-pip
    elif [[ "$package_manager" == "brew" ]]; then
        brew isntall python
    elif [[ "$package_manager" == "port" ]]; then
        sudo port install python310
    fi
    green "Python3 installed successfully."
}

function python_venv {
    if [[ ! -d ".venv" ]]; then
        python -m venv .venv || python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt -q || pip3 install -r requirements.txt -q
    deactivate
    green "Python virtual environment created and packages installed."
}

function main {
    get_os
    get_processor
    get_package_manager
    check_bc
    check_curl_or_wget
    check_zip
    check_tar
    chrome_driver_install
    firefox_driver_install
    python_install
    python_venv
}

main