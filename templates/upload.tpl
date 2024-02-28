<html>
<head>
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js"></script>
</head>
<body>
<form id="file-form"
action="https://{{ domain }}/{{ stage }}{{ path }}"
method="post" enctype="multipart/form-data">
<label for="file-input">Choose file</label>
<input type="file" name="file" id="file-input">
<button class="btn btn-primary" type="submit">
Upload
</button>
</form>
</body>
</html>
