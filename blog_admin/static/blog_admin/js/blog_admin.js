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
					'X-CSRFToken': getCookie('csrftoken')
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
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}