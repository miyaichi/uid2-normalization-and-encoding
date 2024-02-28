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

## config.yml の設定

- region: デプロイするリージョンを指定します。
- source_bucket: アップロードされたファイルを保存するバケット名を指定します。定期的にファイルを削除するため、専用のバケットを作成してください。
- destination_bucket: エンコードしたファイルを保存するバケット名を指定します。定期的にファイルを削除するため、専用のバケットを作成してください。また、source_bucket とは異なるバケットを指定してください。
- expires_in: source_bucket, destination_bucket に保存されたファイルを削除するまでの時間を分単位で指定します。デフォルトは 60 分です。

## 処理内容

### 正規化

Unified ID 2.0 の[Normalization and Encoding](https://unifiedid.com/uid2/normalization-and-encoding)の仕様に従います。

- 先頭と末尾のスペースを削除します。
- ASCII 文字をすべて小文字に変換します。
- メールアドレス (ASCII コード 46) にピリオド (.) がある場合は、削除します。例えば、jane.doe@example.com を janedoe@example.com に正規化します。
- (条件付き) gmail.com のアドレスの場合のみ、@gmail.com の前にプラス記号 (+) とその後ろに追加の文字列を削除します。

### ハッシュ化

SHA-256 でハッシュ化します。

### エンコード

Base64 エンコードします。

### サンプル

| email                  | normalized_email      | hash and encoded                             |
| ---------------------- | --------------------- | -------------------------------------------- |
| jane.doe@gmail.com     | janedoe@gmail.com     | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| janedoe+home@gmail.com | janedoe@gmail.com     | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| JANESaoirse@gmail.com  | janesaoirse@gmail.com | ku4mBX7Z3qJTXWyLFB1INzkyR2WZGW4ANSJUiW21iI8= |
| user@example.com       | user@example.com      | tMmiiTI7IaAcPpQPFQ65uMVCWH8av9jw4cwf/F5HVRQ= |
