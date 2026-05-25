import math

class Player:
    def __init__(self, name, primary_role, secondary_role, play_types, attributes):
        self.name = name
        self.primary_role = primary_role
        self.secondary_role = secondary_role
        self.play_types = play_types  # list of tags
        self.attributes = attributes  # dict: {'Shooting': 0~100, 'Passing': 0~100, 'RimPressure': 0~100, 'Defense': 0~100}

class Lineup:
    def __init__(self, players):
        if len(players) != 5:
            raise ValueError("라인업은 반드시 5명의 선수로 구성되어야 합니다.")
        self.players = players

    def analyze_metrics(self):
        """라인업의 5대 핵심 지표를 계산합니다."""
        total_shooting = sum(p.attributes.get('Shooting', 50) for p in self.players)
        total_passing = sum(p.attributes.get('Passing', 50) for p in self.players)
        total_rim = sum(p.attributes.get('RimPressure', 50) for p in self.players)
        total_defense = sum(p.attributes.get('Defense', 50) for p in self.players)
        
        # 단순 평균 계산 (실제 서비스 시 시너지 가중치 적용 가능)
        spacing_index = round(total_shooting / 5)
        creation_load = round(total_passing / 5)
        rim_pressure = round(total_rim / 5)
        defense_mobility = round(total_defense / 5)
        
        # 전반적인 다재다능함 (내부 지표 조합)
        versatility = round((spacing_index + creation_load + defense_mobility) / 3) + 5

        return {
            "Spacing Index": spacing_index,
            "Creation Load": creation_load,
            "Rim Pressure": rim_pressure,
            "Defensive Mobility": defense_mobility,
            "Versatility": min(versatility, 100)
        }

    def check_roles(self):
        """현재 라인업에 포함된 모든 역할(Primary + Secondary)의 집합을 반환합니다."""
        roles = set()
        for p in self.players:
            roles.add(p.primary_role)
            if p.secondary_role:
                roles.add(p.secondary_role)
        return roles


class TacticEngine:
    def __init__(self):
        # 전술별 필수 요구 역할 정의
        self.tactical_library = {
            "Spain PnR": {
                "required": ["Main Handler", "Rim Runner", "Movement Shooter"],
                "description": "핸들러의 PnR 스크린 이후 스크리너에게 백스크린을 거는 현대 농구 핵심 전술"
            },
            "Chicago Action": {
                "required": ["DHO Hub", "Movement Shooter", "Connector"],
                "description": "핀다운 스크린에 이은 핸드오프 패스로 슈터의 중력을 극대화하는 전술"
            },
            "Delay Motion": {
                "required": ["Post Hub", "Connector", "Spacer"],
                "description": "5-Out 형태에서 하이포스트/엘보의 빅맨을 거쳐 유기적으로 컷인하는 전술"
            },
            "Double Drag": {
                "required": ["Main Handler", "Screener", "Stretch Big"],
                "description": "트랜지션 상황에서 연속으로 두 개의 스크린을 활용해 찬스를 만드는 전술"
            }
        }

    def generate_recommendations(self, lineup):
        """라인업의 역할 구성과 전술 요구사항을 비교하여 적합도를 계산합니다."""
        available_roles = lineup.check_roles()
        recommendations = []

        for tactic_name, info in self.tactical_library.items():
            required_roles = info["required"]
            # 충족하는 역할 개수 계산
            matched_roles = [role for role in required_roles if role in available_roles]
            match_rate = len(matched_roles) / len(required_roles)
            match_percentage = round(match_rate * 100)

            # 충족도 기반 티어 매기기
            if match_percentage >= 90:
                tier = "S Tier"
            elif match_percentage >= 65:
                tier = "A Tier"
            else:
                tier = "B Tier"

            recommendations.append({
                "tactic": tactic_name,
                "tier": tier,
                "fit_score": f"{match_percentage}%",
                "description": info["description"]
            })

        # 티어 순으로 정렬 (S -> A -> B)
        recommendations.sort(key=lambda x: x["tier"])
        return recommendations


# =====================================================================
# 실행 테스트 코드 (시뮬레이션)
# =====================================================================
if __name__ == "__main__":
    print("🏀 HoopsOS Archetype Engine 가동... \n")

    # 1. 샘플 선수 데이터 생성 (요청하신 라인업 기반 정교화)
    players_pool = [
        Player("Tyrese Haliburton", "Main Handler", "Transition Initiator", ["PnR", "Pass-First"], {"Shooting": 88, "Passing": 98, "RimPressure": 70, "Defense": 65}),
        Player("Stephen Curry", "Movement Shooter", "Secondary Handler", ["Off-Ball", "Pull-Up"], {"Shooting": 99, "Passing": 85, "RimPressure": 75, "Defense": 70}),
        Player("Bam Adebayo", "Rim Runner", "DHO Hub", ["Screener", "Short-Roll"], {"Shooting": 60, "Passing": 80, "RimPressure": 88, "Defense": 95}),
        Player("Mikal Bridges", "Connector", "POA Defender", ["Catch-and-Shoot", "Cutter"], {"Shooting": 82, "Passing": 68, "RimPressure": 72, "Defense": 90}),
        Player("Michael Porter Jr.", "Spacer", "Corner Spacer", ["Catch-and-Shoot", "Size"], {"Shooting": 90, "Passing": 50, "RimPressure": 78, "Defense": 68})
    ]

    # 2. 라인업 구성
    my_lineup = Lineup(players_pool)
    
    # 3. 라인업 스탯 분석 결과 출력
    print("--- [1] 라인업 분석 지표 (Lineup Score) ---")
    metrics = my_lineup.analyze_metrics()
    for metric, score in metrics.items():
        print(f"🔹 {metric}: {score}")
    print("-" * 40 + "\n")

    # 4. 전술 추천 시스템 가동
    print("--- [2] AI 전술 자동 생성 엔진 결과 (Tactic Generator) ---")
    engine = TacticEngine()
    suggestions = engine.generate_recommendations(my_lineup)
    
    for sug in suggestions:
        print(f"[{sug['tier']}] {sug['tactic']} (적합도: {sug['fit_score']})")
        print(f" 💡 설명: {sug['description']}\n")