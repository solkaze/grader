FROM ubuntu:24.04

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    && apt-get clean


# Python のテストサポート（pytestなど必要なら）
# RUN pip3 install pytest

# 作業ディレクトリ作成
WORKDIR /workspace

# ホストからコード・テストデータをコンテナにコピー（ビルド時）
# COPY ./src ./src
# COPY ./tests ./tests

# エントリーポイントは bash にしておく
CMD ["/bin/bash"]
