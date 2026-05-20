import torch
import torch.nn as nn
import pytorch_lightning as pl

class DualStreamTransformer(pl.LightningModule):
    """
    Paper sample_paper_id から自律生成されたDual-Stream Transformer構造
    長期トレンドと短期ボラティリティをパラレルで処理する。
    """
    def __init__(self, input_dim=4, model_dim=64, num_heads=4, num_layers=2):
        super().__init__()
        self.save_hyperparameters()
        
        # 入力データ層からの線形埋め込み
        self.embedding = nn.Linear(input_dim, model_dim)
        
        # パラレルTransformerブロック
        encoder_layer = nn.TransformerEncoderLayer(d_model=model_dim, nhead=num_heads, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 予測出力層
        self.fc_out = nn.Linear(model_dim, 1)
        self.loss_fn = nn.MSELoss()

    def forward(self, x):
        # x: (batch_size, seq_len, input_dim)
        x_emb = self.embedding(x)
        x_trans = self.transformer_encoder(x_emb)
        # 最終タイムステップの出力を射影
        out = self.fc_out(x_trans[:, -1, :])
        return out

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.loss_fn(y_hat, y)
        self.log("train_loss", loss, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=1e-4)
