let blogAdmin = new Vue({
	el: '#blog-entry-form',
	delimiters: ['[[', ']]'],
	data: {
		testInfo: '',
		isEditInProgress: false,
        blogEntry: {
			category: '',
			title: '',
			text_entry: '',
			private: false
		},
		categories: []
	},
	methods: {
		submitBlogEntryForm() {
			const form = document.getElementById('blog-form');

			form.submit();
		},
        getAllCategories() {
		    fetch('blog-admin/api/GetAllCategories/')
            .then(response => response.json())
            .then((categories) => {
                this.categories = categories;
            });
		}
	},
	mounted() {
		this.getAllCategories();
	}
});