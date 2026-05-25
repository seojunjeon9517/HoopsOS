from hoops_synergy_engine import Player, Lineup
from hoops_system_fit import SystemFitMatrix
from hoops_tactic_generator import AITacticGenerator

class HoopsDashboard:
    def __init__(self):
        self.fit_matrix_engine = SystemFitMatrix()
        self.tactic_generator_engine = AITacticGenerator()

    def generate_team_report(self, players):
        """5인의 라인업을 분석하여 통합 대시보드 리포트를 생성합니다."""
        # 1. 라인업 생성 및 시너지/기본 스탯 계산
        lineup = Lineup(players)
        score_data = lineup.calculate_final_score()
        
        metrics = score_data["metrics"]
        synergies = score_data["synergies"]

        # 2. 전술 자동 생성 결과 가져오기
        playbook = self.tactic_generator_engine.generate_tactics(lineup)

        # 3. 개별 선수별 시스템 적합도 결과 종합
        player_fits = {}
        for p in players:
            player_fits[p.name] = self.fit_matrix_engine.calculate_fit(p)

        # 리포트 데이터 반환
        return {
            "metrics": metrics,
            "synergies": synergies,
            "playbook": playbook,
            "player_fits": player_fits
        }

    def display_dashboard(self, players):
        """콘솔 창에 깔끔하고 직관적인 대시보드 UI를 출력합니다."""
        report = self.generate_team_report(players)
        
        print("=" * 65)
        print("🏀  HoopsOS - 하이브리드 농구 전술 통합 대시보드  🏀")
        print("=" * 65)
        
        # 1. 현재 라인업 명단
        print("\n[1] ACTIVE LINEUP ARCHITECTURE")
        for i, p in enumerate(players, 1):
            print(f" 🏃 {i}. {p.name.ljust(22)} | Primary: {p.primary_role.ljust(18)} | Secondary: {p.secondary_role}")
        
        # 2. 라인업 핵심 지표 (시너지 보정 완료)
        print("\n" + "-"*65)
        print("[2] LINEUP CORE METRICS (Synergy Adjusted)")
        for metric, score in report["metrics"].items():
            # 점수에 따른 시각 인디케이터 (간이 게이지 바)
            bar = "■" * (score // 10) + "□" * (10 - (score // 10))
            print(f" 🟩 {metric.ljust(20)}: {str(score).rjust(3)} 점 | [{bar}]")

        # 3. 발동된 역할 시너지 효과
        print("\n" + "-"*65)
        print("[3] ACTIVATED ROLE SYNERGIES")
        if not report["synergies"]:
            print(" ⚠️ 현재 조합에서 발동된 특수 시너지 효과가 없습니다.")
        else:
            for syn in report["synergies"]:
                print(f" ✅ {syn['name']} -> {syn['effect']}")

        # 4. AI 추천 전술 플레이북
        print("\n" + "-"*65)
        print("[4] AI RECOMMENDED PLAYBOOK (Tactical Family)")
        for play in report["playbook"]:
            missing_info = f" (보완 필요: {play['missing_roles']})" if play['missing_roles'] else " (READY)"
            print(f"  • [{play['tier']}] {play['tactic'].ljust(15)} | 적합도: {str(play['match_rate']).rjust(3)}%{missing_info}")

        # 5. 선수별 시스템 적합도 요약
        print("\n" + "-"*65)
        print("[5] INDIVIDUAL SYSTEM FIT MATRIX")
        for name, fits in report["player_fits"].items():
            fit_summary = ", ".join([f"{sys[:10]}: {data['tier']}" for sys, data in fits.items()])
            print(f" 👤 {name.ljust(22)} ➡️  {fit_summary}")
        
        print("=" * 65)


# =====================================================================
# 대시보드 실행 테스트 (시뮬레이션)
# =====================================================================
if __name__ == "__main__":
    # 검증용 베스트 라인업 세팅 (할리버튼, 커리, 아데바요, 브릿지스, MPJ)
    squad = [
        Player("Tyrese Haliburton", "Main Handler", "Transition Initiator", {"Shooting": 88, "Passing": 98, "RimPressure": 70, "Defense": 65}),
        Player("Stephen Curry", "Movement Shooter", "Secondary Handler", {"Shooting": 99, "Passing": 90, "RimPressure": 75, "Defense": 70}),
        Player("Bam Adebayo", "Rim Runner", "DHO Hub", {"Shooting": 60, "Passing": 80, "RimPressure": 88, "Defense": 95}),
        Player("Mikal Bridges", "Connector", "POA Defender", {"Shooting": 82, "Passing": 68, "RimPressure": 72, "Defense": 90}),
        Player("Michael Porter Jr.", "Spacer", "Corner Spacer", {"Shooting": 90, "Passing": 50, "RimPressure": 75, "Defense": 68})
    ]

    dashboard = HoopsDashboard()
    dashboard.display_dashboard(squad)