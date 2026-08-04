from typing import Any


class Clothing:
    """表示智能衣柜中的一件衣物。"""

    def __init__(
        self,
        clothing_id: int,
        name: str,
        category: str,
        color: str,
        season: str,
        scenes: list[str],
    ) -> None:
        self.clothing_id = clothing_id
        self.name = name
        self.category = category
        self.color = color
        self.season = season
        self.scenes = scenes

    def to_dict(self) -> dict[str, Any]:
        """将 Clothing 对象转换为可保存到 JSON 的字典。"""
        return {
            "id": self.clothing_id,
            "name": self.name,
            "category": self.category,
            "color": self.color,
            "season": self.season,
            "scenes": self.scenes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Clothing":
        """将 JSON 字典转换成 Clothing 对象。"""
        return cls(
            clothing_id=data["id"],
            name=data["name"],
            category=data["category"],
            color=data["color"],
            season=data["season"],
            scenes=data["scenes"],
        )

    def display(self) -> str:
        """生成适合在终端显示的衣物信息。"""
        print(f"ID: {self.clothing_id}, Name: {self.name}, Category: {self.category}, Color: {self.color}, Season: {self.season}, Scenes: {self.scenes}")
        # TODO：由你完成
        pass