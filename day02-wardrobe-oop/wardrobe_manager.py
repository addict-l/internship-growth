from ast import For
import json
from pathlib import Path

from models import Clothing


class WardrobeManager:
    """负责衣物数据管理和本地持久化。"""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self.clothes: list[Clothing] = []
        self.load()

    def load(self) -> None:
        if not self.data_file.exists():
            self.clothes = []
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                raw_data = json.load(file)

            self.clothes = [Clothing.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            print("衣物数据文件格式错误，将使用空衣柜。")
            self.clothes = []

    def save(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        data = [
            clothing.to_dict()
            for clothing in self.clothes
        ]

        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def generate_next_id(self) -> int:
        """生成不重复的衣物 ID。"""
        return max((c.clothing_id for c in self.clothes), default=0) + 1

    def add_clothing(
        self,
        name: str,
        category: str,
        color: str,
        season: str,
        scenes: list[str],
    ) -> Clothing:
        """添加衣物并保存。"""
        new_id = self.generate_next_id()
        new_clothing = Clothing(new_id, name, category, color, season, scenes)
        self.clothes.append(new_clothing)
        self.save()
        return new_clothing
        # TODO
        pass

    def delete_clothing(self, clothing_id: int) -> bool:
        """根据 ID 删除衣物。"""
        for clothing in self.clothes:
            if clothing.clothing_id == clothing_id:
                self.clothes.remove(clothing)
                self.save()
                return True
        return False

    def filter_by_category(self, category: str) -> list[Clothing]:
        """根据类别筛选衣物。"""
        # TODO
        result = []
        for clothing in self.clothes:
            if clothing.category == category:
                result.append(clothing)
        return result


    def list_all(self) -> list[Clothing]:
        """返回全部衣物。"""
        for clothing in self.clothes:
            print(
                f"ID: {clothing.clothing_id} | {clothing.name} | "
                f"{clothing.category} | {clothing.color} | {clothing.season}"
            )
        return self.clothes