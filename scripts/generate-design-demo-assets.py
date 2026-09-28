"""Create local schematic drawings and a tiny glTF 2.0 building model for the demo."""

from __future__ import annotations

import json
import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "static" / "design-demo"
ROOT.mkdir(parents=True, exist_ok=True)

DRAWINGS = [
    ("cultural", "江湾文化艺术中心", "#587d76"),
    ("campus", "绿谷科创园区", "#718666"),
    ("station", "南站城市更新综合体", "#7c766f"),
    ("library", "湖畔社区图书馆", "#65858b"),
]


def drawing_svg(title: str, color: str, section: bool) -> str:
    grid = "".join(
        f'<path d="M{x} 0V720 M0 {y}H1120" stroke="#dce5e2" stroke-width="1" />'
        for x, y in zip(range(0, 1121, 56), range(0, 721, 36))
    )
    if section:
        geometry = f"""
        <path d="M100 580H1010" stroke="{color}" stroke-width="5"/>
        <path d="M170 580V470H320V394H460V334H690V378H820V460H970V580" fill="none" stroke="{color}" stroke-width="7"/>
        <path d="M170 470H970 M320 394H820 M460 334H690" fill="none" stroke="{color}" stroke-width="3"/>
        <path d="M200 505H940 M350 430H785" stroke="{color}" stroke-width="2" stroke-dasharray="9 8"/>
        <path d="M210 510V580 M300 510V580 M390 510V580 M480 510V580 M570 510V580 M660 510V580 M750 510V580 M840 510V580 M930 510V580" stroke="{color}" stroke-width="2"/>
        <circle cx="90" cy="514" r="27" fill="#d7e5dc"/><path d="M90 535V580" stroke="{color}" stroke-width="4"/>
        <circle cx="1025" cy="495" r="36" fill="#d7e5dc"/><path d="M1025 530V580" stroke="{color}" stroke-width="4"/>
        <text x="190" y="630" font-size="18" fill="#809692">SOUTH ELEVATION / 南立面示意</text>
        """
    else:
        geometry = f"""
        <rect x="130" y="184" width="850" height="410" rx="8" fill="none" stroke="{color}" stroke-width="5"/>
        <rect x="180" y="230" width="275" height="315" fill="#e5efea" stroke="{color}" stroke-width="4"/>
        <rect x="505" y="230" width="420" height="120" fill="#dce9e4" stroke="{color}" stroke-width="4"/>
        <rect x="505" y="405" width="420" height="140" fill="#dce9e4" stroke="{color}" stroke-width="4"/>
        <rect x="535" y="375" width="360" height="18" rx="9" fill="#c5ddd4"/>
        <path d="M455 255H505 M455 315H505 M455 375H505 M455 435H505 M455 495H505" stroke="{color}" stroke-width="2"/>
        <path d="M625 230V350 M745 230V350 M625 405V545 M745 405V545" stroke="{color}" stroke-width="2"/>
        <circle cx="90" cy="250" r="21" fill="#cadfd2"/><circle cx="90" cy="525" r="21" fill="#cadfd2"/>
        <circle cx="1020" cy="295" r="21" fill="#cadfd2"/><circle cx="1020" cy="500" r="21" fill="#cadfd2"/>
        <text x="180" y="637" font-size="18" fill="#809692">CONCEPT FLOOR PLAN / 概念平面示意</text>
        """
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 720">
    <rect width="1120" height="720" fill="#f6faf8"/>{grid}
    <text x="56" y="72" font-family="Arial, sans-serif" font-size="20" fill="{color}" font-weight="bold">DESIGN INSTITUTE / PROJECT STUDY</text>
    <text x="56" y="111" font-family="Arial, sans-serif" font-size="26" fill="#314c49">{title}</text>
    <path d="M56 134H1064" stroke="#b8cec6" stroke-width="2"/>{geometry}
    <text x="1010" y="665" font-family="Arial, sans-serif" font-size="16" fill="#9aaca7" text-anchor="end">ILLUSTRATIVE DRAWING · NOT FOR CONSTRUCTION</text>
    </svg>"""


for prefix, title, color in DRAWINGS:
    for kind in ("plan", "section"):
        (ROOT / f"{prefix}-{kind}.svg").write_text(
            drawing_svg(title, color, kind == "section"), encoding="utf-8"
        )


binary = bytearray()
buffer_views = []
accessors = []
meshes = []
nodes = []


def align_buffer() -> None:
    binary.extend(b"\0" * ((4 - len(binary) % 4) % 4))


def add_accessor(values: list[float] | list[int], component_type: int, type_name: str, count: int, target: int, bounds: bool = False) -> int:
    align_buffer()
    offset = len(binary)
    fmt = "f" if component_type == 5126 else "H"
    binary.extend(struct.pack("<" + fmt * len(values), *values))
    buffer_views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(binary) - offset, "target": target})
    accessor = {"bufferView": len(buffer_views) - 1, "componentType": component_type, "count": count, "type": type_name}
    if bounds:
        triples = list(zip(*(iter(values),) * 3))
        accessor["min"] = [min(point[i] for point in triples) for i in range(3)]
        accessor["max"] = [max(point[i] for point in triples) for i in range(3)]
    accessors.append(accessor)
    return len(accessors) - 1


def box(name: str, center: tuple[float, float, float], size: tuple[float, float, float], material: int) -> None:
    cx, cy, cz = center
    sx, sy, sz = (dimension / 2 for dimension in size)
    faces = [
        ((0, 0, 1), [(-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]),
        ((0, 0, -1), [(sx, -sy, -sz), (-sx, -sy, -sz), (-sx, sy, -sz), (sx, sy, -sz)]),
        ((1, 0, 0), [(sx, -sy, sz), (sx, -sy, -sz), (sx, sy, -sz), (sx, sy, sz)]),
        ((-1, 0, 0), [(-sx, -sy, -sz), (-sx, -sy, sz), (-sx, sy, sz), (-sx, sy, -sz)]),
        ((0, 1, 0), [(-sx, sy, sz), (sx, sy, sz), (sx, sy, -sz), (-sx, sy, -sz)]),
        ((0, -1, 0), [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, -sy, sz), (-sx, -sy, sz)]),
    ]
    positions: list[float] = []
    normals: list[float] = []
    indices: list[int] = []
    for normal, corners in faces:
        start = len(positions) // 3
        for x, y, z in corners:
            positions.extend((cx + x, cy + y, cz + z))
            normals.extend(normal)
        indices.extend((start, start + 1, start + 2, start, start + 2, start + 3))
    pos = add_accessor(positions, 5126, "VEC3", 24, 34962, True)
    norm = add_accessor(normals, 5126, "VEC3", 24, 34962)
    idx = add_accessor(indices, 5123, "SCALAR", 36, 34963)
    meshes.append({"name": name, "primitives": [{"attributes": {"POSITION": pos, "NORMAL": norm}, "indices": idx, "material": material}]})
    nodes.append({"mesh": len(meshes) - 1, "name": name})


materials = [
    {"name": "warm limestone", "pbrMetallicRoughness": {"baseColorFactor": [0.8, 0.78, 0.7, 1], "metallicFactor": 0.05, "roughnessFactor": 0.82}},
    {"name": "blue glass", "pbrMetallicRoughness": {"baseColorFactor": [0.29, 0.56, 0.62, 1], "metallicFactor": 0.18, "roughnessFactor": 0.25}},
    {"name": "roof metal", "pbrMetallicRoughness": {"baseColorFactor": [0.34, 0.41, 0.41, 1], "metallicFactor": 0.48, "roughnessFactor": 0.52}},
    {"name": "landscape", "pbrMetallicRoughness": {"baseColorFactor": [0.35, 0.56, 0.41, 1], "metallicFactor": 0, "roughnessFactor": 1}},
]

box("ground plane", (0, -0.16, 0), (10.8, 0.22, 7.5), 3)
box("public podium", (0, 0.42, 0), (8.8, 1.2, 5.5), 0)
box("central atrium glazing", (0, 1.15, 2.78), (4.8, 1.75, 0.15), 1)
box("north gallery", (-2.45, 1.65, -0.35), (3.45, 1.65, 4.25), 0)
box("south gallery", (2.45, 1.65, -0.35), (3.45, 1.65, 4.25), 0)
box("upper glass bridge", (0, 2.26, -0.1), (2.1, 0.65, 3.2), 1)
box("left roof", (-2.45, 2.57, -0.35), (3.75, 0.18, 4.55), 2)
box("right roof", (2.45, 2.57, -0.35), (3.75, 0.18, 4.55), 2)
box("entrance canopy", (0, 1.35, 3.4), (4.4, 0.12, 1.3), 2)
for x in (-3.55, -2.35, 2.35, 3.55):
    box(f"facade mullion {x}", (x, 0.9, 2.9), (0.07, 1.55, 0.08), 2)
for x in (-4.6, -3.8, 3.8, 4.6):
    box(f"tree {x}", (x, 0.45, 3.2), (0.35, 0.85, 0.35), 3)

gltf = {
    "asset": {"version": "2.0", "generator": "Design Demo asset generator"},
    "scene": 0,
    "scenes": [{"nodes": list(range(len(nodes)))}],
    "nodes": nodes,
    "meshes": meshes,
    "materials": materials,
    "buffers": [{"byteLength": len(binary)}],
    "bufferViews": buffer_views,
    "accessors": accessors,
}
json_chunk = json.dumps(gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
json_chunk += b" " * ((4 - len(json_chunk) % 4) % 4)
align_buffer()
total_length = 12 + 8 + len(json_chunk) + 8 + len(binary)
with (ROOT / "civic-building.glb").open("wb") as file:
    file.write(struct.pack("<4sII", b"glTF", 2, total_length))
    file.write(struct.pack("<I4s", len(json_chunk), b"JSON"))
    file.write(json_chunk)
    file.write(struct.pack("<I4s", len(binary), b"BIN\0"))
    file.write(binary)

print(f"Generated drawings and model in {ROOT}")
