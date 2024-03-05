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
    </style>
</head>

{% set aws_region_mapping = {
    'us-east-2': 'US East (Ohio)',
    'us-east-1': 'US East (Virginia)',
    'us-west-1': 'US West (N. California)',
    'us-west-2': 'US West (Oregon)',
    'af-south-1': 'Africa (Cape Town)',
    'ap-east-1': 'Asia Pacific (Hong Kong)',
    'ap-south-2': 'Asia Pacific (Hyderabad)',
    'ap-southeast-3': 'Asia Pacific (Jakarta)',
    'ap-southeast-4': 'Asia Pacific (Melbourne)',
    'ap-south-1': 'Asia Pacific (Mumbai)',
    'ap-northeast-3': 'Asia Pacific (Osaka)',
    'ap-northeast-2': 'Asia Pacific (Seoul)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'ap-southeast-2': 'Asia Pacific (Sydney)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ca-central-1': 'Canada (Central)',
    'ca-west-1': 'Canada West (Calgary)',
    'eu-central-1': 'Europe (Frankfurt)',
    'eu-west-1': 'Europe (Ireland)',
    'eu-west-2': 'Europe (London)',
    'eu-south-1': 'Europe (Milan)',
    'eu-west-3': 'Europe (Paris)',
    'eu-south-2': 'Europe (Spain)',
    'eu-north-1': 'Europe (Stockholm)',
    'eu-central-2': 'Europe (Zurich)',
    'il-central-1': 'Israel (Tel Aviv)',
    'me-south-1': 'Middle East (Bahrain)',
    'me-central-1': 'Middle East (UAE)',
    'sa-east-1': 'South America (São Paulo)',
} %}

<body>

    <div data-role="page">

        <header data-role="header">
            <h1>Data Conversion Service for Unified ID 2.0</h1>
            <p>Normalize, hash, and encode email addresses.</p>
        </header>

        <div data-role="main" class="ui-content">
            <h2>Overview</h2>

            <p>This service normalizes, hashes, and encodes email addresses for use with <a
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
                <li>The download file contains normalized, hashed, and encoded data for email addresses, one per line.</li>
                <li>The rows are sorted randomly and cannot be matched against the uploaded file.</li>
                <li>The name of the download file will be a unique file name with UUID (e.g. 54f1c989-b7d7-4d97-a054-46562c8c66a8.csv)</li>
            </ul>

            <h2>Security</h2>

            <ul>
                <li>The service is hosted on AWS in the {{ aws_region_mapping[region] }} region.</li>
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
                <button class="btn btn-primary" type="submit" disabled>
                    Upload
                </button>
                </div>
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