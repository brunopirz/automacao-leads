CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255),
    telefone VARCHAR(50),
    origem VARCHAR(100),
    interesse VARCHAR(255),
    renda_aproximada INTEGER,
    cidade VARCHAR(100),
    status VARCHAR(50) DEFAULT 'novo',
    score INTEGER DEFAULT 0,
    raw_payload TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);