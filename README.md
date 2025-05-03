work_tester.pyが実行対象ファイルになります．
python3, java, c/c++のローカル環境がないと動かない場合があります．

input*.txtは標準入力で与えるべき入力例を与えます
output*.txtは標準入力で出てきてほしい出力例を与えます
(例)input1.txt, input2.txt, output1.txt, output2.txt...
数字で入力例に対する出力例が当てはまります

Dockerを使用する場合，環境を構築するためのDockerfileを使ってもらえればその環境を構築することができます
```
docker build -t image_name .
```
これを使うことでdockerのイメージを作成することができます．

```
docker run -it --rm image_name
```
これを実行すると，環境に入ることができ，[exit]をするとdockerのコンテナ事消すことができます．