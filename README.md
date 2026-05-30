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


