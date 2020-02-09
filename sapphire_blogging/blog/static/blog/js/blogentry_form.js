function submitPrivatePost() {
	let form = document.getElementById('blog-form');

	form.action = 'private'

	form.submit();
}