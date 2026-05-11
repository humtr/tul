from __future__ import annotations

from typing import Any

from .errors import TulError


def _scalar(value: str) -> Any:
    value = value.strip()
    if value in ("", "null", "Null", "NULL", "~"):
        return None
    if value in ("true", "True", "TRUE"):
        return True
    if value in ("false", "False", "FALSE"):
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        if value and value == str(int(value)):
            return int(value)
    except Exception:
        pass
    return value


def parse(text: str) -> Any:
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.rstrip()
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.lstrip(" ")))

    def parse_block(i: int, indent: int):
        if i >= len(lines):
            return {}, i

        if lines[i][0] == indent and lines[i][1].startswith("- "):
            arr = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                item = lines[i][1][2:].strip()
                i += 1

                if not item:
                    child, i = parse_block(i, indent + 2)
                    arr.append(child)
                    continue

                if ":" in item and not item.startswith(("'", '"')):
                    k, rest = item.split(":", 1)
                    obj = {k.strip(): _scalar(rest.strip()) if rest.strip() else None}
                    if i < len(lines) and lines[i][0] > indent:
                        child, i = parse_block(i, lines[i][0])
                        if isinstance(child, dict):
                            obj.update(child)
                    arr.append(obj)
                else:
                    arr.append(_scalar(item))
            return arr, i

        obj = {}
        while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
            if ":" not in lines[i][1]:
                raise TulError(f"unsupported yaml line: {lines[i][1]}")
            k, rest = lines[i][1].split(":", 1)
            k = k.strip()
            rest = rest.strip()
            i += 1
            if rest:
                obj[k] = _scalar(rest)
            elif i < len(lines) and lines[i][0] > indent:
                obj[k], i = parse_block(i, lines[i][0])
            else:
                obj[k] = None
        return obj, i

    if not lines:
        return {}
    data, i = parse_block(0, lines[0][0])
    if i != len(lines):
        raise TulError("YAML parser did not consume all lines")
    return data


def dump(data: Any, indent: int = 0) -> str:
    pad = " " * indent
    out = []
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                out.append(f"{pad}{k}:")
                out.append(dump(v, indent + 2).rstrip())
            else:
                out.append(f"{pad}{k}: {v}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if not item:
                    out.append(f"{pad}- {{}}")
                    continue
                keys = list(item.keys())
                first = keys[0]
                first_val = item[first]
                if isinstance(first_val, (dict, list)):
                    out.append(f"{pad}- {first}:")
                    out.append(dump(first_val, indent + 4).rstrip())
                else:
                    out.append(f"{pad}- {first}: {first_val}")
                for k in keys[1:]:
                    v = item[k]
                    if isinstance(v, (dict, list)):
                        out.append(f"{pad}  {k}:")
                        out.append(dump(v, indent + 4).rstrip())
                    else:
                        out.append(f"{pad}  {k}: {v}")
            else:
                out.append(f"{pad}- {item}")
    else:
        out.append(f"{pad}{data}")
    return "\n".join(out) + "\n"
