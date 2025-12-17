# The Crocheted Crumb - Site Development Guide

Welcome to the source code for **sarah.danielsbonnin.com**!
This guide explains how to make changes, preview them, and deploy them to the live site.

## 🚀 Recommended: Online Development (GitHub Codespaces)
The easiest way to work is using **GitHub Codespaces**. This gives you a full coding environment right in your browser, no installation required.

### 1. Start Coding
1.  Click the likely green **Code** button on this page.
2.  Select the **Codespaces** tab.
3.  Click **Create codespace on main**.
    *   *This will open a VS Code editor in your browser.*

### 2. Previewing Your Site
1.  In the terminal at the bottom (if closed, press `Ctrl + ` ), run:
    ```bash
    python app.py
    ```
2.  A popup will appear saying "Your application running on port 8080 is available.".
3.  Click **Open in Browser**.
    *   *This opens a private preview of your site.*
4.  Make code changes and refresh the preview tab to see them instantly.

### 3. Making Changes and Creating a Pull Request
When you want to make changes:
1.  Create a new branch for your changes in Codespaces.
2.  Make your code changes and test them locally with `python app.py`.
3.  Click the **Source Control** icon (branch-looking icon) on the left sidebar.
4.  Type a message in the box (e.g., "Updated contact page colors").
5.  Click **Commit**.
6.  Click **Sync Changes** (or Push) to push your branch.
7.  Create a Pull Request on GitHub to preview your changes in the beta environment.

---

## 💻 Local Development (Macbook)
If you prefer working on your own machine.

### Prerequisites
*   **Docker Desktop**: [Download & Install](https://www.docker.com/products/docker-desktop/)
*   **VS Code**: [Download & Install](https://code.visualstudio.com/)

### 1. Clone & Open
1.  Open Terminal.
2.  Clone the repo:
    ```bash
    git clone https://github.com/sarahbonnin-source/crocheted-crumb-site.git
    cd crocheted-crumb-site
    ```

### 2. Run with Docker
1.  Build and Run:
    ```bash
    docker build -t sarah-site .
    docker run -p 8080:8080 sarah-site
    ```
2.  Open `http://localhost:8080` in your browser to preview.

---

## 🌍 Deployment Process

This site uses a two-stage deployment process:

### 🎨 Preview Deployment (for testing)
When you create or update a **Pull Request**, the site is automatically deployed to a preview environment for acceptance testing.

1.  **Create a PR**: Make your changes in a branch and open a pull request.
2.  **Automatic Preview**: GitHub Actions will automatically deploy your changes to the beta environment.
3.  **Get the URL**: A comment will appear on your PR with the preview URL (e.g., `https://sarah-danielsbonnin-com-beta-*.run.app`).
4.  **Test**: Visit the preview URL to test your changes before merging.

### 🚀 Production Deployment (live site)
Production deployment to **sarah.danielsbonnin.com** happens **only when you push a version tag**.

1.  **Merge your PR**: Once your changes are approved and tested, merge the PR to main.
2.  **Create a version tag**: Tag your release with a version number:
    ```bash
    git tag v1.0.0
    git push origin v1.0.0
    ```
3.  **Automatic Production Deploy**: GitHub Actions will automatically deploy the tagged version to production.
4.  **Verify**: Visit [https://sarah.danielsbonnin.com](https://sarah.danielsbonnin.com) after 60-120 seconds.
5.  **Hard Refresh**: If you don't see changes, try a hard refresh to clear cache:
    *   Mac: `Cmd + Shift + R`
    *   Windows: `Ctrl + F5`

### Version Tag Format
Use semantic versioning for tags:
-   `v1.0.0` - Major version
-   `v1.1.0` - Minor version (new features)
-   `v1.0.1` - Patch version (bug fixes)

Or simply:
-   `1.0.0`, `1.1.0`, `1.0.1` (without the 'v' prefix)
