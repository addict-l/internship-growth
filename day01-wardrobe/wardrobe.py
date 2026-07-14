import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "clothes.json"


def load_clothes():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("衣物数据文件格式错误，将使用空衣柜。")
        return []


def save_clothes(clothes):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clothes, f, ensure_ascii=False, indent=2)


def add_clothing(name, category, color, season):
    clothes = load_clothes()
    new_id = max((c["id"] for c in clothes), default=0) + 1
    item = {
        "id": new_id,
        "name": name,
        "category": category,
        "color": color,
        "season": season,
    }
    clothes.append(item)
    save_clothes(clothes)
    return item


def list_clothes():
    clothes = load_clothes()
    for clothing in clothes:
        print(f"ID: {clothing['id']} | {clothing['name']} | {clothing['category']} | {clothing['color']} | {clothing['season']}")

def filter_by_category(category):
    clothes = load_clothes()
    result = []

    for clothing in clothes:
        if clothing["category"] == category:
            result.append(clothing)

    return result

def delete_clothing(id):
    clothes = load_clothes()
    for clothing in clothes:
        if clothing["id"] == id:
            clothes.remove(clothing)
            save_clothes(clothes)
            return True
    return False