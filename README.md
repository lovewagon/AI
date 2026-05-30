Stock AI Org 📈

arXiv 論文クローリング → PyTorch モデル自律生成 → バックテスト → プロ提案書レポート → デプロイ判定
完全自律循環パイプライン v1.1


概要
stock_ai_org は、株価予測AIの研究・開発・評価・レポート生成をゼロヒューマン介入で一周する自律エージェントシステムです。
最新の arXiv 論文を自動収集し、モデル設計・学習・バックテストを経て、シャープレシオによる運用可否判定まで自動化します。
[STAGE 1] DuckDB 特徴量加工
    ↓
[STAGE 2] paper_agent      arXiv 論文クローリング & PDF 保存
    ↓
[STAGE 3] reader_agent     論文解析・3行要約生成
    ↓
[STAGE 4] reproduce_agent  数理スペック再現・PyTorch コード自動生成
    ↓
[STAGE 5] trainer_agent    モデル学習 + MLflow ロギング
    ↓
[STAGE 6] evaluator_agent  バックテスト・シャープ比ゲート判定（閾値 1.5）
    ↓
[STAGE 7] report_agent     プロ提案書レベルのレポート自律生成

ディレクトリ構成
stock_ai_org/
├── main.py                  # オーケストレーター（全7ステージを順次実行）
├── requirements.txt
├── 01_research/
│   └── papers/pdf/          # arXiv PDFの自律保存先
├── 02_agents/
│   ├── paper_agent/         # arXiv クローリング・PDF ダウンロード
│   ├── reader_agent/        # 論文解析・要約抽出
│   ├── reproduce_agent/     # PyTorch モデルコード生成
│   ├── trainer_agent/       # モデル学習・MLflow ロギング
│   ├── evaluator_agent/     # バックテスト・デプロイ可否判定
│   └── report_agent/        # プロ提案書生成
├── 03_models/               # 学習済みモデル (.pt / .ckpt)
├── 04_data/
│   └── process_duckdb.py    # DuckDB 特徴量エンジニアリング
├── 05_backtest/             # バックテストエンジン・結果
├── 06_reports/              # 自律生成レポート出力先
├── 07_deploy/               # 本番デプロイ設定
└── 08_infra/                # インフラ・環境設定

セットアップ
必要要件

Python 3.10+
CUDA 対応 GPU（推奨）または CPU

インストール
bashgit clone https://github.com/lovewagon/AI.git
cd AI/stock_ai_org
pip install -r requirements.txt
依存パッケージ
パッケージ用途torch >= 2.0モデル学習・推論pytorch-lightning >= 2.0学習ループ管理transformers >= 4.30事前学習モデル活用mlflow >= 2.10実験管理・ロギングduckdb >= 0.9特徴量エンジニアリングfastapi / uvicorn論文メタデータ管理 APIboto3AWS S3 モデル保存

実行方法
bash# Windows (PowerShell)
./start.ps1

# または直接実行
python main.py
main.py 末尾の root_dir をご自身の環境パスに合わせて変更してください：
pythonif __name__ == "__main__":
    root_dir = "/path/to/stock_ai_org"   # ← 変更
    orchestrator = StockAIOrchestrator(root_dir)
    orchestrator.run_full_pipeline()

エージェント詳細
paper_agent — 論文クローリング

arXiv API（export.arxiv.org）から stock price prediction 関連論文を自動検索
PDF を 01_research/papers/pdf/ へ自律ダウンロード
FastAPI エンドポイント（/api/v1/research/register）へメタデータ登録

reader_agent — 論文解析・要約

収集論文を解析し、3行サマリーを生成
以降のステージへの入力として構造化データを提供

reproduce_agent — コード生成

論文の数理仕様を読み取り、PyTorch モデルコードを自律生成
Transformer / LSTM / その他アーキテクチャに対応

trainer_agent — モデル学習

PyTorch Lightning による学習ループ管理
MLflow で実験パラメータ・メトリクス・モデルを自動ロギング

evaluator_agent — パフォーマンス評価
評価メトリクス:
  - 累積リターン
  - 年率シャープレシオ（日次 × √252）
  - 最大ドローダウン（MaxDD）

デプロイ判定:
  シャープレシオ ≥ 1.5 → 🟢 APPROVED（07_deploy へ移行）
  シャープレシオ < 1.5 → 🔴 REJECTED（reproduce_agent で再設計）
評価レポートは 06_reports/evaluation_{model_type}.txt に自動保存されます。
report_agent — レポート生成

全ステージの結果をプロ提案書レベルの形式で 06_reports/ へ出力


パイプライン実行フロー
pythonorchestrator.run_full_pipeline(
    paper_id="2401.12345",    # arXiv paper ID（省略可: "sample_paper_id"）
    model_type="transformer"  # "transformer" | "lstm" | etc.
)

MLflow トラッキング
bashmlflow ui
# → http://127.0.0.1:5000 でダッシュボード表示

ロードマップ

 reader_agent への Claude API 統合（論文要約の精度向上）
 reproduce_agent への Codex / Claude Code 連携
 リアルタイム株価データ（yfinance / Alpha Vantage）の DuckDB 取り込み
 Docker Compose による環境一発構築
 GitHub Actions CI（テスト + MLflow 自動実行）
 07_deploy への FastAPI サービス化


ライセンス
MIT

自律循環パイプライン — 論文から運用判定まで、ノーヒューマン
