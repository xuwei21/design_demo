"""Create five idempotent Open WebUI workspace models for the design demo.

Set OPEN_WEBUI_TOKEN and OPEN_WEBUI_BASE_MODEL before running. Existing agent models
are left untouched so administrators can tune their prompts in Workspace later.
"""

from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = os.environ.get("OPEN_WEBUI_URL", "http://localhost:3000").rstrip("/")
TOKEN = os.environ.get("OPEN_WEBUI_TOKEN", "").strip()
BASE_MODEL = os.environ.get("OPEN_WEBUI_BASE_MODEL", "").strip()

AGENTS = [
    (
        "design-agent-requirements",
        "需求分析",
        "梳理设计任务书、场地条件、功能需求、约束、待确认事项与交付清单。",
        "你是建筑设计院的需求分析专员。先区分已确认信息与假设，再按项目目标、范围、场地与规范约束、关键节点、风险和待确认问题输出。对缺失资料明确提出问题，不编造数据。",
    ),
    (
        "design-agent-3d",
        "3D制作",
        "组织建筑体量建模、模型分层、材质和交付格式。",
        "你是建筑设计院的 3D 建模专员。围绕体量、标高、结构网格、构件命名和材质提出可执行的建模步骤。注明尺寸来源和模型精度；在缺少实际建模工具时给出操作清单，不宣称已经完成文件。",
    ),
    (
        "design-agent-render",
        "图片渲染",
        "规划建筑效果图的视角、材质、光照与后期表现。",
        "你是建筑设计院的效果图专员。根据项目定位提出镜头、时间、光照、材质、景观与人物比例建议。输出清晰的渲染 brief；没有生成图片工具时不要声称图片已生成。",
    ),
    (
        "design-agent-quote",
        "报价预估",
        "基于明确假设进行方案阶段成本区间估算。",
        "你是建筑设计院的方案估算专员。先写明面积口径、价格基准与不包含项，再分系统给出估算方法和区间。任何金额必须标注假设和币种，并提示需由造价专业复核。",
    ),
    (
        "design-agent-report",
        "报告生成",
        "把设计材料整理成结构化汇报与交付说明。",
        "你是建筑设计院的报告编制专员。按背景、目标、设计策略、关键指标、风险、下一步组织中文报告。保留事实来源与版本信息，缺失数据标注待补充。",
    ),
]


def request_json(path: str, method: str = "GET", body: dict | None = None):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    request = Request(
        BASE_URL + path,
        data=data,
        method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urlopen(request, timeout=25) as response:
        return json.load(response)


def main() -> int:
    if not TOKEN or not BASE_MODEL:
        print("Set OPEN_WEBUI_TOKEN and OPEN_WEBUI_BASE_MODEL first.", file=sys.stderr)
        return 2

    try:
        base_models = request_json("/api/models/base")
        available = {model.get("id") for model in base_models.get("data", [])}
        if BASE_MODEL not in available:
            print(f"Base model '{BASE_MODEL}' is not available to this account.", file=sys.stderr)
            return 2

        existing = request_json("/api/v1/models/all")
        existing_ids = {model.get("id") for model in existing}

        for model_id, label, description, system_prompt in AGENTS:
            if model_id in existing_ids:
                print(f"Skipped existing model: {model_id}")
                continue
            payload = {
                "id": model_id,
                "base_model_id": BASE_MODEL,
                "name": label,
                "meta": {"description": description, "tags": [{"name": "设计院 Demo"}]},
                "params": {"system": system_prompt},
                "access_grants": [
                    {"principal_type": "anyone", "principal_id": "*", "permission": "read"}
                ],
                "is_active": True,
            }
            request_json("/api/v1/models/create", "POST", payload)
            print(f"Created: {label} ({model_id})")
        return 0
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        print(f"Open WebUI API returned HTTP {error.code}: {detail}", file=sys.stderr)
        return 1
    except URLError as error:
        print(f"Cannot reach Open WebUI at {BASE_URL}: {error.reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
