function addToCart(productId) {
    const csrfToken = '{{ csrf_token }}';
    
    fetch(`/add_to_cart_ajax/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${data.product} added to cart!`);
        } else {
            alert('There was an error adding the item to the cart.');
        }
    })
    .catch(error => console.error('Error:', error));
}