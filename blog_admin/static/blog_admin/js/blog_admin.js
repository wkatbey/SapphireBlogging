let blogAdmin = new Vue({
	el: '#blog-admin',
	delimiters: ['[[', ']]'],
	data: {
		testInfo: '',
		categoryForm: {
			title: '',
			parent: ''
		},
		categoryCriteria: {
			title: '',
			results: []
		},
		categories: [

		]
	},
	methods: {
		submitCategoryForm() {
			fetch('api/CreateCategory/', { 
				method: 'POST', 
				body: JSON.stringify(this.categoryForm),
				headers: {
					'Content-Type': 'application/json',
					'X-CSRF-TOKEN': getCookie('CSRF-TOKEN')
				}
			});
		},
		getCategoriesByTitle() {
			
		},
		getCategoryToEdit() {

		}
	},
	mounted() {
		fetch('api/GetAllCategories/')
		.then(response => this.testInfo = response.json().then((categories) => {
			this.categories = categories;
		}))
	}
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
			
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}