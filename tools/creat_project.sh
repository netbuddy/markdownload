#!/bin/bash

# 设置项目名称
project_name="markdownload"

# 检查是否已提供项目名
if [ -z "$project_name" ]; then
    echo "Please provide a project name."
    exit 1
fi

# 初始化Git仓库
git init

# 创建项目目录结构
mkdir src
touch README.md
touch .gitignore

# 生成requirements.txt
echo -e "requests\nbeautifulsoup4\nmarkdownify" > requirements.txt

# 编写.gitignore内容
cat << EOF > .gitignore
# Generic
.idea/
.vscode/
*.pyc
*.pyo
*.pth
*.swp
.DS_Store

# Python specific
.env
.pytest_cache/
coverage/
.tox/
.dist/
.build/
*.egg-info/
*.egg
requirements.txt.lock

# Editor directories and files
.vscode/
.idea/

# Dependency directories
node_modules/
.bower-components/
EOF

# 编写README.md的基本内容
echo "# $project_name" > README.md
echo "A Python web scraper project that downloads a webpage and converts its main content to Markdown format." >> README.md

echo "Project \"$project_name\" has been set up successfully."

# 创建env环境，并安装依赖
python -m venv ~/venv/$project_name
source ~/venv/$project_name/bin/activate
pip install -r requirements.txt
