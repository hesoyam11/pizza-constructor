const orderPriceInput = document.querySelector('#order-price-input');
console.log('orderPriceInput', orderPriceInput.value);

const orderPriceSpan = document.querySelector('#order-price-span');
console.log('orderPriceSpan', orderPriceSpan.textContent);

const ingredientDivs = document.querySelectorAll('.ingredient');

function updatePrice() {
    let orderPrice = 0;
    for (let ingredientDiv of ingredientDivs) {
        let price = Number(ingredientDiv.querySelector('.price').textContent);
        let amount = Number(ingredientDiv.querySelector('input').value);
        orderPrice += price * amount;
        console.log(price, amount);
    }
    let orderPriceString = orderPrice.toFixed(2);
    orderPriceInput.value = orderPriceSpan.textContent = orderPriceString;
}

for (let ingredientDiv of ingredientDivs) {
    ingredientDiv.querySelector('input').onchange = function() {
        updatePrice();
    };
}
