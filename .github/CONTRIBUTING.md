# Contributing to Auto Registrar

1. Having a GitHub account [(Click to sign up)](https://github.com/signup)

2. [Fork](https://help.github.com/articles/fork-a-repo/) the [auto-registrar](https://github.com/Yokozuna59/auto-registrar) repository [(Click to fork)](https://github.com/Yokozuna59/auto-registrar/fork).

3. Clone the repository to your device:

    ```bash
    git clone https://github.com/<username>/auto-registrar.git
    ```

4. Change directory to the cloned project:

    ```bash
    cd auto-registrar
    ```

5. Create your new feature branch locally:

    ```bash
    git checkout -b <branch_name>
    ```

    **For clarity**, name your branch `update-xxx` or `fix-xxx`. The `xxx` is a short description of the changes you're making, e.g., `update-readme-md` or `fix-typo-in-contributing-md`.

6. Add your changes to git:
    - Add specific file to git using:

        ```bash
        git add path/to/filename.ext
        ```

    - Add all unstaged files using:

        ```bash
        git add *
        ```

7. Commit your changes using a descriptive commit message:

    ```bash
    git commit -sm "Brief Description of Commit"
    ```

   **Note** that **-s**, it's important!

8. Push your commits to your GitHub Fork:

    ```bash
    git push --set-upstream origin <branch_name>
    ```

9. Submit a [pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) [(Click to pull request)](https://github.com/Yokozuna59/auto-registrar/pulls).
