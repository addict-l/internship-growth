from models import Clothing


class RecommendationEngine:
    """根据天气、场景和颜色偏好推荐衣物。"""

    def calculate_score(
        self,
        clothing: Clothing,
        target_season: str,
        target_scene: str,
        preferred_color: str,
    ) -> tuple[int, list[str]]:
        """计算单件衣物的推荐分数和推荐原因。"""
        score = 0
        reasons: list[str] = []
        if clothing.season == target_season:
            score+=4
            reasons.append("适合当前季节")
        elif clothing.season == "四季":
            score+=3
            reasons.append("属于四季通用衣物")
        if target_scene in clothing.scenes:
            score+=3
            reasons.append("适合当前场景")
        if preferred_color and clothing.color == preferred_color:
            score+=2
            reasons.append("符合颜色偏好")

        # TODO：季节评分
        # TODO：场景评分
        # TODO：颜色评分

        return score, reasons

    def recommend(
        self,
        clothes: list[Clothing],
        target_season: str,
        target_scene: str,
        preferred_color: str,
        limit: int = 3,
    ) -> list[tuple[Clothing, int, list[str]]]:
        """按照得分从高到低返回推荐结果。"""
        results = []

        for clothing in clothes:
            score, reasons = self.calculate_score(
            clothing,
            target_season,
            target_scene,
            preferred_color,
        )

            if score > 0:
                results.append((clothing, score, reasons))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]