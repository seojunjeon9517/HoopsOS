class Player:
    def __init__(self, name, primary_role, secondary_role, attributes):
        self.name = name
        self.primary_role = primary_role
        self.secondary_role = secondary_role
        self.attributes = attributes  # {'Shooting': 0~100, 'Passing': 0~100, 'RimPressure': 0~100, 'Defense': 0~100}

class SystemFitMatrix:
    def __init__(self):
        # [전술 시스템별 정밀 요구사항 정의]
        self.systems = {
            "Motion System": {
                "key_roles": ["Movement Shooter", "Connector", "Secondary Handler", "Offensive Engine"],
                "primary_stat": "Passing",
                "desc": "유기적인 패싱과 끊임없는 오프볼 움직임을 강조하는 시스템"
            },
            "Drop Coverage": {
                "key_roles": ["Rim Protector", "Rim Runner", "Screen Navigator"],
                "primary_stat": "Defense",
                "desc": "빅맨이 골밑을 지키고 핸들러가 뒤를 쫓는 전통적인 스크린 수비 시스템"
            },
            "5-Out System": {
                "key_roles": ["Spacer", "Stretch Big", "Movement Shooter"],
                "primary_stat": "Shooting",
                "desc": "5명의 선수 전원이 외곽에 배치되어 공간을 극대화하는 양궁 농구 시스템"
            },
            "Switch-All": {
                "key_roles": ["POA Defender", "Switch Big", "Glue Guy"],
                "primary_stat": "Defense",
                "desc": "모든 스크린 상황에서 매치업을 바꾸어 미스매치를 제어하는 기동성 중심 수비"
            }
        }

    def _convert_score_to_tier(self, score):
        """점수를 기반으로 직관적인 알파벳 티어를 반환합니다."""
        if score >= 96: return "S+"
        elif score >= 88: return "S"
        elif score >= 80: return "A"
        elif score >= 70: return "B"
        else: return "C"

    def calculate_fit(self, player):
        """선수의 역할과 스탯을 분석하여 각 시스템별 적합도와 티어를 계산합니다."""
        fit_results = {}

        for system_name, requirements in self.systems.items():
            base_score = 50  # 기본 점수 시작
            
            # 1. 역할 적합도 검증 (Primary 매칭 시 +25, Secondary 매칭 시 +15)
            if player.primary_role in requirements["key_roles"]:
                base_score += 25
            if player.secondary_role in requirements["key_roles"]:
                base_score += 15
                
            # 2. 능력치 가중치 검증 (핵심 능력치의 20%를 점수에 반영)
            target_stat = requirements["primary_stat"]
            stat_value = player.attributes.get(target_stat, 50)
            base_score += (stat_value * 0.2)

            # 최종 점수 보정 (최대 100점 제한)
            final_score = min(round(base_score), 100)
            tier = self._convert_score_to_tier(final_score)

            fit_results[system_name] = {
                "score": final_score,
                "tier": tier
            }

        return fit_results


# =====================================================================
# 실행 테스트 (시뮬레이션)
# =====================================================================
if __name__ == "__main__":
    print("🏀 HoopsOS - System Fit Matrix Engine 가동...\n")

    # 기획서 예시 선수 생성
    curry = Player(
        "Stephen Curry", 
        "Movement Shooter", 
        "Secondary Handler", 
        {"Shooting": 99, "Passing": 90, "RimPressure": 75, "Defense": 70}
    )

    gobert = Player(
        "Rudy Gobert", 
        "Rim Protector", 
        "Rim Runner", 
        {"Shooting": 30, "Passing": 55, "RimPressure": 85, "Defense": 98}
    )

    engine = SystemFitMatrix()

    # 선수별 적합도 출력 자동화 함수
    for player in [curry, gobert]:
        print(f"👤 [선수 프로필 분석] {player.name}")
        print(f" ▫️ 주 역할: {player.primary_role} | 부 역할: {player.secondary_role}")
        print(f" ▫️ 주요 스탯: {player.attributes}\n")
        
        print(f" ⚡ [시스템 전술 적합도 결과]")
        analysis = engine.calculate_fit(player)
        for sys_name, res in analysis.items():
            print(f"   ▶ {sys_name.ljust(15)} : 점수 {str(res['score']).rjust(3)}점 [{res['tier']}]")
        print("\n" + "="*50 + "\n")