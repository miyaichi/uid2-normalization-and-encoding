# uid2-normalization-and-encoding

## はじめに

[Unified ID 2.0](https://unifiedid.com)の普及に伴い、顧客のメールアドレスをハッシュ化して扱うことがが増えてきました。こうしたニーズに答えるため、アップロードしたメールアドレスを正規化、ハッシュ化、エンコードするサービスを開発しました。

## 特徴

- メールアドレスの正規化、ハッシュ化、エンコードを一括で行えます。
- ユーザーがアップロードしたファイル、変換したファイルは、一定時間後（デフォルトは 1 時間）に自動的に削除します。
- メールアドレスのファイルとエンコードしたファイルを用意に照合できないよう、エンコードしたファイルにはユーザーがアップロードしたファイル名は含まず、データの並びもランダムになります。

## 使い方

1. アップロード用のエンドポイントに GET リクエストを送り、ファイルをアップロードするフォームを表示します。
2. フォームから、メールアドレスが１行に１つずつ書かれたテキストファイルをアップロードします。
3. ダウンロードリンクが表示されるので、それをクリックしてエンコードしたファイルをダウンロードします。

## システム構成

![uid2-normalization-and-encoding](https://github.com/miyaichi/uid2-normalization-and-encoding/assets/129797/45b781a6-c91c-4a7a-8233-76c1357fab33)

## デプロイ方法

1. serverless framework をインストールします。serverless-python-requirements も追加でインストールします。
   ```bash
   npm install -g serverless
   npm install --save serverless-python-requirements
   ```
2. このリポジトリをクローンします。
   ```bash
   git clone https://github.com/miyaichi/uid2-normalization-and-encoding.git
   ```
3. ディレクトリを移動します。
   ```bash
   cd uid2-normalization-and-encoding
   ```
4. config.yml を作成し、設定を記述します。
   ```bash
   cp config.yml.sample config.yml
   ```
5. デプロイします。
   ```bash
   sls deploy
   ```
