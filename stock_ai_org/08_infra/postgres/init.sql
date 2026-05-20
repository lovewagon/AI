CREATE TABLE research_papers (
    paper_id VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    published_date DATE,
    arxiv_url TEXT,
    category VARCHAR(50),
    summary_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE experiment_runs (
    run_id VARCHAR(50) PRIMARY KEY,
    paper_id VARCHAR(50) REFERENCES research_papers(paper_id),
    model_name VARCHAR(50) NOT NULL,
    mlflow_run_uuid VARCHAR(100),
    reproduction_score FLOAT,
    status VARCHAR(20),
    error_log TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trading_signals (
    signal_id SERIAL PRIMARY KEY,
    run_id VARCHAR(50) REFERENCES experiment_runs(run_id),
    ticker VARCHAR(20) NOT NULL,
    signal_type VARCHAR(10) NOT NULL,
    target_price NUMERIC(12, 2),
    confidence_score FLOAT,
    executed_status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE market_features (
    timestamp TIMESTAMP NOT NULL,
    ticker VARCHAR(20) NOT NULL,
    close_price NUMERIC(12, 2),
    volume BIGINT,
    returns_1d FLOAT,
    volatility_5d FLOAT,
    ma_cross_indicator INT,
    llm_sentiment_score FLOAT,
    PRIMARY KEY (timestamp, ticker)
);
