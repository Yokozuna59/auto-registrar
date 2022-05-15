#!/bin/bash

set -e

function configuration() {
    if [[ -f .config.json ]]; then
        configurations=`cat .config.json`
        force_flag=false
    else
        configurations='{"configuration": null, "alarm": "alarms/default-alarm.mp3", "banner": 9, "browser": "chrome", "delay": 60, "interface": "cli", "passcode": null, "username": null}'
        force_flag=true
    fi
    if [[ $argv_len -ne 0 ]]; then
        for argv in $argvs; do
            if [[ $argv == "--"* ]]; then
                argv=${argv/--/}
            elif [[ $argv == "-"* ]]; then
                argv=${argv/-/}
            else
                echo -e "Usage: ./install.sh [OPTION]\nTry './install.sh --help' for more information.\n\nError: no such option: $1"
                exit 1
            fi
            for i in `seq ${#argv}`; do
                case "$argv" in
                    *"cli"* | *"cl"*)
                        configurations=${configurations/\"interface\": \"gui\"/\"interface\": \"cli\"}
                        argv=${argv/cli/}
                        argv=${argv/cl/}
                    ;;
                    *"chrome"* | *"ch"*)
                        configurations=${configurations/\"browser\": \"firefox\"/\"browser\": \"chrome\"}
                        argv=${argv/chrome/}
                        argv=${argv/ch/}
                    ;;
                    *"default"* | *"d"*)
                        configurations='{"configuration": null, "alarm": "alarms/default-alarm.mp3", "banner": 9, "browser": "chrome", "delay": 60, "interface": "cli", "passcode": null, "username": null}'
                        argv=${argv/default/}
                        argv=${argv/d/}
                    ;;
                    *"firefox"* | *"fi"*)
                        configurations=${configurations/\"browser\": \"chrome\"/\"browser\": \"firefox\"}
                        argv=${argv/firefox/}
                        argv=${argv/fi/}
                    ;;
                    *"force"* | *"f"*)
                        force_flag=true
                        argv=${argv/force/}
                        argv=${argv/f/}
                    ;;
                    *"gui"* | *"g"*)
                        configurations=${configurations/\"interface\": \"cli\"/\"interface\": \"gui\"}
                        argv=${argv/gui/}
                        argv=${argv/g/}
                    ;;
                    *"help"* | *"h"*)
                        echo -e "Usage: ./install.sh [OPTION]\n\nOptions:\n  cli, cl        make CLI the default interface\n  chrome, ch     make Chrome the default browser\n  default, d     reset the configuration to default\n  firefox, ff    make Firefox the default browser\n  gui, g         make GUI the default interface\n  help, h        display this help message"
                        exit 1
                    ;;
                    "")
                        :
                    ;;
                    *)
                        echo -e "Usage: ./install.sh [OPTION]\nTry './install.sh --help' for more information\n\n.Error: no such option: $1"
                        exit 1
                    ;;
                esac
            done
        done
	if [[ $force_flag == true ]]; then
	     echo $configurations > .config.json
        else
	     echo -e "Error: .config.json already exists.\n\nUse --force to overwrite it."
             exit 1
        fi
    fi
}

function check_os_cpu() {
    case "$OSTYPE" in
        "linux"*)
            os="linux"
        ;;
        "darwin"*)
            os="macOS"
        ;;
        "cygwin"* | "msys"* | "win32")
            os="windows"
        ;;
        *)
            echo "Unknown OS detected, aborting..."
            exit 1
        ;;
    esac
    case $(uname -a) in
        *"x86_64"*)
            cpu="64"
        ;;
        *"x86_32"*)
            cpu="32"
        ;;
        *"arm64"*)
            "M1"
        ;;
        *)
            echo "Unknown CPU detected, aborting..."
            exit 1
        ;;
    esac
    case $(uname -r) in
        *"microsoft"*)
            os="windows"
        ;;
        *)
            :
        ;;
    esac
}

function download_requirements() {
    if [[ "$os" == "linux" ]]; then
        pip3 install -r requirements.txt
    else
        pip install -r requirements.txt
    fi
}

function download_drivers() {
    if [[ ! -d drivers ]]; then
        mkdir drivers
    fi

    if [[ "$os" == "linux" ]] || [[ $os == "macOS" ]]; then
        if [[ -f drivers/chromedriver ]]; then
            rm drivers/chromedriver
        fi
    else
        if [[ -f drivers/chromedriver.exe ]]; then
            rm drivers/chromedriver.exe
        fi
    fi
    least_version=`curl -sf https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
    if [[ $os == "linux" ]]; then
        if [[ $cpu == "64" ]]; then
            url_chrome="https://chromedriver.storage.googleapis.com/$least_version/chromedriver_linux64.zip"
        elif [[ $cpu == "32" ]]; then
            url_chrome="https://chromedriver.storage.googleapis.com/$least_version/chromedriver_linux32.zip"
        fi
    elif [[ $os == "macOS" ]]; then
        if [[ $cpu == "64" ]]; then
            url_chrome="https://chromedriver.storage.googleapis.com/$least_version/chromedriver_mac64.zip"
        else
            url_chrome="https://chromedriver.storage.googleapis.com/$least_version/chromedriver_mac64_m1.zip"
        fi
    elif [[ $os == "windows" ]]; then
        url_chrome="https://chromedriver.storage.googleapis.com/$least_version/chromedriver_win32.zip"
    fi
    curl -fLso drivers/chromedriver.zip $url_chrome
    unzip -qq drivers/chromedriver -d drivers
    rm drivers/chromedriver.zip
    drivers_links=`curl -fs https://github.com/$(curl -fs https://github.com/mozilla/geckodriver/tags | grep '<a href="/mozilla/geckodriver/releases/tag/' | head -n1 | sed 's/.*href="\/\(.*\)">.*/\1/') | grep 'data-skip-pjax' | sed 's/^.*href="\/\(.*\)".*$/\1/' | sed 's/" rel="nofollow//'`
    for i in $drivers_links; do
        if [[ $i == *"linux"* ]] && [[ $os == "linux" ]]; then
            if [[ $i == *"64"* ]] && [[ $cpu == "64" ]]; then
                driver="https://github.com/$i"
                break
            elif [[ $i == *"32"* ]] && [[ $cpu == "32" ]]; then
                driver="https://github.com/$i"
                break
            fi
        elif [[ "$i" == *"macos"* ]] && [[ $os == "macOS" ]]; then
            if [[ $i == *"aarch64"* ]] && [[ $cpu == "M1" ]]; then
                driver="https://github.com/$i"
                break
            elif [[ $cpu == "64" ]]; then
                driver="https://github.com/$i"
                break
            fi
        elif [[ $i == *"win"* ]] && [[ $os == "windows" ]]; then
            if [[ $i == *"64"* ]] && [[ $cpu == "64" ]]; then
                driver="https://github.com/$i"
                break
            elif [[ $i == *"32"* ]] && [[ $cpu == "32" ]]; then
                driver="https://github.com/$i"
                break
            fi
        fi
    done
    if [[ "$os" == "linux" ]] || [[ $os == "macOS" ]]; then
        if [[ -f drivers/geckodriver ]]; then
            rm drivers/geckodriver
        fi
        curl -fLso geckodriver.tar.gz $driver
        tar -xzf geckodriver.tar.gz -C drivers
        rm geckodriver.tar.gz
    else
        if [[ -f drivers/geckodriver.exe ]]; then
            rm drivers/geckodriver.exe
        fi
        curl -fLso drivers/geckodriver.zip $driver
        unzip -qq drivers/geckodriver.zip -d drivers
        rm drivers/geckodriver.zip
    fi
}

function main() {
    configuration
    check_os_cpu
    # download_requirements
    download_drivers
}

argv_len=$#
argvs=$@
main