from wardrobe import (
    load_clothes,
    add_clothing,
    list_clothes,
    filter_by_category,
    delete_clothing,
)


def print_menu() -> None:
    print("\n========== 智能衣柜 ==========")
    print("1. 添加衣物")
    print("2. 查看全部衣物")
    print("3. 按类别筛选")
    print("4. 删除衣物")
    print("5. 退出")


def main() -> None:
    load_clothes()
    while True:
        print_menu()
        choice = input("请输入选项: ")
        if choice == "1":
            name = input("请输入衣物名称（如：白色短袖）: ")
            category = input("请输入衣物类别（如：上衣）: ")
            color = input("请输入衣物颜色（如：白色）: ")
            season = input("请输入适合季节（如：夏季）: ")
            add_clothing(name=name, category=category, color=color, season=season)
        elif choice == "2":
            list_clothes()
        elif choice == "3":
            category = input("请输入衣物类别（如：上衣）: ")
            clothes = filter_by_category(category)
            print(clothes)
        elif choice == "4":
            list_clothes()
            try:
                clothing_id = int(input("请输入衣物 ID: "))
            except ValueError:
                print("ID 必须是整数。")
                continue
            if delete_clothing(clothing_id):
                print("删除成功")
            else:
                print("删除失败")
        elif choice == "5":
            print("退出程序")
            break
        else:
            print("无效选项，请重新输入")


if __name__ == "__main__":
    main()
