import os
import sys

# エージェント群のディレクトリをPathに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "02_agents"))

# 各コンポーネントの自律モジュールをインポート
from paper_agent.agent import PaperAgent
from reader_agent.agent import ReaderAgent
from reproduce_agent.agent import ReproduceAgent
from trainer_agent.agent import TrainerAgent
from evaluator_agent.agent import EvaluatorAgent
from report_agent.agent import ReportAgent

# データパイプラインのインポート
sys.path.append(os.path.join(os.path.dirname(__file__), "04_data"))
from process_duckdb import DataPipeline

class StockAIOrchestrator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        print("\n====================================================")
        print("   Stock AI 完全自律循環パイプライン v1.1 - 起動")
        print("====================================================\n")

    def run_full_pipeline(self, paper_id="sample_paper_id", model_type="transformer"):
        print("====== [STAGE 1] 数据特徴量加工 (DuckDB層) ======")
        pipeline = DataPipeline(self.base_dir)
        if not pipeline.run_feature_engineering():
            print("[Abort] データパイプラインで異常が発生したため停止します。")
            return

        print("\n====== [STAGE 2] 論文自律クローリング (paper_agent) ======")
        paper_agent = PaperAgent(self.base_dir)
        paper_agent.run_pipeline()

        print("\n====== [STAGE 3] 論文解析・3行要約抽出 (reader_agent) ======")
        reader_agent = ReaderAgent(self.base_dir)
        if not reader_agent.generate_summary(paper_id):
            print("[Abort] 論文解析に失敗したため停止します。")
            return

        print("\n====== [STAGE 4] 数理スペック再現・コード生成 (reproduce_agent) ======")
        reproduce_agent = ReproduceAgent(self.base_dir)
        if not reproduce_agent.generate_pytorch_model(paper_id, model_type):
            print("[Abort] PyTorchコードの自律生成に失敗しました。")
            return

        print("\n====== [STAGE 5] 自律モデル学習＆MLflowロギング (trainer_agent) ======")
        trainer_agent = TrainerAgent(self.base_dir)
        trainer_agent.execute_training(model_type, epochs=1)

        print("\n====== [STAGE 6] バックテスト・運用品質ゲート判定 (evaluator_agent) ======")
        evaluator_agent = EvaluatorAgent(self.base_dir, sharpe_threshold=1.5)
        is_approved = evaluator_agent.evaluate_performance(model_type)

        print("\n====== [STAGE 7] プロ提案書レベル・レポートパブリッシュ (report_agent) ======")
        report_agent = ReportAgent(self.base_dir)
        report_agent.generate_pro_report()

        print("\n====================================================")
        print(" 🟢 パイプライン全行程の自律実行が正常に完了しました。")
        if is_approved:
            print(" 【最終ステータス】: 運用基準クリア ➔ デプロイ可")
        else:
            print(" 【最終ステータス】: 運用基準未達 ➔ 再チューニング対象")
        print("====================================================\n")

if __name__ == "__main__":
    root_dir = "C:\\Users\\User\\Desktop\\AI\\stock_ai_org"
    orchestrator = StockAIOrchestrator(root_dir)
    orchestrator.run_full_pipeline()