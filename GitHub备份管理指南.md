
> 面向小白的详细步骤，帮你把 ROS2 项目上传到 GitHub

---

## 📋 目录

1. [准备工作](#准备工作)
2. [创建 GitHub 仓库](#创建-github-仓库)
3. [检查并完善 .gitignore](#检查并完善-gitignore)
4. [提交代码到本地仓库](#提交代码到本地仓库)
5. [连接远程仓库并推送](#连接远程仓库并推送)
6. [日常使用命令](#日常使用命令)
7. [常见问题](#常见问题)

---

## 一、准备工作

### 1.1 检查 Git 是否已安装

```bash
git --version
```

如果提示 "command not found"，先安装：

```bash
sudo apt update
sudo apt install git
```

### 1.2 配置 Git 用户信息（如果还没配置）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

查看配置：

```bash
git config --global --list
```

### 1.3 检查当前项目 Git 状态

```bash
cd /home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system
git status
```

---

## 二、创建 GitHub 仓库

### 方法A：通过网页创建（推荐新手）

1. **登录 GitHub**
   - 打开 https://github.com
   - 登录你的账号（如果没有，先注册）

2. **创建新仓库**
   - 点击右上角 **"+"** → **"New repository"**
   - 填写仓库信息：
     - **Repository name**: `Pure-tracking-slam-automatic-navigation-system`（或你喜欢的名字）
     - **Description**: `基于ROS2的差速机器人SLAM建图与自动导航系统`
     - **Visibility**: 
       - `Public`：公开，所有人都能看到（推荐）
       - `Private`：私有，只有你能看到（需要付费账号）
     - **不要勾选**：
       - ❌ Initialize this repository with a README
       - ❌ Add .gitignore
       - ❌ Choose a license
     - （因为你的项目已经有代码了）
   - 点击 **"Create repository"**

3. **复制仓库地址**
   - 创建成功后，GitHub 会显示仓库地址，类似：
     ```
     https://github.com/你的用户名/Pure-tracking-slam-automatic-navigation-system.git
     ```
   - 或者 SSH 地址：
     ```
     git@github.com:你的用户名/Pure-tracking-slam-automatic-navigation-system.git
     ```
   - **复制这个地址**，后面要用

### 方法B：通过 GitHub CLI（如果你安装了）

```bash
gh repo create Pure-tracking-slam-automatic-navigation-system --public --source=. --remote=origin --push
```

---

## 三、检查并完善 .gitignore

ROS2 项目需要忽略编译生成的文件，创建一个 `.gitignore` 文件：

### 3.1 检查是否已有 .gitignore

```bash
ls -la | grep .gitignore
```

### 3.2 创建/编辑 .gitignore 文件

```bash
cd /home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system
nano .gitignore
```

### 3.3 .gitignore 内容（复制粘贴进去）

```gitignore
# ROS2 编译生成的文件（必须忽略）
build/
install/
log/

# Python 缓存文件
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE 配置文件（可选）
.vscode/
.idea/
*.swp
*.swo
*~

# 系统文件
.DS_Store
Thumbs.db

# 临时文件
*.tmp
*.bak
*.log

# 项目特定的（如果需要忽略）
# *.world.backup
# *.urdf.backup

# 但保留这些（用 ! 表示不忽略）
!README.md
!LICENSE
```

**保存并退出**：
- `nano`：按 `Ctrl+X`，然后 `Y`，然后 `Enter`
- `vim`：按 `Esc`，输入 `:wq`，按 `Enter`

---

## 四、提交代码到本地仓库

### 4.1 查看当前状态

```bash
cd /home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system
git status
```

### 4.2 添加所有文件到暂存区

```bash
# 添加所有文件（包括新建的 .gitignore）
git add .

# 或者只添加特定文件
# git add src/ .gitignore README.md
```

### 4.3 提交到本地仓库

```bash
git commit -m "Initial commit: ROS2 SLAM导航项目

- 添加 Gazebo 仿真环境
- 添加 SLAM 建图功能
- 添加 A* 路径规划
- 添加纯追踪路径跟踪
- 添加项目文档"
```

**提交信息规范**：
- 第一行：简短描述（50字以内）
- 空一行
- 详细描述（可选）
- 使用中文或英文都可以

### 4.4 查看提交历史

```bash
git log --oneline
```

---

## 五、连接远程仓库并推送

### 5.1 检查是否已有远程仓库

```bash
git remote -v
```

### 5.2A 如果没有远程仓库，添加新的

```bash
# 使用 HTTPS 地址（推荐新手）
git remote add origin https://github.com/你的用户名/Pure-tracking-slam-automatic-navigation-system.git

# 或者使用 SSH 地址（需要配置 SSH key）
# git remote add origin git@github.com:你的用户名/Pure-tracking-slam-automatic-navigation-system.git
```

### 5.2B 如果已有远程仓库，修改地址

```bash
# 查看当前远程地址
git remote get-url origin

# 修改远程地址
git remote set-url origin https://github.com/你的用户名/Pure-tracking-slam-automatic-navigation-system.git
```

### 5.3 重命名分支（如果需要）

```bash
# 查看当前分支
git branch

# 如果当前分支是 masters，改名为 main（GitHub 默认）
git branch -M main
```

### 5.4 推送代码到 GitHub

```bash
# 第一次推送
git push -u origin main

# 或者如果当前分支是 masters
# git push -u origin masters
```

**注意**：
- 如果使用 HTTPS，GitHub 会要求输入用户名和密码（或 Personal Access Token）
- 如果使用 SSH，需要先配置 SSH key（见下方说明）

### 5.5 验证推送成功

- 打开 GitHub 网页，刷新你的仓库页面
- 应该能看到所有代码文件了

---

## 六、日常使用命令

### 6.1 查看状态

```bash
git status
```

### 6.2 添加修改的文件

```bash
# 添加所有修改
git add .

# 或添加特定文件
git add src/nav_slam/nav_slam/astar.py
```

### 6.3 提交修改

```bash
git commit -m "修复A*路径规划bug"
```

### 6.4 推送到 GitHub

```bash
git push
```

### 6.5 拉取远程更新（如果多台电脑工作）

```bash
git pull
```

### 6.6 查看提交历史

```bash
git log --oneline --graph --all
```

---

## 七、配置 GitHub 认证（重要）

### 方法A：使用 Personal Access Token（推荐）

1. **生成 Token**
   - 登录 GitHub
   - 点击右上角头像 → **Settings**
   - 左侧菜单 → **Developer settings**
   - **Personal access tokens** → **Tokens (classic)**
   - 点击 **Generate new token** → **Generate new token (classic)**
   - 填写信息：
     - Note: `ROS2项目备份`
     - Expiration: 选择过期时间（如 90 days）
     - 勾选权限：`repo`（全部勾选）
   - 点击 **Generate token**
   - **复制 token**（只显示一次，务必保存）

2. **使用 Token 推送**
   - 推送时，密码处输入刚才复制的 token
   - 或者配置 Git 凭证存储：

```bash
git config --global credential.helper store
```

### 方法B：使用 SSH Key（适合高级用户）

1. **生成 SSH Key**

```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```

按提示操作（直接回车使用默认路径）

2. **查看公钥**

```bash
cat ~/.ssh/id_ed25519.pub
```

复制输出的内容

3. **添加到 GitHub**
   - GitHub → Settings → SSH and GPG keys
   - New SSH key
   - 粘贴公钥，保存

4. **测试连接**

```bash
ssh -T git@github.com
```

应该看到：`Hi 你的用户名! You've successfully authenticated...`

5. **使用 SSH 地址**

```bash
git remote set-url origin git@github.com:你的用户名/仓库名.git
```

---

## 八、常见问题

### Q1: 推送时提示 "remote: Support for password authentication was removed"

**A**: GitHub 不再支持密码登录，需要使用 Personal Access Token 或 SSH Key。

**解决**：
```bash
# 方法1：使用 Token（见上面的方法A）
# 方法2：使用 SSH（见上面的方法B）
```

### Q2: 想忽略某些文件但已经提交了

**A**: 需要先从 Git 中删除，但保留本地文件：

```bash
# 删除 Git 跟踪，但保留本地文件
git rm --cached build/ -r
git rm --cached install/ -r
git rm --cached log/ -r

# 提交删除
git commit -m "移除编译文件从Git跟踪"

# 推送到远程
git push
```

### Q3: 提交了错误的文件，想撤销

**A**: 

```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 完全撤销（删除修改）
git reset --hard HEAD~1
```

### Q4: 想查看远程仓库信息

**A**: 

```bash
git remote -v
git remote show origin
```

### Q5: 推送时提示 "error: failed to push some refs"

**A**: 可能是远程仓库有更新，需要先拉取：

```bash
git pull origin main --rebase
git push
```

或者强制推送（**危险，会覆盖远程**）：

```bash
git push -f origin main
```

---

## 九、完整操作示例

假设你第一次创建 GitHub 仓库：

```bash
# 1. 进入项目目录
cd /home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system

# 2. 检查状态
git status

# 3. 创建/编辑 .gitignore（如果还没有）
nano .gitignore
# 粘贴 .gitignore 内容，保存退出

# 4. 添加所有文件
git add .

# 5. 提交
git commit -m "Initial commit: ROS2 SLAM导航项目"

# 6. 添加远程仓库（替换成你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 7. 重命名分支为 main（如果需要）
git branch -M main

# 8. 推送
git push -u origin main
```

---

## 十、建议的最佳实践

1. **频繁提交**：每次完成一个小功能就提交一次
2. **清晰的提交信息**：说明这次提交做了什么
3. **定期推送**：至少每天推送一次到 GitHub
4. **创建分支**：开发新功能时创建新分支，完成后合并

```bash
# 创建新分支
git checkout -b feature/new-feature

# 开发完成后合并
git checkout main
git merge feature/new-feature
git push
```

5. **定期备份**：即使有了 GitHub，也建议定期本地备份

---

**祝你备份顺利！** 🚀

如有问题，随时查看 `git status` 和 `git log` 来了解当前状态。

