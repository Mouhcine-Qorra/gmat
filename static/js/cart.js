var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'action:', action)

		console.log('USER:', user)
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
			console.log('entered as AnonymousUser')
		}else{
			updateUserOrder(productId, action)
			console.log('entered as', user)
		}
	})
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')
		var url = '/update_item/'
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'user':user})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
		    location.reload()
		});
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')
		var url = '/update_item/'
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action, 'user':user})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('Data:', data)
		    location.reload()
		});
}
