let blogAdmin = new Vue({
	el: '#blog-admin',
	delimiters: ['[[', ']]'],
	data: {
		testInfo: '',
		categoryForm: {
			title: '',
			parent: null,
			isEditInProgress: false,
			resetForm: function() {
				this.title = '';
				this.parent = null;
			},
			getCategoryToEdit: function(category) {
			    this.title = category.title;
                this.parent = category.parent;
                this.isEditInProgress = true;
			}
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
			}).then(response => {
				this.categoryForm.resetForm();
				this.getAllCategories();
			});
		},
		getCategoriesByTitle() {
			const title = this.categoryCriteria.title;
			const url = `api/GetCategoriesByTitle/${title}`;

			fetch(url).then(response => {
				return response.json();
			}).then(categories => {
				this.categoryCriteria.results = categories;
			})
		},
		getAllCategories() {
		    fetch('api/GetAllCategories/')
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