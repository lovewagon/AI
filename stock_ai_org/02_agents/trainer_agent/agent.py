import os
import importlib.util
import torch
from torch.utils.data import DataLoader, TensorDataset
import pytorch_lightning as pl
from pytorch_lightning.loggers import MLFlowLogger

class TrainerAgent:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.models_dir = os.path.join(base_dir, "03_models")
        # Docker-Composeで定義したMLflowサーバーのURL
        self.mlflow_tracking_uri = "http://localhost:5000"

    def _load_generated_model(self, model_type):
        """reproduce_agentが自律生成したmodel.pyを動的にインポート"""
        model_path = os.path.join(self.models_dir, model_type, "model.py")
        if not os.path.exists(model_path):
            print(f"[Error] Model file not found: {model_path}")
            return None
        
        spec = importlib.util.spec_from_file_location("dynamic_model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # モジュール内からLightningModuleを継承したクラスを自動探索
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, pl.LightningModule) and attr != pl.LightningModule:
                return attr
        return None

    def _prepare_mock_data(self):
        """04_data/processed からのデータ読み込みをシミュレートするダミーテンソル"""
        # (サンプル数, シーケンス長=20, 特徴量数=4)
        x_train = torch.randn(128, 20, 4)
        y_train = torch.randn(128, 1)
        dataset = TensorDataset(x_train, y_train)
        return DataLoader(dataset, batch_size=32, shuffle=True)

    def execute_training(self, model_type="transformer", epochs=3):
        """
        自律インポートしたモデルを、MLflowロギング環境下で自動学習
        """
        model_class = self._load_generated_model(model_type)
        if not model_class:
            print("[Error] 実行可能なモデルクラスが検出されませんでした。")
            return False

        print(f"[Train] {model_type} モデルの動的インスタンス化に成功。学習を開始します。")
        model = model_class()
        train_loader = self._prepare_mock_data()

        # MLflow Logger の紐付け設定 (Dockerコンテナ側へメトリクスを自動転送)
        mlf_logger = MLFlowLogger(
            experiment_name=f"stock_ai_{model_type}_automated",
            tracking_uri=self.mlflow_tracking_uri
        )

        # PyTorch Lightningによるワンストップトレーナーの起動
        trainer = pl.Trainer(
            max_epochs=epochs,
            logger=mlf_logger,
            enable_checkpointing=True,
            default_root_dir=os.path.join(self.base_dir, "01_research", "experiments")
        )

        try:
            trainer.fit(model, train_loader)
            print(f"[Success] MLflow Run UUID: {mlf_logger.run_id} に学習成果が記録されました。")
            return True
        except Exception as e:
            print(f"[Error] Training Failed: {e}")
            return False

if __name__ == "__main__":
    agent = TrainerAgent("C:\\Users\\User\\Desktop\\AI\\stock_ai_org")
    # 先ほど生成したtransformerのmodel.pyを自動ターゲットにしてテスト駆動
    agent.execute_training("transformer", epochs=2)
