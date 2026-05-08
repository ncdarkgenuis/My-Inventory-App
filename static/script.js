const contactForm = document.querySelector('form');

contactForm.addEventListener('submit', function(e) {
    e.preventDefault();

    // Get values from the form
    const formData = {
        name: document.querySelector('input[type="text"]').value,
        email: document.querySelector('input[type="email"]').value,
        message: document.querySelector('textarea').value
    };

    // Use FETCH to send data to our Python server
    fetch('/submit_contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        // Show the success message in the UI
        contactForm.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <h2 style="color: #2ecc71;">Sent to Database!</h2>
                <p>${data.message}</p>
                <button onclick="window.location.reload()" class="btn">Send Another</button>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function loadInventory() {
    fetch('/get_inventory')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('inventoryBody');
        tableBody.innerHTML = ''; // Clear old data
        
        data.forEach(item => {
            tableBody.innerHTML += `
                <tr style="border-bottom: 1px solid #ddd; text-align: center;">
                    <td style="padding: 15px; text-align: left;">${item[1]}</td>
                    <td>${item[2]}</td>
                    <td>GH₵ ${item[3]}</td>
                </tr>
            `;
        });
    });
}

// Call this when the page loads
window.onload = loadInventory;

function addItem() {
    const itemData = {
        name: document.getElementById('itemName').value,
        qty: document.getElementById('itemQty').value,
        price: document.getElementById('itemPrice').value
    };

    fetch('/add_item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadInventory(); // Refresh the table to show the new item
    });
}