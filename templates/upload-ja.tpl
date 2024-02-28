<html>

<head>
    <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js"></script>
    <style>
        /* Basic Style */
        body {
            font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
            color: #333;
            background-color: #f4f4f4;
            padding: 20px;
        }

        .main-content {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }

        .main-content__header {
            color: #007bff;
            margin-bottom: 20px;
        }

        .main-content__divider {
            border-bottom: 1px solid #eee;
            margin-bottom: 20px;
        }

        .main-content__description {
            margin-bottom: 20px;
        }

        /* Foam styling */
        form {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
        }

        label {
            display: block;
            margin-bottom: 10px;
        }

        input[type="file"] {
            margin-bottom: 20px;
        }

        .btn-primary {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .btn-primary:hover {
            background-color: #0056b3;
        }

        /* Responsive design */
        @media (max-width: 600px) {
            .main-content {
                padding: 10px;
            }

            form {
                padding: 10px;
            }
        }
    </style>
</head>

<body>

    <div class="main">
        <div class="main-content">
            <h1 class="main-content__header">
                メールアドレスの正規化、ハッシュ化、およびエンコード
            </h1>
            <div class="main-content__divider"></div>
            <p class="main-content__description">
                アップロードしたファイルに記載されたメールアドレスを正規化、ハッシュ化、およびエンコードします。
            </p>

            <form id="file-form" action="https://{{ domain }}/{{ stage }}{{ path }}" method="post"
                enctype="multipart/form-data">
                <input type="file" name="file" id="file-input">
                <button class="btn btn-primary" type="submit">
                    Upload
                </button>
            </form>
        </div>
    </div>
</body>

</html>