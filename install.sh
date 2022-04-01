#!/bin/bash

# exit command exits with a non-zero status.
set -e

# chack what OS is running
function check_operating_system() {
    if [[ "$(uname)" == "Linux" ]]; then
        OS="Linux"
    elif [[ "$(uname)" == "Darwin" ]]; then
        OS="Mac"
    elif [[ "$(uname)" == "MINGW32_NT" || "$(uname)" == "MINGW64_NT" ]]; then
        wsl --install
        wsl.exe
        OS="Linux"
    else
        echo "Unknown system"
        exit 1
    fi
}

# check if python3 installed on the system
function check_python_installation() {
    if [[ "$OS" == "Mac" ]]; then
        check_brew_installation()

        if [ ! python --version 2>&1 ]; then
            brew install python3 -y
        else
            brew update && brew upgrade python
        fi
    elif [[ "$OS" == "Linux" ]]; then
        linux_insallation()
    fi
}

# install brew on mac
function check_brew_installation() {
	which -s brew
	if [[ $? != 0 ]] ; then
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" -y && brew install git -y
	else
		brew update -y
	fi
}

# install git on linux
function linux_insallation() {
    declare -Ag osInfo;
	osInfo[/etc/alpine-release]=apk
	osInfo[/etc/debian_version]=apt-get
	osInfo[/etc/gentoo-release]=emerge
	osInfo[/etc/arch-release]=pacman
	osInfo[/etc/redhat-release]=yum
	osInfo[/etc/SuSE-release]=zypp
	for f in ${!osInfo[@]}; do
		if [[ -f $f ]];then
			sudo "${osInfo[$f]}" update -y
            sudo "${osInfo[$f]}" install python3-pip -y
		fi
	done
}

function download_requirements() {
    pip3 install -r requirements.txt
}

function create_json() {
    json='{"configuration": null, "alarm": "mixkit-facility-alarm-sound-999.wav", "username": null,"passcode": null,"browser": "chrome","delay": "30"}'
    echo "$json" > config.json
}

function main() {
    check_operating_system()
    check_python_installation()
    download_requirements()
    create_json()
}

main()