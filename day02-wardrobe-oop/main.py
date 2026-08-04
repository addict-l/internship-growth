from pathlib import Path

from recommendation import RecommendationEngine
from wardrobe_manager import WardrobeManager


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "clothes.json"


def print_menu() -> None:
    print("\n========== 智能衣柜 OOP版 ==========")
    print("1. 添加衣物")
    print("2. 查看全部衣物")
    print("3. 按类别筛选")
    print("4. 删除衣物")
    print("5. 推荐衣物")
    print("6. 退出")


def main() -> None:
    manager = WardrobeManager(DATA_FILE)
    engine = RecommendationEngine()

    while True:
        print_menu()
        choice = input("请选择操作：").strip()

        if choice == "1":
            name = input("请输入衣物名称：").strip()
            category = input("请输入衣物类别：").strip()
            color = input("请输入衣物颜色：").strip()
            season = input("请输入衣物季节：").strip()
            scenes = input("请输入衣物场景：").strip()
            manager.add_clothing(name, category, color, season, scenes)
        elif choice == "2":
            manager.list_all()
        elif choice == "3":
            category = input("请输入衣物类别：").strip()
            clothes = manager.filter_by_category(category)
            for clothing in clothes:
                clothing.display()
        elif choice == "4":
            manager.list_all()
            try:
                clothing_id = int(input("请输入衣物ID:").strip())
            except ValueError:
                print("ID 必须是整数。")
                continue
            if manager.delete_clothing(clothing_id):
                print("删除成功")
            else:
                print("删除失败：未找到该 ID")
        elif choice == "5":
            target_season = input("请输入目标季节：").strip()
            target_scene = input("请输入目标场景：").strip()
            preferred_color = input("请输入颜色偏好：").strip()
            results = engine.recommend(manager.clothes,target_season, target_scene, preferred_color)
            if not results:
                print("没有符合条件的推荐。")
            else:
                for clothing, score, reasons in results:
                    clothing.display()
                    print(f"得分: {score}")
                    print(f"推荐原因: {', '.join(reasons)}")
                    print("-" * 50)
        elif choice == "6":
            break
        else:
            print("无效的选项，请重新选择。")

if __name__ == "__main__":
    main()