# design_demo — 设计院主题 Demo

基于 **Open WebUI 0.11.4** 的二次开发演示项目，固定上游提交 `8bd8b4fac5e059578ac0c74b3c18d11139f88b7d`。项目保留 Open WebUI 的登录、聊天、模型选择及品牌标识，新增**设计院主题导航与静态展示页面**（案例、统计、知识库、技能、3D 模型等），并内置四个设计项目示例对话。

## 技术栈

| 层 | 技术 |
| --- | --- |
| 前端 | SvelteKit 5 / Vite 5 / Tailwind CSS 4 / TypeScript |
| 后端 | Python 3.11–3.12 / FastAPI / Uvicorn / SQLite |
| 依赖管理 | npm（前端）、uv 或 pip（后端，`pyproject.toml` + `uv.lock` / `requirements.txt`） |
| 部署 | Docker（`Dockerfile` / `docker-compose.*.yml`） |

## 项目结构（关键部分）

```
design_demo/
├─ src/
│  ├─ lib/design-demo/        # 演示数据：案例、项目、知识文档、默认个人 Skill
│  └─ routes/(app)/demo/      # 设计院主题页面路由
├─ static/design-demo/        # 建筑效果图(png)、平面/立面示意图(svg)、3D 模型(glb)
├─ backend/                   # FastAPI 后端（open_webui 包）
│  ├─ data/                   # 数据目录（webui.db 等）
│  ├─ requirements.txt        # 后端完整依赖
│  ├─ dev.sh / start.sh / start_windows.bat
├─ scripts/
│  ├─ seed-design-agents.py           # 种子 Agent（5 个子 Agent）
│  └─ generate-design-demo-assets.py  # 生成 svg/glb 素材，无外部依赖
├─ docker-compose.design-demo.yml     # 演示用 Docker 编排（端口 3000）
├─ DESIGN_DEMO.md            # 本项目详细说明
└─ README.md                 # 上游 Open WebUI 官方说明（未改动）
```

## 环境要求

| 工具 | 要求 | 本机现状 |
| --- | --- | --- |
| Node.js | `>=18.13.0 <=22.x`（建议 22） | ✅ v22.23.2 |
| Python | `>=3.11 <3.13`（`pyproject.toml` 约束） | ⚠️ 当前仅 3.14，需另装 3.12 |
| Docker Desktop | 仅备选（Docker 方式）需要 | 可选 |
| uv | 可选，用 uv 装后端依赖时需要 | 未安装 |

---

## 一、本地调试（推荐）

日常开发推荐前后端分离调试：可热重载，改动即时生效。需要**两个终端**，一个跑后端（8080），一个跑前端（5173，代理 `/api`、`/ws` 等到 8080）。

### 1. 后端（终端 1）

```powershell
# ① 准备 Python 3.12
#    先执行 py -0p 查看已安装版本；若没有 3.11/3.12，到 python.org 安装 3.12（勾选 py launcher）

# ② 在仓库根目录（本文件所在目录）创建虚拟环境并安装后端依赖
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt -U
# 依赖较大；如需精简版可用 backend\requirements-slim.txt

# ③ 准备 .env（后端启动时会从仓库根目录加载 .env）
Copy-Item .env.example .env
# 认证默认开启，直接跑 uvicorn 必须设置密钥，请在 .env 末尾追加一行：
# WEBUI_SECRET_KEY=<至少 24 位的随机字符串>

# ④ 启动后端（--reload 热重载）
cd backend
..\.venv\Scripts\python -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --reload
```

> 备选：直接运行 `backend\start_windows.bat`——它会自动生成 `.webui_secret_key` 并启动 uvicorn，但默认不带 `--reload`。

### 2. 前端（终端 2）

```powershell
# 以下命令均在仓库根目录（本文件所在目录）执行
npm install
npm run dev        # 开发服务器 http://localhost:5173（首次会先执行 pyodide:fetch，需联网）
```

- 默认端口 5173 被占用时改用：`npm run dev:5050`
- 后端不在 8080 时，可通过环境变量 `WEBUI_BACKEND_URL` 调整代理目标。

### 3. 验证

1. 打开 <http://localhost:5173>，注册管理员账号登录。
2. 管理设置 → 连接模型（Ollama 或任意 OpenAI 兼容接口）。
3. 按 DESIGN_DEMO.md 的检查清单逐项验证：六项导航、历史项目切换、案例/知识库搜索、3D 模型、目录上传、Agent 路由。

---

## 二、Docker 方式运行（备选）

不想本地装依赖时，可用 Docker 一键起演示环境：

```powershell
docker compose -f docker-compose.design-demo.yml up --build -d
```

- 打开 <http://localhost:3000>，注册首位管理员账号并登录。
- 首次构建会下载上游依赖，耗时较长。
- 停止 / 查看日志：

```powershell
docker compose -f docker-compose.design-demo.yml down
docker compose -f docker-compose.design-demo.yml logs -f
```

---

## 三、常用调试命令速查表

| 目的 | 命令 | 说明 |
| --- | --- | --- |
| 前端开发服务器 | `npm run dev` | Vite，端口 5173 |
| 前端备用端口 | `npm run dev:5050` | 端口 5050 |
| Svelte 类型检查 | `npm run check` | svelte-kit sync + svelte-check |
| 类型检查（监听） | `npm run check:watch` | 改代码自动重查 |
| 生产构建 | `npm run build` | 输出 `build/` |
| 构建（监听） | `npm run build:watch` | |
| 预览构建产物 | `npm run preview` | |
| 前端 lint | `npm run lint:frontend` | eslint --fix |
| 后端 lint | `npm run lint:backend` | pylint backend/ |
| 全量 lint | `npm run lint` | 前端 + 类型 + 后端 |
| 代码格式化 | `npm run format` / `npm run format:backend` | prettier / ruff |
| 前端单测 | `npm run test:frontend` | vitest |
| 种子 Agent | `python scripts\seed-design-agents.py` | 见下 |
| 生成素材 | `python scripts\generate-design-demo-assets.py` | 生成 svg/glb，无外部依赖 |

### 种子 Agent（5 个子 Agent）

获取管理员 API Token 后，设置环境变量再运行：

```powershell
$env:OPEN_WEBUI_URL      = "http://localhost:3000"   # 默认就是该值，可省略
$env:OPEN_WEBUI_TOKEN    = "<管理员 API Token>"
$env:OPEN_WEBUI_BASE_MODEL = "<基础模型 ID>"
python scripts\seed-design-agents.py
```

脚本只创建缺失的模型，不会覆盖已编辑的模型；Agent 固定 ID 与前端菜单一致。

---

## 四、常见问题

| 现象 | 处理 |
| --- | --- |
| 后端启动报 `WEBUI_SECRET_KEY is not set` | 认证默认开启。在根目录 `.env` 中设置 `WEBUI_SECRET_KEY`，或改用 `backend\start_windows.bat` |
| 前端连不上后端 / CORS 报错 | 确认后端已在 8080 启动；`.env` 中 `CORS_ALLOW_ORIGIN` 建议设为 `http://localhost:5173;http://localhost:8080`（示例值 `*` 也可用） |
| Python 版本不满足 | 项目要求 `>=3.11 <3.13`；`py -0p` 查看本机版本，安装 3.12 后用 `py -3.12 -m venv .venv` |
| 模型未配置 | 案例、统计、知识库、技能与示例历史项目仍可浏览；发送聊天消息需要实际模型 |
| `npm run check` 报大量类型错误 | 属上游代码现状（隐式 any 等，当前约 6900 条，全部位于上游文件，与 design-demo 新增代码无关）；命令可正常运行 |
| 8080 端口被占用 | 换端口启动 uvicorn，并通过 `WEBUI_BACKEND_URL` 告知前端 |
| 5173 端口被占用 | 用 `npm run dev:5050` |
| 首次 `npm run dev` 很慢 | 会先执行 `pyodide:fetch` 下载前端运行依赖，需要网络 |

---

## 五、演示数据说明

- 首次登录且聊天列表为空时，自动创建四条设计项目示例对话；之后的真实对话继续出现在「历史项目」下。
- 案例、项目、知识文档与默认个人 Skill 数据位于 `src/lib/design-demo/data.ts`；Skill 的模拟异步更新保存在浏览器 `localStorage`。
- 建筑效果图位于 `static/design-demo/`（由内置 ImageGen 生成，16:9 专业建筑效果图，无文字水印）。
- 平面/立面示意图与 `.glb` 3D 模型由 `scripts/generate-design-demo-assets.py` 生成，无外部资源依赖。

## 相关文档

- [DESIGN_DEMO.md](./DESIGN_DEMO.md) — 本项目详细说明
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — 上游排障指南
- [README.md](./README.md) — 上游 Open WebUI 官方说明
