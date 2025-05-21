document.addEventListener('DOMContentLoaded', function() {
    DOMListener();
    setupPasswordToggle();
});

function setupPasswordToggle() {
    const toggleButton = document.querySelector('.toggle-password');
    const passwordField = document.getElementById('password');

    if(toggleButton && passwordField) {
        toggleButton.addEventListener('click', function() {
            // Toggle between password and text type
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
        });
    }
}

async function sha256(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hashBuffer))
          .map((b) => b.toString(16).padStart(2, '0'))
          .join('');
}

function DOMListener() {
    //show/hide password
    const form = document.getElementById('Login')
    //form listener
    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent default form submission
        await processFormData(form);
    });
}

async function processFormData(form) {
    const fieldsToSend = ['username','password'];
    let data = {};
    fieldsToSend.forEach(function(field){
        let value = form.elements[field].value;
        data[field] = value;
    });
    data['password'] = await sha256(data['password']);

    sendData(data)
}

async function sendData(data){
    let response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    let responseData= await response.json();

    if (response.status===200){
        window.location.href=responseData['redirectURL'];
    }else {
        document.getElementById('login-error').innerHTML = responseData["issue"];
    }
}