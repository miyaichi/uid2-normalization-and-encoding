<html>
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
