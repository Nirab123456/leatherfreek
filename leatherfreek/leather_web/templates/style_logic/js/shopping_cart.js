
var taxRate = 0.05; // 5% tax rate
var shippingRate = 15.00; // Fixed shipping rate
var fadeTime = 300; // Animation time

/* Recalculate cart */
function recalculateCart() {
  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).find('.product-line-price').text().replace('$', ''));
  });

  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0); // Shipping applies if subtotal > 0
  var total = subtotal + tax + shipping;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').text('$' + subtotal.toFixed(2));
    $('#cart-tax').text('$' + tax.toFixed(2));
    $('#cart-shipping').text('$' + shipping.toFixed(2));
    $('#cart-total').text('$' + total.toFixed(2));
    
    // Show/hide checkout button based on total
    if (total == 0) {
      $('.checkout').fadeOut(fadeTime);
    } else {
      $('.checkout').fadeIn(fadeTime);
    }
    
    $('.totals-value').fadeIn(fadeTime);
  });
}

async function increase_quantity_ajax(product_id){
  const csrf = '{{ csrf_token }}';
  const response = await fetch(`/increase_quantity_ajax/${product_id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf,
    },
  });
  const data = await response.json();
  if (data.success) {
    alert('Quantity increased!');
  } else {
    alert('There was an error increasing the quantity.');
  }
  recalculateCart();
}

async function decrease_quantity_ajax(product_id){
  const csrf = '{{ csrf_token }}';
  const response = await fetch(`/decrease_quantity_ajax/${product_id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf,
    },
  });
  const data = await response.json();
  if (data.success) {
    alert('Quantity decreased!');
  } else {
    alert('There was an error decreasing the quantity.');
  }
  recalculateCart();
}

function updateQuantity_ajax(product_id) {
  // current value of the input field
  const quantity = document.querySelector(`input[data-product-id="${product_id}"]`).value;

  console.log(`Quantity from input field: ${quantity}`);

  // find the hidden div tag
  const hiddenDiv = document.querySelector(`div[data-previous-quantity-product-id="${product_id}"]`);

  // check if hiddenDiv is found
  if (!hiddenDiv) {
    console.error(`No <div> tag found with data-product-id="${product_id}"`);
    return; // exit the function early
  }

  // quantity previously stored in the div tag
  const previous_quantity = hiddenDiv.textContent.trim();
  // make it a number
  const previous_quantity_number = parseInt(previous_quantity);

  console.log(`Previous quantity from <div> tag: ${previous_quantity_number}`);

  if (quantity > previous_quantity_number) {
    increase_quantity_ajax(product_id);
  } else if (quantity < previous_quantity_number) {
    decrease_quantity_ajax(product_id);
  }

  // Update inline price immediately
  update_inline_price(product_id);
}

/* Remove item from cart */
async function removeItem(product_id) {
  const csrf = '{{ csrf_token }}';
  const response = await fetch(`/remove_from_cart_ajax/${product_id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf,
    },
  });
  const data = await response.json();
  if (data.success) {
    alert('Item removed from cart!');
    // find the product element in the DOM
    const productElement = document.querySelector(`.product[data-product-id="${product_id}"]`);
    if (productElement) {
      // remove the product element from the DOM
      productElement.remove();
      recalculateCart();
    } else {
      console.error(`No product element found with data-product-id="${product_id}"`);
    }
  } else {
    alert('There was an error removing the item from the cart.');
  }
}

function update_inline_price(product_id){
  var quantity = document.querySelector(`input[data-product-id="${product_id}"]`).value;
  var price = document.querySelector(`.product[data-product-id="${product_id}"] .product-price`).textContent;
  price = price.replace('$', '');
  var line_price = quantity * price;
  document.querySelector(`.product[data-product-id="${product_id}"] .product-line-price`).textContent = '$' + line_price.toFixed(2);
}

recalculateCart();
