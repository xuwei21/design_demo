# 设计院主题 Demo

基于 Open WebUI 0.11.4，固定上游提交 `8bd8b4fac5e059578ac0c74b3c18d11139f88b7d`。Demo 保留 Open WebUI 的登录、聊天、模型选择及品牌标识，增加设计院主题导航和静态展示页面。

## 本地启动

1. 启动 Docker Desktop，确保 Docker Engine 可用。
2. 在仓库根目录运行 `docker compose -f docker-compose.design-demo.yml up --build -d`。
3. 打开 `http://localhost:3000`，注册首位管理员账号并登录。首次构建会下载上游依赖，可能需要较长时间。
4. 在管理设置中连接 Ollama 或 OpenAI 兼容模型服务。模型未配置时，案例、统计、知识库、技能与示例历史项目仍可浏览；发送聊天消息需要实际模型。

在使用 Node 本地开发时请用 Node 22；上游 `package.json` 声明支持 Node 18–22。本仓库的 Dockerfile 使用 Node 22 构建前端。

## 配置五个子 Agent

连接基础模型后，获取管理员 API Token，并设置环境变量 `OPEN_WEBUI_TOKEN` 和 `OPEN_WEBUI_BASE_MODEL`。可选设置 `OPEN_WEBUI_URL`，默认 `http://localhost:3000`。运行 `python scripts/seed-design-agents.py`。脚本只创建缺少的模型，不覆盖已经编辑的模型。Agent 的固定 ID 与前端菜单一致；若模型不可用，发送前会提示配置。

目录关联通过浏览器的文件夹选择器读取本地文件列表。用户勾选文件后按 Open WebUI 现有附件机制上传；浏览器不会持久保存目录访问权限。

## 演示数据与素材

- 首次登录且聊天列表为空时，自动创建四条设计项目示例对话；之后新建的真实对话继续出现在“历史项目”下。
- 案例、项目、知识文档与默认个人 Skill 数据位于 `src/lib/design-demo/data.ts`。Skill 的模拟异步更新保存在当前浏览器的 `localStorage`。
- 建筑效果图位于 `static/design-demo/`，由内置 ImageGen 生成。四个提示词分别描述：上海滨水文化中心、杭州绿谷研发园区、南京旧车站更新综合体、苏州湖畔社区图书馆；均要求 16:9、专业建筑效果图、无文字和水印。
- 平面/立面示意图和可旋转缩放的 `.glb` 建筑模型由 `python scripts/generate-design-demo-assets.py` 生成，无外部资源依赖。

## 检查

运行 `npm run check` 和 `npm run build`。前者检查 Svelte 类型，后者验证生产构建。登录后依次检查六项导航、历史项目切换、案例和知识库搜索、3D 模型、目录上传及 Agent 路由。
