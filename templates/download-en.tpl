<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Conversion Service for Unified ID 2.0</title>

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

        a.disabled{
           pointer-events: none;
        }
    </style>
</head>

<body>

    <div data-role="page">

        <header data-role="header">
            <h1>Data Service for Unified ID 2.0</h1>
            <p>Normalize, hash, and encode email addresses and phone numbers.</p>
        </header>

        <div data-role="main" class="ui-action">
            <p>Download the converted file {{key}} from <a href="{{ location["GET"] }}" id="download" onclick="startDownload">this link</a>.</p>
            <p>The file will be automatically deleted after {{ expires_in }} minutes.</p>
            <script>
                var intervalId;

                function startDownload() {
                    var link = document.getElementById("download");
                    link.classList.add("disabled");
                    intervalId = setInterval(checkStatus, 1000);
                }

                function checkStatus() {
                    var xhr = new XMLHttpRequest();
                    xhr.open("HEAD", "{{ location["HEAD"] }}", true);
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4) {
                            if (xhr.status === 200) {
                                link.classList.remove("disabled");
                                window.location.href = "{{ location["GET"] }}";
                                clearInterval(intervalId);
                            }
                        }
                    };
                    xhr.send();
                }
            </script>
        </div>

        <footer data-role="footer">
            <p>&copy; 2024 Yoshihiko Miyaichi - <a href="http://pier1.co.jp">pier1.co.jp</a></p>
        </footer>

    </div>

</body>

</html>