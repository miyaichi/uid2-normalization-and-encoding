<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified ID 2.0のためのメールアドレス変換サービス</title>

    <link href="http://fonts.googleapis.com/earlyaccess/notosansjp.css">

    <style>
        /* Body */
        body {
            text-align: center;
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Header */
        header {
            padding: 5px;
        }

        h1 {
            font-size: 24px;
            margin: 0;
        }

        /* Main contents */
        .ui-content {
            display: inline-block;
            text-align: left;
            padding: 20px;
        }

        .ui-action {
            text-align: center;
            padding: 20px;
        }

        h2 {
            font-size: 18px;
            margin-top: 20px;
        }

        p {
            margin-bottom: 10px;
        }

        /* List */
        li {
            margin-bottom: 10px;
        }

        /* Code */
        code {
            background-color: #f6f8fa;
            padding: 2px 4px;
            border-radius: 4px;
        }

        /* Button */
        .btn {
            border: 1px solid #ccc;
            background-color: #fff;
            color: #333;
            padding: 5px 10px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
        }

        .btn-primary {
            background-color: #007bff;
            color: #fff;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 10px;
            margin-top: 20px;
        }

        /* Other */
        a {
            color: #007bff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .ui-collapsible {
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
        }

        .ui-collapsible-header {
            background-color: #f6f8fa;
            padding: 10px;
        }

        .ui-collapsible-content {
            padding: 10px;
        }
    </style>
</head>

{% set aws_region_mapping = {
    'us-east-2': '米国東部（オハイオ）',
    'us-east-1': '米国東部 (バージニア)',
    'us-west-1': '米国西部（北カリフォルニア）',
    'us-west-2': '米国西部（オレゴン）',
    'af-south-1': 'アフリカ (ケープタウン)',
    'ap-east-1': 'アジアパシフィック (香港)',
    'ap-south-2': 'アジアパシフィック (ハイデラバード)',
    'ap-southeast-3': 'アジアパシフィック (ジャカルタ)',
    'ap-southeast-4': 'アジアパシフィック (メルボルン)',
    'ap-south-1': 'アジアパシフィック（ムンバイ）',
    'ap-northeast-3': 'アジアパシフィック (大阪)',
    'ap-northeast-2': 'アジアパシフィック（ソウル）',
    'ap-southeast-1': 'アジアパシフィック（シンガポール）',
    'ap-southeast-2': 'アジアパシフィック（シドニー）',
    'ap-northeast-1': 'アジアパシフィック（東京）',
    'ca-central-1': 'カナダ（中部）',
    'ca-west-1': 'カナダ西部 (カルガリー)',
    'eu-central-1': '欧州 (フランクフルト)',
    'eu-west-1': '欧州 (アイルランド)',
    'eu-west-2': '欧州 (ロンドン)',
    'eu-south-1': '欧州 (ミラノ)',
    'eu-west-3': '欧州 (パリ)',
    'eu-south-2': '欧州 (スペイン)',
    'eu-north-1': '欧州 (ストックホルム)',
    'eu-central-2': '欧州 (チューリッヒ)',
    'il-central-1': 'イスラエル (テルアビブ)',
    'me-south-1': '中東 (バーレーン)',
    'me-central-1': '中東 (アラブ首長国連邦)',
    'sa-east-1': '南米（サンパウロ）',
} %}

<body>

    <div data-role="page">

        <header data-role="header">
            <h1>Unified ID 2.0のためのメールアドレス変換サービス</h1>
            <p>メールアドレスの正規化、ハッシュ化、エンコードを行います。</p>
        </header>

        <div data-role="main" class="ui-content">
            <h2>サービス概要</h2>

            <p>このサービスは、<a href="https://unifiedid.com/ja/">Unified ID 2.0</a> で利用する際に必要なメールアドレスの正規化、ハッシュ化、エンコードを行います。</p>

            <p>サービスの詳細、システム概要、ソースコードは GitHub: <a
                    href="https://github.com/miyaichi/uid2-normalization-and-encoding">Email
                    address processing service for Unified ID 2.0</a> を確認してください。</p>

            <h2>使い方</h2>

            <ol>
                <li>メールアドレスを1行に1つずつ記載したテキストファイルを用意します。</li>
                <li>ファイルをアップロードします。</li>
                <li>変換後のファイルをダウンロードします。ダウンロードは{{ expires_in }}分以内に行ってください。</li>
            </ol>

            <h2>変換後のファイル</h2>

            <ul>
                <li>ダウンロードファイルには、1行に1ずつ記載された、メールアドレスを正規化、ハッシュ化、エンコードしたデータが含まれます。</li>
                <li>行は無作為に並べ替えられていますので、アップロードしたファイルと照合することはできません。</li>
                <li>ダウンロードファイルの名前は、UUIDを使ったユニークなファイル名（例:54f1c989-b7d7-4d97-a054-46562c8c66a8.csv）になります。</li>
            </ul>

            <h2>セキュリティ</h2>

            <ul>
                <li>このサービスは、AWSの {{ aws_region_mapping[region] }} リージョンで運用されています。</li>
                <li>アップロードされたファイル、変換されたファイルは、{{ expires_in }}分後に自動削除されます。</li>
                <li>メールアドレスは、ログファイルを含めて、システムには一切記録されません。</li>
                <li>オリジナルのファイル名は保持せず、変換後のデータの順序を無作為にすることで、匿名性を高めています。</li>
            </ul>
        </div>

        <div data-role="main" class="ui-action">
            <h2>ファイルアップロード</h2>
            <form id="file-form" action="https://{{ domain }}/{{ stage }}{{ path }}?language={{ language }}"
                method="post" enctype="multipart/form-data">
                <p><input type="checkbox" id="agree" /><label for="agree">上記内容を確認の上、サービスを利用する</label></p>

                <input type="file" name="file" id="file-input" disabled>
                <button class="btn btn-primary" type="submit" disabled>
                    アップロード
                </button>
            </form>
            <script type="text/javascript">
                document.getElementById('agree').addEventListener('change', function () {
                    if (this.checked) {
                        document.getElementById('file-input').disabled = false;
                        document.querySelector('button[type="submit"]').disabled = false;
                    } else {
                        document.getElementById('file-input').disabled = true;
                        document.querySelector('button[type="submit"]').disabled = true;
                    }
                });
            </script>
        </div>

        <footer data-role="footer">
            <p>&copy; 2024 Yoshihiko Miyaichi - <a href="http://pier1.co.jp">pier1.co.jp</a></p>
        </footer>

    </div>

</body>

</html>