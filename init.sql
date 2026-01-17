-- O banco 'gestor_financeiro' já foi criado pelo Compose, 
-- então criamos apenas o do Metabase:
CREATE DATABASE IF NOT EXISTS metabase_internal;

-- Garantimos que o usuário 'user' tenha acesso a TUDO 
-- (inclusive ao novo banco metabase_internal)
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';

FLUSH PRIVILEGES;