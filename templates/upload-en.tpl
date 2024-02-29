<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Address Conversion Service for Unified ID 2.0</title>

    <link href="http://fonts.googleapis.com/earlyaccess/notosansjp.css">

    <style>
        /* Body */
        body {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: #333;
            margin: 0;
            padding: 0;
        }

        /* Header */
        header {
            text-align: center;
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

<body>

    <div data-role="page">

        <header data-role="header">
            <h1>Email Address Conversion Service for Unified ID 2.0</h1>
            <p>Normalize, hash, and encode email addresses.</p>
        </header>

        <div data-role="main" class="ui-content">
            <h2>Overview</h2>

            <p>This tool normalizes, hashes, and encodes email addresses for use with <a
                    href="https://unifiedid.com">Unified ID 2.0</a>.</p>

            <p>For more information about the service, system overview, and source code, check GitHub: <a
                    href="https://github.com/miyaichi/uid2-normalization-and-encoding">Email
                    address processing service for Unified ID 2.0</a>.

            <h2>How to Use</h2>

            <ol>
                <li>Prepare a text file with one email address per line.</li>
                <li>Upload the file to the service.</li>
                <li>Download the converted file. The download link will expire after {{ expires_in }} minutes.</li>
            </ol>

            <h2>The Converted File</h2>

            <ul>
                <li>The download file contains normalized, hashed, and encoded data for email addresses, one per line.
                </li>
                <li>The rows are sorted randomly and cannot be matched against the uploaded file.</li>
                <li>The download file will be named YYYYYMMDD-HHMMMSS.csv, using the uploaded time.</li>
            </ul>

            <h2>Security</h2>

            <ul>
                <li>The uploaded and converted files are automatically deleted after {{ expires_in }} minutes.</li>
                <li>Email addresses are never stored in the system, including in log files.</li>
                <li>We enhance anonymity by not retaining the original file name and randomizing the order of the
                    converted data.</li>
            </ul>
        </div>

        <div data-role="main" class="ui-action">
            <h2>File Upload</h2>
            <form id="file-form" action="https://{{ domain }}/{{ stage }}{{ path }}?language={{ language }}"
                method="post" enctype="multipart/form-data">
                <p><input type="checkbox" id="agree" /><label for="agree">Please review the above information before using the service.</label></p>

                <input type="file" name="file" id="file-input" disabled>
                <button class="btn btn-primary" type="submit">
                    Upload
                </button>
                </div>
            </form>
            <script type="text/javascript">
                document.getElementById('agree').addEventListener('change', function () {
                    if (this.checked) {
                        document.getElementById('file-input').disabled = false;
                    } else {
                        document.getElementById('file-input').disabled = true;
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