# GroupMate AI v2.0

基于原 GroupMate Classroom Python 项目，将 v1.2 LM 风格整合到真实教师与学生页面。
保留现有 API、XIPU 工作流、课堂持久化、证据审核与反馈发布；原型中的模拟按钮与数据未作为后台功能使用。
具体范围见 [集成说明](docs/V2-INTEGRATION.md)。

## 本地启动

需要 Python 3.10+。后端仅使用标准库；提取 PDF 另需安装 Poppler 并让 pdftotext 可执行。
在解压后的项目根目录运行。PowerShell：

```powershell
$env:GROUPMATE_OWNER_SECRET = '自行设置一个长随机教师口令'
$env:GROUPMATE_XIPU_WORKFLOW_KEY = '填入获授权工作流密钥'
python -m groupmate.server --host 127.0.0.1 --port 8765
```

Linux/macOS：

```sh
export GROUPMATE_OWNER_SECRET='choose-a-long-random-password'
export GROUPMATE_XIPU_WORKFLOW_KEY='your-approved-workflow-key'
python3 -m groupmate.server --host 127.0.0.1 --port 8765
```

访问 http://127.0.0.1:8765/；教师数据面板 http://127.0.0.1:8765/teacher。
不设置 XIPU key 也能运行课堂管理，但 AI 生成功能不可用。没有有效密钥时不会自动模拟回答。
教师口令必须通过进程环境设置；原服务仅从本地 .env 补读两种 XIPU key，不会从 .env 读取教师口令。
不要把真实密钥写入 README、前端或提交到 GitHub。

## 环境变量

- GROUPMATE_OWNER_SECRET：必填，现有服务的 owner 身份凭据。升级时保留原值。
- GROUPMATE_TEACHER_PASSWORD：可选，独立登录口令覆盖；遵循现有服务行为。
- GROUPMATE_XIPU_WORKFLOW_KEY：完整自动化工作流密钥。
- GROUPMATE_XIPU_ROLE_KEY：可选，独立角色工作流密钥；未配置时角色调用回退至统一工作流。

沿用原项目 XIPU endpoint 和工作流协议；需保留已发布的远端工作流。仅更换 UI 不会重新创建它。

## 验证与打包

```sh
python -m unittest discover -s tests -v
node native/test_class.js
node native/test_observer.js
python tools/package_release.py
```

GitHub Actions 执行相同测试并产生源码 ZIP，不会部署。Node 仅用于原有工作流资产测试。
测试结果及验证边界见 docs/VERIFICATION.md。
打包采用源码目录白名单，排除课堂数据库、上传文件、日志、缓存和真实 .env；保留案例模板与合成测试输入。

## 上传 GitHub

解压 ZIP，将 GroupMate_AI_v2.0 文件夹内全部源码（包括 .github、.gitignore、.env.example）放到仓库根目录。
首次提交前再次确认没有加入本地 data/、uploads/ 或真实配置。无需提交 ZIP 本身。
此应用需要 Python 服务器，不能仅通过 GitHub Pages 运行。

## 部署、升级和回滚

原部署文件保留在 deploy/。先读 [升级与回滚](docs/UPGRADE-ROLLBACK.md)，再参考
[原部署说明](deploy/README.md)。本次没有执行任何线上部署。

数据库在服务工作目录的 data/classroom.sqlite；本地首次启动自动创建空库。
生产 systemd 使用 /var/lib/groupmate 作为工作目录，源代码在 /opt/groupmate/app，
密钥在 /etc/groupmate/groupmate.env，升级时保持这些位置和权限。
