let blogAdmin = new Vue({
	el: '#blog-admin',
	delimiters: ['[[', ']]'],
	data: {
		testInfo: '',
		categoryForm: {
			title: '',
			description: '',
			parent: ''
		}
	},
	methods: {
		submitCategoryForm() {
			// Nothing
		}
	},
	mounted() {
		fetch('https://api.coindesk.com/v1/bpi/currentprice.json')
		.then(response => this.testInfo = response.json().then((data) => {
			this.testInfo = data.time.updated;
		}))
	}
})