class PlayerDNA:
    def __init__(self, motion, isolation, transition, pnr_freq):
        self.motion = motion        # 모션 오펜스 이해도/성향
        self.isolation = isolation  # 아이솔레이션 선호도
        self.transition = transition # 트랜지션 가속도/참여도
        self.pnr_freq = pnr_freq    # 픽앤롤 전술 빈도/숙련도

class AdvancedPlayer:
    def __init__(self, name, primary_role, secondary_role, attributes, dna):
        self.name = name
        self.primary_role = primary_role
        self.secondary_role = secondary_role
        self.attributes = attributes  # {'Shooting', 'Passing', 'RimPressure', 'Defense'}
        self.dna = dna                # PlayerDNA 객체

class AdvancedLineup:
    def __init__(self, players):
        if len(players) != 5:
            raise ValueError("라인업은 반드시 5명의 선수로 구성되어야 합니다.")
        self.players = players

    def analyze_ball_dominance(self):
        """볼 점유율 오버랩을 분석하여 패널티 혹은 밸런스 점수를 계산합니다."""
        heavy_handlers = ["Main Handler", "Offensive Engine", "Isolation Scorer", "Secondary Handler"]
        handler_count = 0
        
        for p in self.players:
            if p.primary_role in heavy_handlers:
                handler_count += 1
                
        # 핸들러가 3명 이상이면 볼 배분 과부하 발생
        is_overloaded = handler_count >= 3
        return handler_count, is_overloaded

    def calculate_advanced_score(self):
        """DNA와 볼 밸런스, 슈팅 중력이 결합된 정밀 스탯을 도출합니다."""
        # 1. 기본 스탯 평균 및 DNA 데이터 집계
        base_shooting = sum(p.attributes['Shooting'] for p in self.players) / 5
        base_passing = sum(p.attributes['Passing'] for p in self.players) / 5
        base_rim = sum(p.attributes['RimPressure'] for p in self.players) / 5
        base_defense = sum(p.attributes['Defense'] for p in self.players) / 5
        
        team_transition_dna = sum(p.dna.transition for p in self.players) / 5

        # 2. 정교화 시스템 A: 슈팅 중력(Gravity Mapping) 보정
        # 슈팅 90점 이상의 초고급 슈터 한 명당 스페이싱 가중치 추가
        elite_shooters = sum(1 for p in self.players if p.attributes['Shooting'] >= 90)
        gravity_bonus = elite_shooters * 4

        # 3. 정교화 시스템 B: 볼 점유율 밸런싱(Ball Dominance)
        handler_count, is_overloaded = self.analyze_ball_dominance()
        penalty = 12 if is_overloaded else 0

        # 4. 최종 스탯 계산 (가중치 및 패널티 반영)
        final_spacing = min(round(base_shooting + gravity_bonus), 100)
        final_creation = max(round(base_passing - penalty), 10)  # 볼 배분 저하 반영
        final_rim = round(base_rim)
        final_defense = round(base_defense)
        
        # 속공 압박 지표 수치화 (수비력과 트랜지션 DNA의 조합)
        transition_pressure = min(round((base_defense * 0.4) + (team_transition_dna * 0.6)), 100)
        
        # 다재다능함 (패널티 반영)
        versatility = min(round(((final_spacing + final_creation + final_defense) / 3) - (penalty * 0.5)) + 5, 100)

        return {
            "metrics": {
                "Spacing Index": final_spacing,
                "Creation Load": final_creation,
                "Rim Pressure": final_rim,
                "Defensive Mobility": final_defense,
                "Transition Pressure": transition_pressure,
                "Versatility": versatility
            },
            "balance_report": {
                "handler_count": handler_count,
                "is_overloaded": is_overloaded,
                "elite_shooters_count": elite_shooters
            }
        }