import os

class ReportAgent:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.reports_dir = os.path.join(base_dir, "06_reports")
        self.eval_report_path = os.path.join(self.reports_dir, "evaluation_transformer.txt")

    def _read_eval_status(self):
        if not os.path.exists(self.eval_report_path): return "No data"
        with open(self.eval_report_path, "r", encoding="utf-8") as f: return f.read()

    def generate_pro_report(self):
        print("[Report] Generating report...")
        eval_raw = self._read_eval_status()
        pro_markdown = f"""# 【異次元のα】Dual-Stream Transformer報告\n\n> **【SNSフック】**\n> 「まだ従来のLSTMで消耗してるの？」\n> 成果をここに公開。\n\n## Executive Summary\nプロ提案書レベルのレポート。\n\n```text\n{eval_raw}\n```"""
        target_path = os.path.join(self.reports_dir, "final_pro_report.md")
        try:
            os.makedirs(self.reports_dir, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f: f.write(pro_markdown)
            print(f"[Success] {target_path}")
            return True
        except Exception as e: print(e); return False

if __name__ == "__main__":
    agent = ReportAgent("C:\\Users\\User\\Desktop\\AI\\stock_ai_org")
    agent.generate_pro_report()