# Pre-Training Preparation Checklist

## DevSecOps Training with OWASP Juice Shop

**Send to Trainees: 48-72 hours before training session**

---

## 📋 Overview

This 3-4 hour hands-on training requires significant local setup. Please complete ALL items below **before** the training session to ensure a smooth start.

**Estimated setup time: 45-60 minutes**

---

## 🖥️ System Requirements

### Minimum Hardware

- [ ] **RAM**: 8GB minimum (16GB recommended for running Docker, Kind cluster, and runners)
- [ ] **Disk Space**: 20GB free space minimum
- [ ] **CPU**: 4 cores minimum (for running 3-node Kubernetes cluster)
- [ ] **Internet**: Stable broadband connection (for Docker pulls)

### Operating System

- [ ] macOS (10.15+), Linux (Ubuntu 20.04+), or Windows 11 with WSL2
- [ ] **Note**: Windows users MUST have WSL2 configured
- [ ] Admin/sudo privileges on your machine

---

## 🛠️ Required Software Installations

### 1. Core Development Tools

#### Git

```bash
# Verify installation
git --version

# If not installed:
# macOS: brew install git
# Linux: sudo apt-get install git
# Windows: https://git-scm.com/download/win
```

- [ ] Git version 2.30+

#### Docker Desktop

- [ ] Download from: https://www.docker.com/products/docker-desktop
- [ ] **CRITICAL**: Allocate at least 6GB RAM to Docker
  - macOS/Windows: Docker Desktop → Settings → Resources → Memory → 6GB+
- [ ] Verify Docker is running:
  ```bash
  docker --version
  docker ps
  ```
- [ ] Expected: Docker version 20.10+ or higher

#### Node.js

- [ ] Download from: https://nodejs.org/ (LTS version)
- [ ] Verify installation:
  ```bash
  node --version  # Should be v18+ or v20+
  npm --version   # Should be v9+
  ```

### 2. Cloud & Infrastructure Tools

#### AWS CLI

- [ ] Install: https://aws.amazon.com/cli/
- [ ] Verify:
  ```bash
  aws --version  # Should be 2.x
  ```
- [ ] **Note**: We'll configure profiles during training

### 3. Kubernetes Tools (Will be installed during training)

**Note**: kubectl and Kind will be auto-installed via `/kind-k8s-setup` slash command during Part 4

Optional pre-installation:

```bash
# macOS
brew install kubectl kind

# Verify
kubectl version --client
kind version
```

### 4. Code Editor

- [ ] **Recommended**: Cursor (https://cursor.sh/)
- [ ] **Alternative**: VS Code with extensions:
  - Docker
  - Kubernetes
  - GitLens
  - ESLint
  - GitHub Actions

### 5. Claude Code CLI ⭐ **CRITICAL**

- [ ] Install from: https://claude.ai/code
- [ ] Verify installation:

  ```bash
  claude --version
  ```
- [ ] **Complete authentication setup**:

  ```bash
  claude login
  # Follow prompts to authenticate
  ```
- [ ] **Verify working**:

  ```bash
  claude "What is Claude Code CLI?"
  ```

  Should receive a response about Claude Code capabilities

---

## 🔑 Required Account Setup

### 1. GitHub Account

- [ ] Create/verify GitHub account: https://github.com
- [ ] **Generate Personal Access Token (PAT)** for:

  - Docker Hub authentication
  - GitHub Actions runner (Part 4)

  Steps:

  1. Go to: https://github.com/settings/tokens/new
  2. Name: "DevSecOps Training"
  3. Expiration: 30 days
  4. Scopes: ✅ `repo`, ✅ `workflow`, ✅ `write:packages`
  5. Generate and **SAVE SECURELY** (you won't see it again!)
- [ ] **Save your PAT**: Format `ghp_xxxxxxxxxxxxxxxxxxxxx`

### 2. Docker Hub Account

- [ ] Create account: https://hub.docker.com/signup
- [ ] **Generate Access Token**:

  1. Account Settings → Security → New Access Token
  2. Name: "DevSecOps Training"
  3. Permissions: Read, Write, Delete
  4. **SAVE TOKEN SECURELY**
- [ ] Verify Docker Hub login:

  ```bash
  docker login
  # Username: your_dockerhub_username
  # Password: your_access_token (NOT your password!)
  ```

### 3. Anthropic Account (for Claude Code CLI)

- [ ] Create account: https://claude.ai
- [ ] **Note**: Claude Code CLI authentication done in Step 5 above

---

## 📦 Repository Setup

### 1. Fork Demo Repository (Recipe App)

- [ ] Navigate to: [Provide Recipe App GitHub URL]
- [ ] Click "Fork" button (top right)
- [ ] Clone your fork:
  ```bash
  git clone https://github.com/YOUR_USERNAME/recipe-app
  cd recipe-app
  ```

### 2. Clone OWASP Juice Shop

```bash
# Create training workspace
mkdir -p ~/devsecops-training
cd ~/devsecops-training

# Clone Juice Shop
git clone https://github.com/juice-shop/juice-shop
cd juice-shop
```

- [ ] Verify clone successful

---

## ✅ Pre-Training Verification Tests

### Test 1: Docker & Juice Shop

Run this 24 hours before training:

```bash
# Pull and run Juice Shop
docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop

# Verify (wait 30 seconds for startup)
curl http://localhost:3000
# Should return HTML

# Open in browser
open http://localhost:3000  # macOS
# or visit http://localhost:3000 in browser

# Stop container
docker stop juice-shop
docker rm juice-shop
```

**Expected Result**: Juice Shop login page loads in browser

- [ ] ✅ Juice Shop runs successfully

### Test 2: Docker Resource Check

```bash
# Check Docker resource allocation
docker info | grep -E 'CPUs|Total Memory'
```

**Expected Result**:

- CPUs: 4+
- Total Memory: 6+ GiB

- [ ] ✅ Docker has sufficient resources

### Test 3: Claude Code CLI Test

```bash
cd ~/devsecops-training/juice-shop

# Test Claude Code
claude "List the main technologies used in this project by reading package.json"
```

**Expected Result**: Claude analyzes and responds with tech stack

- [ ] ✅ Claude Code CLI working

### Test 4: Git & GitHub Connectivity

```bash
# Test Git config
git config --global user.name
git config --global user.email

# If not set:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Test GitHub authentication
ssh -T git@github.com
# OR (if using HTTPS)
git ls-remote https://github.com/YOUR_USERNAME/recipe-app
```

- [ ] ✅ Git configured and GitHub accessible

### Test 5: Node.js & npm

```bash
cd ~/devsecops-training/juice-shop

# Install dependencies (this may take 5-10 minutes)
npm install

# Run tests
npm test
```

**Expected Result**: Tests pass (some may fail - that's intentional!)

- [ ] ✅ npm install completes successfully

---

## 📚 Recommended Pre-Reading (Optional but Helpful)

### Knowledge Prerequisites

- [ ] **Basic Git**: Commits, branches, push/pull
- [ ] **Basic Docker**: What containers are, how to run them
- [ ] **Basic CLI**: Comfortable with terminal/command line
- [ ] **Optional**: Basic JavaScript/Node.js understanding

### Pre-Training Reading (Optional)

- [ ] OWASP Top 10 Overview: https://owasp.org/www-project-top-ten/
- [ ] What is DevSecOps?: https://www.devsecops.org/
- [ ] Claude Code CLI Documentation: https://docs.claude.ai/code

### Videos (Optional)

- [ ] "What is OWASP Juice Shop?" (10 min): https://www.youtube.com/watch?v=Lu0-kDdtVf4
- [ ] "Introduction to Kubernetes" (10 min): https://www.youtube.com/watch?v=VnvRFRk_51k
- [ ] "GitHub Actions in 15 Minutes": https://www.youtube.com/watch?v=R8_veQiYBjI

---

## 🔐 Security & Privacy

### Secure Storage of Credentials

- [ ] **DO NOT** commit tokens/passwords to Git
- [ ] **DO NOT** share your GitHub PAT or Docker Hub token
- [ ] **Create** a secure password manager entry for:
  - GitHub PAT
  - Docker Hub token
  - AWS credentials (if using)

### .gitignore Verification

Ensure these are in your `.gitignore`:

```
.env
*.env
.aws/credentials
kind-k8s-cluster/.env
```

---

## 📝 Day-of-Training Checklist

**On training day, BEFORE session starts:**

- [ ] Laptop fully charged (or charger handy)
- [ ] Docker Desktop running (verify with `docker ps`)
- [ ] Close unnecessary applications (free up RAM)
- [ ] Have GitHub PAT and Docker Hub token ready (in password manager)
- [ ] Have repository URLs bookmarked

---

## ❓ Troubleshooting Guide

### Docker Desktop Not Starting

**Symptoms**: `Cannot connect to Docker daemon`

**Solutions**:

1. Restart Docker Desktop application
2. Increase allocated RAM (Settings → Resources)
3. Restart computer
4. Reinstall Docker Desktop

### Claude Code CLI Authentication Issues

**Symptoms**: `Authentication failed` or `API key invalid`

**Solutions**:

1. Run `claude login` again
2. Check API key at https://console.anthropic.com/
3. Set environment variable: `export ANTHROPIC_API_KEY=sk-...`
4. Clear cache: `rm -rf ~/.claude/cache`

### npm install Failures

**Symptoms**: `EACCES` permission errors

**Solutions**:

```bash
# Fix npm permissions (macOS/Linux)
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Or use nvm for Node version management
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

### Port 3000 Already in Use

**Symptoms**: `Error: Port 3000 is already in use`

**Solutions**:

```bash
# Find process using port 3000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use different port
docker run -d -p 3001:3000 bkimminich/juice-shop
```

### Insufficient Docker Resources

**Symptoms**: Containers crash, slow performance

**Solutions**:

1. Docker Desktop → Settings → Resources
2. Increase RAM to 8GB
3. Increase CPUs to 4+
4. Increase Disk space to 60GB+
5. Restart Docker Desktop

---

## ✅ Final Verification Checklist

**Complete this checklist 24 hours before training and email confirmation:**

```
□ Docker Desktop installed and running (6GB+ RAM allocated)
□ Git installed and configured
□ Node.js 18+ installed
□ Claude Code CLI installed AND authenticated
□ GitHub account created with PAT generated
□ Docker Hub account created with token generated
□ Juice Shop repository cloned
□ Recipe App repository forked and cloned
□ Juice Shop successfully runs on http://localhost:3000
□ Claude Code CLI responds to test queries
□ npm install completed in juice-shop directory
□ All credentials saved securely
□ Code editor (Cursor/VS Code) installed
□ Web browser (Chrome/Firefox) installed

I confirm all items are complete: [Your Name]
Date: [Date]
```

---

## 🎯 What to Expect on Training Day

### What You'll Build

✅ Complete DevSecOps CI/CD pipeline
✅ Local Kubernetes cluster with Kind
✅ Self-hosted GitHub Actions runner in K8s
✅ Security scanning automation (SAST, SCA, DAST)
✅ Deploy Juice Shop to Kubernetes
✅ Hands-on security exploits (ethical hacking)
✅ Custom Claude Code security agents

### Hands-On Labs

- Claude CLI ( Memory / context window / Advanced Automation)
- Simple Pipeline
- Enhanced Pipeline(inclusive of Security scan)
- OWASP Top 10 - via automated way

---

## 🌟 Training Day Quick Reference

### Essential URLs (Bookmark These)

```
Juice Shop Local:      http://localhost:3000
Kube-ops-view:         http://localhost:8080
LocalStack Dashboard:  https://app.localstack.cloud/
GitHub:                https://github.com
Docker Hub:            https://hub.docker.com
Claude Code Docs:      https://docs.claude.ai/code
```

### Essential Commands (Keep Handy)

```bash
# Verify Docker
docker ps

# Start Juice Shop
docker run -d -p 3000:3000 bkimminich/juice-shop

# Check Kubernetes
kubectl get nodes

# Claude Code help
claude --help

# Git status
git status
```

---

## 🎓 Success Tips

1. **DONT Ask questions**: Use support channels if stuck
2. **Stay curious**: We'll hack legally - embrace the mindset!
3. **Collaborate**: This is hands-on, ask peers for help
4. **Have fun**: Security training should be exciting!

**See you at the training! 🚀**

---

*Last Updated: 2025-11-26*
*Version: 1.0*
