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
    $('#cart-subtotal').text(subtotal.toFixed(2));
    $('#cart-tax').text(tax.toFixed(2));
    $('#cart-shipping').text(shipping.toFixed(2));
    $('#cart-total').text(total.toFixed(2));
    
    // Show/hide checkout button based on total
    if (total == 0) {
      $('.checkout-cta').fadeOut(fadeTime);
    } else {
      $('.checkout-cta').fadeIn(fadeTime);
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
  const PRODUCT_ID = product_id;
  console.log(`Product ID: ${PRODUCT_ID}`);
  const quantity = document.querySelector(`input[data-product-id="${PRODUCT_ID}"]`).value;
  console.log(`Quantity from input field: ${quantity}`);
  const hiddenDiv = document.querySelector(`div[data-previous-quantity-product-id="${PRODUCT_ID}"]`);
  if (!hiddenDiv) {
    console.error(`No <div> tag found with data-product-id="${PRODUCT_ID}"`);
    return;
  }
  const previous_quantity = hiddenDiv.textContent.trim();
  const previous_quantity_number = parseInt(previous_quantity);
  console.log(`Previous quantity from <div> tag: ${previous_quantity_number}`);

  if (quantity > previous_quantity_number) {
    increase_quantity_ajax(PRODUCT_ID);
  } else if (quantity < previous_quantity_number) {
    decrease_quantity_ajax(PRODUCT_ID);
  }
  // update hidden div with new quantity
  hiddenDiv.textContent = quantity;
  

  // Update inline price immediately
  update_inline_price(product_id);
}

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
    const productElement = document.querySelector(`.product[data-product-id="${product_id}"]`);
    if (productElement) {
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
  var price = document.querySelector(`.product[data-product-id="${product_id}"] .price`).textContent;
  price = price.replace('$', '');
  var line_price = quantity * price;
  document.querySelector(`.product[data-product-id="${product_id}"] .product-line-price`).textContent = '$' + line_price.toFixed(2);
}
  
async function apply_coupon_code(event) {
  event.preventDefault(); // Prevent the default form submission
  const csrf = '{{ csrf_token }}';
  const coupon_code = document.querySelector('#promo-code').value;
  const grand_total = document.querySelector('#cart-total').textContent;
  console.log(`Coupon code: ${coupon_code}`);
  console.log(`Grand total: ${grand_total}`);

  try {
    const response = await fetch(`/apply_coupon_code_ajax/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf,
      },
      body: JSON.stringify({
        coupon_code: coupon_code,
        grand_total: grand_total,
      }),
    });

    const data = await response.json();
    if (data.success) {
      alert('Coupon code applied!');
      document.querySelector('#cart-total').textContent = data.grand_total.toFixed(2);
    } else {
      alert('There was an error applying the coupon code.');
    }
  } catch (error) {
    console.error('Error applying coupon code:', error);
    alert('There was an error applying the coupon code.');
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const colorDivs = document.querySelectorAll('.color-viewer');
  colorDivs.forEach(div => {
      const hexCode = div.getAttribute('data-hex');
      div.style.backgroundColor = hexCode;
  });
});


recalculateCart();
