class Player:
    def __init__(self, name, primary_role, secondary_role):
        self.name = name
        self.primary_role = primary_role
        self.secondary_role = secondary_role

class Lineup:
    def __init__(self, players):
        if len(players) != 5:
            raise ValueError("라인업은 반드시 5명의 선수로 구성되어야 합니다.")
        self.players = players

    def get_available_roles(self):
        """라인업에 포함된 모든 역할(Primary + Secondary)을 추출합니다."""
        roles = set()
        for p in self.players:
            roles.add(p.primary_role)
            if p.secondary_role:
                roles.add(p.secondary_role)
        return roles

class AITacticGenerator:
    def __init__(self):
        # [기획서 기반 전술 패밀리 트리 데이터베이스]
        self.tactic_database = {
            "Spain PnR": {
                "family": "Ball Screen Family",
                "required_roles": ["Main Handler", "Rim Runner", "Movement Shooter"],
                "desc": "핸들러, 롤맨, 그리고 스크리너에게 백스크린을 거는 슈터의 삼각 공조 전술"
            },
            "Chicago Action": {
                "family": "Motion Family",
                "required_roles": ["DHO Hub", "Movement Shooter", "Connector"],
                "desc": "핀다운 스크린을 받은 슈터가 이어서 핸드오프(DHO)를 받아 외곽을 파괴하는 전술"
            },
            "Delay Motion": {
                "family": "Motion Family",
                "required_roles": ["Post Hub", "Connector", "Spacer"],
                "desc": "5-Out 형태에서 하이포스트 빅맨을 허브로 삼아 유기적인 컷인과 패싱을 도출하는 전술"
            },
            "Double Drag": {
                "family": "Ball Screen Family",
                "required_roles": ["Main Handler", "Screener", "Stretch Big"],
                "desc": "트랜지션 상황에서 시간차로 들어오는 연속 스크린을 활용해 찬스를 만드는 전술"
            }
        }

    def generate_tactics(self, lineup):
        """현재 라인업의 역할 충족률을 계산하여 맞춤형 전술 플레이북을 생성합니다."""
        lineup_roles = lineup.get_available_roles()
        playbook = []

        for tactic_name, info in self.tactic_database.items():
            required = info["required_roles"]
            
            # 라인업이 만족하는 역할 교집합 찾기
            matched = [role for role in required if role in lineup_roles]
            
            # 충족률 계산 (100% 만점 환산)
            match_rate = len(matched) / len(required)
            match_percentage = round(match_rate * 100)

            # 충족도 기반 티어링(Tiering)
            if match_percentage >= 90:
                tier = "S Tier"
            elif match_percentage >= 70:
                tier = "A Tier"
            else:
                tier = "B Tier"

            playbook.append({
                "tactic": tactic_name,
                "family": info["family"],
                "match_rate": match_percentage,
                "tier": tier,
                "desc": info["desc"],
                "missing_roles": [r for r in required if r not in lineup_roles]
            })

        # 높은 티어와 높은 충족률 순으로 정렬
        playbook.sort(key=lambda x: (x["tier"], -x["match_rate"]))
        return playbook


# =====================================================================
# 실행 테스트 (시뮬레이션)
# =====================================================================
if __name__ == "__main__":
    print("🏀 HoopsOS - AI Tactic Generator 엔진 가동... \n")

    # 1. 기획서 6번에 등장한 혁신적인 입력 라인업 그대로 재현
    input_players = [
        Player("Tyrese Haliburton", "Main Handler", "Transition Initiator"),
        Player("Stephen Curry", "Movement Shooter", "Secondary Handler"),
        Player("Bam Adebayo", "Rim Runner", "DHO Hub"),
        Player("Mikal Bridges", "Connector", "POA Defender"),
        Player("Michael Porter Jr.", "Spacer", "Corner Spacer")
    ]

    # 2. 라인업 객체 및 생성기 생성
    my_lineup = Lineup(input_players)
    generator = AITacticGenerator()

    # 3. 전술 추천 리포트 출력
    recommended_playbook = generator.generate_tactics(my_lineup)

    print("📋 [현재 라인업 기반 추천 전술 플레이북]")
    print(f"👉 입력 라인업 구성원: {[p.name for p in input_players]}\n")
    print("-" * 60)

    for play in recommended_playbook:
        print(f"[{play['tier']}] {play['tactic']} (적합도: {play['match_rate']}% | 카테고리: {play['family']})")
        print(f" 💡 핵심 설명: {play['desc']}")
        
        # 만약 부족한 역할이 있다면 팁으로 출력
        if play['missing_roles']:
            print(f" ⚠️ 필요 보완 역할: {play['missing_roles']}")
        else:
            print(" ✅ 전술 수행 조건 100% 충족!")
        print("-" * 60)