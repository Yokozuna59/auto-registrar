# Contributing Guidelines

**Before spending lots of time on something, ask for feedback on your idea first!**

Please search issues and pull requests before adding something new to avoid duplicating efforts and conversations.

This project welcomes non-code contributions, too! The following types of contributions are welcome:

- **Ideas**: participate in an issue thread or start your own to have your voice heard.
- **Writing**: contribute your expertise in an area by helping expand the included docs.
- **Copy editing**: fix typos, clarify language, and improve the quality of the docs.
- **Formatting**: help keep docs easy to read with consistent formatting.

## Code Style

This repository uses best practice to maintain code style and consistency,
and to avoid style arguments.

- Python (.py)
    Use the [PEP8 style guide](https://peps.python.org/pep-0008) and apply it in python files in project.

- JSON (.json)
    Use the [Google style guide](https://google.github.io/styleguide/jsoncstyleguide.xml) and apply it in json files and dictionary elements in project.

- Markdown (.md)
    Use the [markdownlint style guide](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) and apply it in markdown files in project.

- Unix Shell (.sh)
    Use the [Google style guide](https://google.github.io/styleguide/shellguide.html) and apply it in shell files in project.

- PowerShell (.ps1)
    Use the [PoshCode style guide](https://github.com/PoshCode/PowerShellPracticeAndStyle) and apply it in PowerShell files in project.

<!-- - Log (.log) -->

<!-- - Yml / Yaml (.yml / .yaml) -->

## Project Governance

Individuals making significant and valuable contributions are given commit-access to the project to contribute as they see fit.

### Rules

There are a few basic ground-rules for contributors:

1. **No `--force` pushes** or modifying the Git history in any way.
2. **Non-master branches** should be used for ongoing work.
3. **Significant modifications** like API changes should be subject to a **pull request** to solicit feedback from other contributors.
4. **Pull requests** are _encouraged_ for all contributions to solicit feedback, but left to the discretion of the contributor.

### Releases

Declaring formal releases remains the prerogative of the project maintainer.

### Changes to this arrangement

This is an experiment and feedback is welcome! This document may also be subject to pull-requests or changes by contributors where you believe you have something valuable to add or change.

## Pull Request

1. Having a GitHub account ([Click to sign up](https://github.com/signup)).

2. [Fork](https://help.github.com/articles/fork-a-repo/) the [auto-registrar](https://github.com/Yokozuna59/auto-registrar) repository ([Click to fork](https://github.com/Yokozuna59/auto-registrar/fork)).

3. Open a new terminal/cmd/powershell window.

4. Change to directory where you want Auto Registrar to be. For example, Desktop:

    - For Linux and macOS

        ```bash
        cd ~/Desktop
        ```

    - For PowerShell

        ```PowerShell
        cd ~\Destop
        ```

    - For Command Prompt:

        ```cmd
        cd %USERPROFILE%\Desktop
        ```

5. Clone the repository to your device:

    ```bash
    git clone https://github.com/<username>/auto-registrar.git
    ```

6. Change directory to the cloned project:

    ```bash
    cd auto-registrar
    ```

7. Create your new feature branch locally:

    ```bash
    git checkout -b <branch_name>
    ```

    **For clarity**, name your branch `update-xxx` or `fix-xxx`. The `xxx` is a short description of the changes you're making. For example, `update-readme-md` or `fix-typo-in-contributing-md`.

8. Add your changes to git:
    - Add specific file to git using:

        ```bash
        git add path/to/filename.ext
        ```

    - Add all unstaged files using:

        ```bash
        git add *
        ```

9. Commit your changes using a descriptive commit message:

    ```bash
    git commit -sm "Brief Description of Commit"
    ```

   **Note** that **-s**, it's important!

10. Push your commits to your GitHub Fork:

    ```bash
    git push --set-upstream origin <branch_name>
    ```

11. Submit a [pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) ([Click to pull request](https://github.com/Yokozuna59/auto-registrar/pulls)).
