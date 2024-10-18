# Analise e limpeza de arquivos duplicados

**Limpeza de Duplicatas** é um script Python eficiente e versátil desenvolvido para identificar e remover arquivos duplicados em pastas, incluindo imagens e outros tipos de arquivos. O script utiliza técnicas avançadas de hashing para detectar duplicatas, mantendo apenas a versão de melhor qualidade de cada conjunto de arquivos duplicados. Além disso, oferece funcionalidades adicionais como mover duplicatas para uma pasta específica, registrar operações em logs e executar simulações antes de realizar ações reais.

## 📋 Características

- **Detecção de Duplicatas:**
  - **Imagens:** Utiliza hashes perceptuais para identificar imagens visualmente semelhantes, mesmo com pequenas diferenças.
  - **Outros Arquivos:** Utiliza hashes SHA256 para identificar arquivos exatamente iguais.
  
- **Seleção da Melhor Versão:**
  - Mantém o arquivo de maior tamanho, presumindo-se que possua melhor qualidade ou mais informações.

- **Suporte a Diversos Tipos de Arquivos:**
  - Detecta e remove duplicatas de vários formatos, incluindo imagens (`.jpg`, `.png`, `.heic`, etc.), documentos (`.pdf`, `.docx`, `.xlsx`, `.txt`) e outros.

- **Modo de Simulação (Dry Run):**
  - Permite verificar quais arquivos seriam removidos ou movidos sem executar a deleção real.

- **Log de Operações:**
  - Gera um arquivo de log detalhando as ações realizadas, facilitando a revisão e auditoria.

- **Interface de Linha de Comando (CLI) Amigável:**
  - Utiliza `argparse` para facilitar a configuração e execução do script com diferentes opções.

## 🛠️ Requisitos

- **Python 3.6+** instalado no sistema.
- **Bibliotecas Python:**
  - `Pillow`
  - `imagehash`
  
  Essas bibliotecas podem ser instaladas via `pip`:
  ```bash
  pip install Pillow imagehash
  ```
  
- **Permissões Adequadas:**
  - Permissões para ler os arquivos nas pastas de origem e escrever/remover arquivos nas pastas de destino.

## 💾 Instalação

1. **Verifique a Instalação do Python:**

   Abra o terminal (macOS/Linux) ou o Prompt de Comando (Windows) e execute:
   ```bash
   python --version
   ```
   ou
   ```bash
   python3 --version
   ```
   Se Python não estiver instalado, baixe e instale a partir do [site oficial do Python](https://www.python.org/downloads/).

2. **Instale as Dependências:**

   Instale as bibliotecas necessárias usando `pip`:
   ```bash
   pip install Pillow imagehash
   ```
   ou, se estiver usando Python 3:
   ```bash
   pip3 install Pillow imagehash
   ```

3. **Baixe o Script:**

   Crie um arquivo chamado `limpeza_duplicatas.py` e copie o código do script fornecido anteriormente para esse arquivo.

## 🚀 Uso

### 📝 Sintaxe Básica

```bash
python limpeza_duplicatas.py /caminho/para/sua/pasta [opções]
```

ou, se `python3` for necessário no seu sistema:

```bash
python3 limpeza_duplicatas.py /caminho/para/sua/pasta [opções]
```

### 🛠️ Opções de Linha de Comando

- **`-m`, `--mover`**
  - **Descrição:** Move os arquivos duplicados para uma pasta chamada `duplicatas` dentro do diretório especificado, ao invés de removê-los.
  - **Exemplo:** `--mover`

- **`-t`, `--tipos_imagem`**
  - **Descrição:** Especifica as extensões de arquivos de imagem a serem processados.
  - **Padrão:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.heic`
  - **Exemplo:** `--tipos_imagem .jpg .png .gif`

- **`-o`, `--outros_tipos`**
  - **Descrição:** Especifica as extensões de outros tipos de arquivos a serem processados.
  - **Padrão:** `.pdf`, `.docx`, `.xlsx`, `.txt`
  - **Exemplo:** `--outros_tipos .pdf .docx`

- **`-l`, `--log`**
  - **Descrição:** Caminho para o arquivo de log. Se não for especificado, usa `limpeza_duplicatas.log` no diretório especificado.
  - **Exemplo:** `--log "/caminho/para/meu_log.log"`

- **`-d`, `--dry_run`**
  - **Descrição:** Executa o script em modo de simulação, listando quais arquivos seriam removidos/movidos sem executar a ação real.
  - **Exemplo:** `--dry_run`

- **`-v`, `--verbose`**
  - **Descrição:** Exibe informações detalhadas durante a execução do script.
  - **Exemplo:** `--verbose`

### 📂 Exemplos de Comando

1. **Executar uma Limpeza Básica:**

   Remove duplicatas de imagens e outros tipos de arquivos no diretório especificado:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta"
   ```

2. **Executar em Modo de Simulação:**

   Verifica quais arquivos seriam removidos/movidos sem executar a ação real:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --dry_run
   ```

3. **Mover Duplicatas para uma Pasta Específica:**

   Em vez de remover, move os arquivos duplicados para a pasta `duplicatas`:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --mover
   ```

4. **Especificar Tipos de Arquivos a Serem Processados:**

   Processa apenas arquivos `.jpg`, `.png` e `.gif`:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --tipos_imagem .jpg .png .gif
   ```

5. **Registrar as Operações em um Arquivo de Log Específico:**

   Registra todas as ações no arquivo `meu_log.log`:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --log "/caminho/para/meu_log.log"
   ```

6. **Exibir Informações Detalhadas Durante a Execução:**

   Obter feedback mais detalhado no terminal:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --verbose
   ```

7. **Combinação de Opções:**

   Executar uma simulação, mover duplicatas e registrar em um log específico com informações detalhadas:
   ```bash
   python limpeza_duplicatas.py "/caminho/para/sua/pasta" --mover --dry_run --log "/caminho/para/meu_log.log" --verbose
   ```

## 🔧 Funcionamento do Script

1. **Escaneamento do Diretório:**
   - O script percorre recursivamente todas as subpastas do diretório especificado.

2. **Cálculo de Hashes:**
   - **Imagens:** Calcula um hash perceptual para identificar imagens visualmente semelhantes.
   - **Outros Arquivos:** Calcula um hash SHA256 para identificar arquivos exatamente iguais.

3. **Identificação de Duplicatas:**
   - Agrupa arquivos que possuem o mesmo hash.

4. **Seleção e Remoção/Movimentação:**
   - Dentro de cada grupo de duplicatas, mantém apenas o arquivo de maior tamanho (presumidamente de melhor qualidade) e remove ou move os demais.

5. **Registro das Operações:**
   - Todas as ações são registradas no arquivo de log especificado ou exibidas no console se a opção de log não for utilizada.

## ⚙️ Personalizações e Melhorias Futuras

- **Suporte a Mais Formatos de Imagem:**
  - Adicione mais extensões de arquivos de imagem nas opções `--tipos_imagem` conforme necessário.

- **Utilização de Outros Métodos de Hash:**
  - Experimente diferentes métodos de hash perceptual (como `phash`, `dhash`) para melhorar a detecção de duplicatas.

- **Interface Gráfica (GUI):**
  - Implemente uma interface gráfica utilizando bibliotecas como `Tkinter` ou `PyQt` para facilitar o uso por usuários que preferem não utilizar a linha de comando.

- **Recuperação de Arquivos Movidos:**
  - Implemente uma funcionalidade para restaurar arquivos movidos caso ocorra algum erro durante o processo.

- **Integração com Serviços de Backup:**
  - Automatize o processo de backup antes da remoção/movimentação de arquivos duplicados para maior segurança.

## 🛠️ Resolução de Problemas

1. **Erro: "As bibliotecas 'Pillow' e 'imagehash' são necessárias"**

   - **Causa:** As bibliotecas necessárias não estão instaladas.
   - **Solução:** Instale as bibliotecas usando `pip`:
     ```bash
     pip install Pillow imagehash
     ```
     ou
     ```bash
     pip3 install Pillow imagehash
     ```

2. **Arquivos Não Estão Sendo Removidos/Movidos**

   - **Causa:** Falta de permissões ou arquivos em uso.
   - **Solução:**
     - Verifique se você possui as permissões necessárias para modificar os arquivos e pastas.
     - Certifique-se de que os arquivos não estão abertos em outro programa.
     - Utilize a opção `--verbose` para obter mais detalhes sobre o que está ocorrendo.

3. **O Script Não Identifica Duplicatas Visuais de Imagens**

   - **Causa:** Arquivos não estão no formato suportado ou problemas com as bibliotecas.
   - **Solução:**
     - Assegure-se de que os arquivos são do tipo suportado (verifique as extensões).
     - Verifique se as bibliotecas `Pillow` e `imagehash` estão corretamente instaladas.
     - Considere ajustar os parâmetros do hash perceptual (o script atual usa `average_hash`, mas você pode experimentar outros como `phash`, `dhash`, etc., modificando a função `calcular_hash_imagem`).

4. **Pasta 'duplicatas' Não Está Sendo Criada**

   - **Causa:** A opção `--mover` não foi utilizada ou problemas de permissão.
   - **Solução:**
     - Verifique se a opção `--mover` está sendo utilizada ao executar o script.
     - Assegure-se de que o diretório de destino tem espaço suficiente e permissões adequadas.
     - Verifique o arquivo de log para possíveis erros durante a criação ou movimentação dos arquivos.

5. **Desempenho Lento Durante a Execução**

   - **Causa:** Grande quantidade de arquivos ou arquivos muito grandes.
   - **Solução:**
     - Organize suas imagens em subpastas menores para reduzir a quantidade de arquivos processados de uma vez.
     - Execute o script em partes menores, se possível.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você encontrou um bug, tem uma sugestão de melhoria ou deseja adicionar uma nova funcionalidade, sinta-se à vontade para abrir uma [issue](https://github.com/seu-usuario/limpeza_duplicatas/issues) ou enviar um [pull request](https://github.com/seu-usuario/limpeza_duplicatas/pulls).

### Passos para Contribuir

1. **Fork o Repositório:**
   - Clique no botão "Fork" no canto superior direito da página do repositório.

2. **Clone o Repositório Forkado:**
   ```bash
   git clone https://github.com/seu-usuario/limpeza_duplicatas.git
   ```

3. **Crie uma Branch para Sua Alteração:**
   ```bash
   git checkout -b minha-melhoria
   ```

4. **Faça as Alterações Necessárias:**

5. **Commit as Suas Alterações:**
   ```bash
   git commit -m "Descrição da melhoria ou correção"
   ```

6. **Envie a Branch para o Repositório Remoto:**
   ```bash
   git push origin minha-melhoria
   ```

7. **Abra um Pull Request:**
   - Vá até o repositório original e abra um pull request comparando sua branch com a branch principal.

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato

Para dúvidas, sugestões ou contribuições, entre em contato:

- **Nome:** João
- **Email:** jpaulodamico@hotmail.com

---

**Nota:** SEMPRE FAÇA BACKUP de seus dados antes de executar operações em massa para evitar perda acidental de informações.

Este README fornece uma visão abrangente sobre como utilizar o script **LimpezaDuplicatas**, desde a instalação até exemplos práticos e resolução de problemas comuns. Siga as instruções cuidadosamente para garantir uma execução bem-sucedida e aproveite as funcionalidades avançadas para gerenciar seus arquivos de forma eficiente.

Se tiver dúvidas adicionais ou precisar de assistência para personalizar o script, sinta-se à vontade para entrar em contato!
