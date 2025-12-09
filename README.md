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

### 3. Deploying Changes
When you are happy with your changes:
1.  Click the **Source Control** icon (branch-looking icon) on the left sidebar.
2.  Type a message in the box (e.g., "Updated contact page colors").
3.  Click **Commit**.
4.  Click **Sync Changes** (or Push).
    *   *This automatically triggers a fresh deployment to sarah.danielsbonnin.com.*

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

## 🌍 Deployment & Verification
Deployment is **automatic**. Any time you push code to the `main` branch, Google Cloud Build picks it up.

### How to check:
1.  **Wait**: Deployments usually take 60-120 seconds.
2.  **Verify**: Visit [https://sarah.danielsbonnin.com](https://sarah.danielsbonnin.com).
3.  **Hard Refresh**: If you don't see changes, try a hard refresh to clear cache:
    *   Mac: `Cmd + Shift + R`
    *   Windows: `Ctrl + F5`
