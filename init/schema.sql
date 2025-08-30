CREATE TABLE IF NOT EXISTS 'requisicoes' (
    "id" TEXT NOT NULL PRIMARY KEY,
    "setor" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "comments" TEXT,
    "priority" INTEGER NOT NULL,
    "status" TEXT NOT NULL,
    "data_emissao" DATE NOT NULL,
    "data_conclusao" DATE,
    "nome_requisitante" TEXT NOT NULL,
    "servicos" TEXT
)

