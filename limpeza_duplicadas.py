import os
import sys
import argparse
import hashlib
from pathlib import Path
from collections import defaultdict
import logging
import shutil

try:
    from PIL import Image
    import imagehash
except ImportError:
    print("As bibliotecas 'Pillow' e 'imagehash' são necessárias para executar este script.")
    print("Instale-as usando: pip install Pillow imagehash")
    sys.exit(1)

def configurar_logging(log_path):
    """
    Configura o sistema de logging para registrar as operações em um arquivo de log.

    :param log_path: Caminho completo para o arquivo de log.
    """
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # Anexa ao arquivo de log existente
    )

def calcular_hash_arquivo(file_path, chunk_size=8192):
    """
    Calcula o hash SHA256 de um arquivo.

    :param file_path: Caminho para o arquivo.
    :param chunk_size: Tamanho do bloco para leitura.
    :return: Hash SHA256 hexadecimal do arquivo.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logging.error(f"Erro ao calcular hash do arquivo {file_path}: {e}")
        return None

def calcular_hash_imagem(file_path):
    """
    Calcula o hash perceptual de uma imagem.

    :param file_path: Caminho para a imagem.
    :return: Hash perceptual (como string) da imagem.
    """
    try:
        with Image.open(file_path) as img:
            hash_perceptual = imagehash.average_hash(img)
        return str(hash_perceptual)
    except Exception as e:
        logging.error(f"Erro ao calcular hash perceptual da imagem {file_path}: {e}")
        return None

def identificar_duplicatas(diretorio, tipos_imagem=None, outros_tipos=None):
    """
    Identifica arquivos duplicados em um diretório.

    :param diretorio: Diretório para escanear.
    :param tipos_imagem: Conjunto de extensões de arquivos de imagem.
    :param outros_tipos: Conjunto de extensões de outros tipos de arquivos.
    :return: Dois dicionários contendo duplicatas de imagens e outros arquivos.
    """
    duplicatas_imagens = defaultdict(list)
    duplicatas_outros = defaultdict(list)

    for root, dirs, files in os.walk(diretorio):
        for file in files:
            caminho_arquivo = Path(root) / file
            ext = caminho_arquivo.suffix.lower()

            if tipos_imagem and ext in tipos_imagem:
                hash_img = calcular_hash_imagem(caminho_arquivo)
                if hash_img:
                    duplicatas_imagens[hash_img].append(caminho_arquivo)
            elif outros_tipos and ext in outros_tipos:
                hash_file = calcular_hash_arquivo(caminho_arquivo)
                if hash_file:
                    duplicatas_outros[hash_file].append(caminho_arquivo)
            else:
                # Ignora arquivos que não são imagens ou não estão nos outros tipos especificados
                continue

    return duplicatas_imagens, duplicatas_outros

def selecionar_arquivo_para_manter(arquivos):
    """
    Seleciona qual arquivo manter com base no tamanho (maior é melhor).

    :param arquivos: Lista de Path objetos representando arquivos duplicados.
    :return: Path objeto do arquivo a ser mantido.
    """
    arquivos_sorted = sorted(arquivos, key=lambda x: x.stat().st_size, reverse=True)
    return arquivos_sorted[0]

def remover_duplicatas(duplicatas, modo='arquivo', dry_run=False):
    """
    Remove arquivos duplicados, mantendo apenas um arquivo por grupo.

    :param duplicatas: Dicionário com grupos de duplicatas.
    :param modo: 'imagem' ou 'outro' para indicar o tipo de arquivo.
    :param dry_run: Se True, não remove arquivos, apenas registra as ações.
    """
    for hash_val, arquivos in duplicatas.items():
        if len(arquivos) < 2:
            continue  # Não são duplicatas

        arquivo_para_manter = selecionar_arquivo_para_manter(arquivos)
        arquivos_para_remover = [f for f in arquivos if f != arquivo_para_manter]

        for arquivo in arquivos_para_remover:
            if dry_run:
                logging.info(f"[Dry Run] Remover: {arquivo}")
                print(f"[Dry Run] Remover: {arquivo}")
            else:
                try:
                    os.remove(arquivo)
                    logging.info(f"Removido: {arquivo} (Duplicata de {arquivo_para_manter})")
                    print(f"Removido: {arquivo} (Duplicata de {arquivo_para_manter})")
                except Exception as e:
                    logging.error(f"Erro ao remover o arquivo {arquivo}: {e}")
                    print(f"Erro ao remover o arquivo {arquivo}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Script para identificar e remover arquivos duplicados em uma pasta, mantendo apenas a melhor versão."
    )
    parser.add_argument('diretorio', help="Caminho para o diretório a ser escaneado.")
    parser.add_argument('-m', '--mover', action='store_true', help="Mover os arquivos duplicados para uma pasta 'duplicatas' ao invés de removê-los.")
    parser.add_argument('-t', '--tipos_imagem', nargs='*', default=['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic'], help="Extensões de arquivos de imagem a serem processados (padrão: .jpg .jpeg .png .gif .bmp .tiff .heic).")
    parser.add_argument('-o', '--outros_tipos', nargs='*', default=['.pdf', '.docx', '.xlsx', '.txt'], help="Extensões de outros tipos de arquivos a serem processados (padrão: .pdf .docx .xlsx .txt).")
    parser.add_argument('-l', '--log', help="Caminho para o arquivo de log. Se não for especificado, usa 'limpeza_duplicatas.log' no diretório atual.")
    parser.add_argument('-d', '--dry_run', action='store_true', help="Executa o script em modo de simulação sem remover arquivos.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Exibe mais informações durante a execução.")

    args = parser.parse_args()

    diretorio = Path(args.diretorio).resolve()
    if not diretorio.exists() or not diretorio.is_dir():
        print(f"O diretório especificado '{diretorio}' não existe ou não é uma pasta.")
        sys.exit(1)

    log_path = args.log if args.log else diretorio / 'limpeza_duplicatas.log'
    configurar_logging(log_path)

    if args.verbose:
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        logging.getLogger().setLevel(logging.INFO)

    tipos_imagem = set([ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in args.tipos_imagem])
    outros_tipos = set([ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in args.outros_tipos])

    logging.info(f"Iniciando a identificação de duplicatas no diretório: {diretorio}")
    logging.info(f"Tipos de imagem a serem processados: {tipos_imagem}")
    logging.info(f"Outros tipos de arquivos a serem processados: {outros_tipos}")
    if args.dry_run:
        logging.info("Modo de simulação ativado. Nenhum arquivo será removido.")
    if args.mover:
        logging.info("Arquivos duplicados serão movidos para a pasta 'duplicatas'.")

    duplicatas_imagens, duplicatas_outros = identificar_duplicatas(diretorio, tipos_imagem, outros_tipos)

    # Processar duplicatas de imagens
    if duplicatas_imagens:
        logging.info(f"Encontradas {len(duplicatas_imagens)} grupos de imagens duplicadas.")
        print(f"Encontradas {len(duplicatas_imagens)} grupos de imagens duplicadas.")
        remover_duplicatas(duplicatas_imagens, modo='imagem', dry_run=args.dry_run)
    else:
        logging.info("Nenhuma duplicata de imagem encontrada.")
        print("Nenhuma duplicata de imagem encontrada.")

    # Processar duplicatas de outros arquivos
    if duplicatas_outros:
        logging.info(f"Encontrados {len(duplicatas_outros)} grupos de outros arquivos duplicados.")
        print(f"Encontrados {len(duplicatas_outros)} grupos de outros arquivos duplicados.")
        remover_duplicatas(duplicatas_outros, modo='outro', dry_run=args.dry_run)
    else:
        logging.info("Nenhuma duplicata de outros arquivos encontrada.")
        print("Nenhuma duplicata de outros arquivos encontrada.")

    # Se o modo de mover estiver ativado, criar a pasta 'duplicatas' e mover os arquivos
    if args.mover and not args.dry_run:
        pasta_duplicatas = diretorio / 'duplicatas'
        pasta_duplicatas.mkdir(exist_ok=True)
        # Reprocessar duplicatas para mover
        for duplicatas in [duplicatas_imagens, duplicatas_outros]:
            for hash_val, arquivos in duplicatas.items():
                if len(arquivos) < 2:
                    continue
                arquivo_para_manter = selecionar_arquivo_para_manter(arquivos)
                arquivos_para_mover = [f for f in arquivos if f != arquivo_para_manter]
                for arquivo in arquivos_para_mover:
                    destino = pasta_duplicatas / arquivo.name
                    try:
                        shutil.move(str(arquivo), str(destino))
                        logging.info(f"Movido: {arquivo} -> {destino}")
                        print(f"Movido: {arquivo} -> {destino}")
                    except Exception as e:
                        logging.error(f"Erro ao mover o arquivo {arquivo}: {e}")
                        print(f"Erro ao mover o arquivo {arquivo}: {e}")

    logging.info("Processo de limpeza de duplicatas concluído.")
    print("Processo de limpeza de duplicatas concluído.")

def selecionar_arquivo_para_manter(arquivos):
    """
    Seleciona qual arquivo manter com base no tamanho (maior é melhor).

    :param arquivos: Lista de Path objetos representando arquivos duplicados.
    :return: Path objeto do arquivo a ser mantido.
    """
    arquivos_sorted = sorted(arquivos, key=lambda x: x.stat().st_size, reverse=True)
    return arquivos_sorted[0]

if __name__ == "__main__":
    main()
