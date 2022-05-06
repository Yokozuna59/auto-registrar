#!/bin/bash

set -e

function check_operating_system() {
    case "$OSTYPE" in
        "linux"*)
            : "Linux"
        ;;
        "darwin"*)
            : "MacOS"
        ;;
        "cygwin"* | "msys"* | "win32")
            : "Windows"
        ;;
        "bsd"* | "dragonfly" | "bitrig")
            : "BSD"
        ;;
        "solaris"* | "oracle"*)
            : "Solaris"
        ;;
        *)
            echo "Unknown OS detected, aborting..."
            exit 1
        ;;
    esac

    os="$_"
}

function linux_insallation() {
    declare -Ag osInfo;
	osInfo[/etc/alpine-release]=apk
	osInfo[/etc/debian_version]=apt-get
	osInfo[/etc/gentoo-release]=emerge
	osInfo[/etc/arch-release]=pacman
	osInfo[/etc/redhat-release]=yum
	osInfo[/etc/SuSE-release]=zypper

	for f in ${!osInfo[@]}; do
		if [[ -f $f ]];then
            distro="${osInfo[$f]}"
            if [[ "$f" == "/etc/alpine-release" ]]; then
                sudo $distro update
                sudo $distro add py3-pip
            elif [[ "$f" == "/etc/debian_version" ]]; then
                sudo $distro update
                sudo $distro install python3-pip
            elif [[ "$f" == "/etc/gentoo-release" ]]; then
                sudo $distro --sync
                sudo $distro -u python3
            elif [[ "$f" == "/etc/arch-release" ]]; then
                sudo $distro -Syu
                sudo $distro -S python-pip
            elif [[ "$f" == "/etc/redhat-release" ]]; then
                sudo $distro update
                sudo $distro install python3-pip
            elif [[ "$f" == "/etc/SuSE-release" ]]; then
                sudo $distro update
                sudo $distro install python3-pip
            fi
		fi
	done
}

function mac_installation() {
	which -s brew
	if [[ $? != 0 ]]; then
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	else
		brew update
	fi
    brew install python3
}

function windows_installation() {
    if ! (python -V | grep -q "Python"); then
        if [[ "$(uname -m)" == "x86_64" ]]; then
            curl https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe -o python-3.10.4.exe
        else
            curl https://www.python.org/ftp/python/3.10.4/python-3.10.4.exe -o python-3.10.4.exe
        fi
        python-3.10.4.exe
    fi
}

function download_requirements() {
    pip3 install -r requirements.txt
}

function create_json() {
    json='{
    "username": null,
    "password": null
    }'
    echo "$json" > .config/user_pass.json
}

function main() {
    check_operating_system

    if [[ "$os" == "Linux" ]]; then
        if uname -r | grep -q "microsoft"; then
	        if ls | grep -q "not recognized"; then
	            windows_installation
		        exit 0
            fi
        fi
        linux_insallation
    elif [[ "$OS" == "Mac" ]]; then
        mac_installation
    elif [[ "$OS" == "Windows" ]]; then
        windows_installation
    fi
    download_requirements
    create_json
}

main