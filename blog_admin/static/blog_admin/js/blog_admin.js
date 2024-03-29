let blogAdmin = new Vue({
	el: '#blog-admin',
	delimiters: ['[[', ']]'],
	data: {
		testInfo: '',
		isEditInProgress: false,
        categoryForm: {
            id: null,
			title: '',
            parentModel: null,
            parent: null,
			resetForm: function() {
				this.title = '';
                this.parentModel = null;
                this.parent = null;
            },
            preProcess: function () {
            	if (this.parentModel) {
            		this.parent = this.parentModel.id;	
            	}
            }
		},
		categoryCriteria: {
			title: '',
			results: []
		},
		categories: []
	},
	methods: {
        submitCategoryForm() {
            this.categoryForm.preProcess();

		    if (this.isEditInProgress) {
		        fetch('api/UpdateCategory/', {
                    method: 'PUT',
                    body: JSON.stringify(this.categoryForm),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    this.resetForm();
                    this.getAllCategories();
                });
		    }
		    else {
		    	fetch('api/CreateCategory/', {
                    method: 'POST',
                    body: JSON.stringify(this.categoryForm),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    this.resetForm();
                    this.getAllCategories();
                });
		    }
		},
		getCategoriesByTitle() {
			let title = this.categoryCriteria.title;

			title = title ? title : "NO_CATEGORY";

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
		},
        getCategoryToEdit(category) {
            this.categoryForm.id = category.id;
		    this.categoryForm.title = category.title;
            this.categoryForm.parentModel = this.categories.find(x => category.parent && x.id == category.parent.id);
            this.isEditInProgress = true;
		},
		resetForm() {
		    this.categoryForm.resetForm();
		    this.isEditInProgress = false;
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