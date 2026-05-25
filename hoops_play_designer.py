from hoops_advanced_engine import AdvancedPlayer, PlayerDNA

class TacticalAction:
    def __init__(self, action_type, actor_name, target_name=None):
        self.action_type = action_type  # Screen, Cut, Slip, DHO, Relocate, Hammer
        self.actor_name = actor_name    # 행동을 수행하는 선수 이름
        self.target_name = target_name  # 행동의 대상이 되는 선수 이름 (필요 시)

class PlayDesign:
    def __init__(self, play_name):
        self.play_name = play_name
        self.sequence = []  # 유저가 조립한 전술 액션들의 순서 배열

    def add_action(self, action):
        """작전 보드 UI에서 드래그 앤 드롭으로 액션을 추가하는 과정을 시뮬레이션합니다."""
        self.sequence.append(action)

    def validate_and_simulate(self, lineup_players):
        """디자인된 전술 시퀀스를 현재 라인업이 실행했을 때의 성공률과 가치를 계산합니다."""
        # 선수 이름으로 객체를 빠르게 찾기 위한 딕셔너리 생성
        player_map = {p.name: p for p in lineup_players}
        
        total_difficulty = len(self.sequence) * 15  # 액션이 많아질수록 기본 난이도 상승
        execution_power = 0
        log_messages = []

        for idx, act in enumerate(self.sequence, 1):
            actor = player_map.get(act.actor_name)
            if not actor:
                return {"status": "오류", "message": f"라인업에 {act.actor_name} 선수가 없습니다."}

            # [액션 유형별 정밀 검증 로직]
            if act.action_type == "Screen":
                # 스크리너의 Rim Pressure(신체 조건)와 PnR DNA 반영
                score = (actor.attributes['RimPressure'] * 0.6) + (actor.dna.pnr_freq * 0.4)
                execution_power += score
                log_messages.append(f"Step {idx}: {actor.name}의 스크린 시도 (역량: {round(score)}점)")

            elif act.action_type == "DHO":
                # 핸드오프 패서의 Passing 능력과 Motion DNA 반영
                score = (actor.attributes['Passing'] * 0.5) + (actor.dna.motion * 0.5)
                execution_power += score
                log_messages.append(f"Step {idx}: {actor.name}의 핸드오프 패스 전달 (역량: {round(score)}점)")

            elif act.action_type == "Cut":
                # 컷인 플레이어의 Rim Pressure와 Transition(기동성) DNA 반영
                score = (actor.attributes['RimPressure'] * 0.4) + (actor.dna.transition * 0.6)
                execution_power += score
                log_messages.append(f"Step {idx}: {actor.name}의 빈 공간 컷인 슬래싱 (역량: {round(score)}점)")

            elif act.action_type == "Relocate":
                # 재배치 슈터의 Shooting 능력과 Motion DNA 반영
                score = (actor.attributes['Shooting'] * 0.7) + (actor.dna.motion * 0.3)
                execution_power += score
                log_messages.append(f"Step {idx}: {actor.name}의 외곽 공간 재배치 (역량: {round(score)}점)")

            else:
                # 기타 액션 기본 처리
                execution_power += 75
                log_messages.append(f"Step {idx}: {actor.name}의 {act.action_type} 액션 수행")

        # 최종 성공 확률 계산 (최대 95%, 최소 20%)
        average_power = execution_power / len(self.sequence)
        success_rate = min(max(round(average_power - (total_difficulty * 0.1)), 20), 95)

        return {
            "status": "성공",
            "play_name": self.play_name,
            "success_rate": f"{success_rate}%",
            "execution_log": log_messages
        }


# =====================================================================
# 작전 보드 플레이 디자인 시뮬레이션 실행
# =====================================================================
if __name__ == "__main__":
    print("🏀 HoopsOS - Play Design Sequence Engine 가동...\n")

    # 1. 시뮬레이션용 골든스테이트 워리어스 타입 라인업 구성
    gsw_squad = [
        AdvancedPlayer("Stephen Curry", "Movement Shooter", "Secondary Handler", {"Shooting": 99, "Passing": 90, "RimPressure": 75, "Defense": 70}, PlayerDNA(98, 75, 90, 85)),
        AdvancedPlayer("Draymond Green", "Connector", "Switch Big", {"Shooting": 65, "Passing": 88, "RimPressure": 70, "Defense": 92}, PlayerDNA(95, 40, 85, 90)),
        AdvancedPlayer("Klay Thompson", "Movement Shooter", "POA Defender", {"Shooting": 88, "Passing": 65, "RimPressure": 60, "Defense": 80}, PlayerDNA(90, 50, 75, 60)),
        AdvancedPlayer("Andrew Wiggins", "Connector", "POA Defender", {"Shooting": 80, "Passing": 60, "RimPressure": 85, "Defense": 85}, PlayerDNA(75, 70, 88, 65)),
        AdvancedPlayer("Kevon Looney", "Screener", "Rim Runner", {"Shooting": 20, "Passing": 65, "RimPressure": 75, "Defense": 82}, PlayerDNA(80, 10, 50, 88))
    ]

    # 2. 유저가 작전 보드 UI에서 드래그앤드롭으로 전술을 직접 디자인하는 상황 연출
    print("🛠️ [UI 시뮬레이션] 유저가 '스플릿 액션(Split Action) 파생 전술'을 조립 중...")
    custom_play = PlayDesign("Curry-Green Top Split Play")
    
    # 드래그 앤 드롭 순서대로 액션 등록
    custom_play.add_action(TacticalAction("Screen", "Kevon Looney", "Stephen Curry")) # 루니가 커리에게 스크린
    custom_play.add_action(TacticalAction("DHO", "Draymond Green", "Stephen Curry"))   # 그린이 커리에게 핸드오프 패스
    custom_play.add_action(TacticalAction("Relocate", "Stephen Curry"))               # 커리가 외곽으로 재배치(팝아웃)
    custom_play.add_action(TacticalAction("Cut", "Andrew Wiggins"))                  # 그 사이 위긴스가 골밑 빈틈으로 컷인
    
    # 3. 디자인한 작전 시뮬레이션 검증 가동
    report = custom_play.validate_and_simulate(gsw_squad)

    print("\n📋 [플레이 디자인 실행 보고서]")
    print(f" ▪️ 작전명: {report['play_name']}")
    print(f" ▪️ 예측 전술 성공률: {report['success_rate']}")
    print("\n 상세 타임라인 액션 로그:")
    for log in report['execution_log']:
        print(f"   {log}")