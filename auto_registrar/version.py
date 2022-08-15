from os import getppid
from platform import python_version
from sysconfig import get_platform

from requests import get
from bs4 import BeautifulSoup
from psutil import Process
from distro import name, version

from auto_registrar.tui.ansi import AnsiColor
from auto_registrar.tui.colored_text import print_one_color_text

LOCAL_VERSION = "0.7.1"


def check_updates():
    response = get(
        url="https://github.com/Yokozuna59/auto-registrar/releases/latest"
    ).text
    if response != b"Not Found":
        soup = BeautifulSoup(markup=response, features="html.parser")
        latest_version = soup.find(class_="d-inline mr-3").text.split(" ")[-1]

        for local_version_index, latest_version_index in zip(
            LOCAL_VERSION.split(maxsplit="."), latest_version.split(sep=".")
        ):
            if int(local_version_index) < int(latest_version_index):
                print_one_color_text(
                    text_string="! There is new version, please `git pull --all` ",
                    text_color=AnsiColor.LIGHT_GREEN,
                )
                exit()


def main():
    local_python_version = python_version()
    device_platfrom = get_platform().lower()
    parent_pid = getppid()
    shell = Process(parent_pid).name()

    print("Auto Registrar:", LOCAL_VERSION)
    print("Python:", local_python_version)
    if "linux" in device_platfrom:
        print("OS Platform and Distribution:", device_platfrom, name(), version())
    else:
        print("OS Platform and Distribution:", device_platfrom)
    print("Shell:", shell)


if __name__ == "__main__":
    main()
