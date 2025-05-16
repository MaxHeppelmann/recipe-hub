document.addEventListener('DOMContentLoaded', DOMListener());
async function sha256(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hashBuffer))
          .map((b) => b.toString(16).padStart(2, '0'))
          .join('');
}

function DOMListener() {
    const form = document.getElementById('Signup')
    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent default form submission
        await processFormData(form);
    });
}
async function processFormData(form) {
    const fieldsToSend = ['username','email','password'];
    let data={};
    fieldsToSend.forEach(function(field){
        let value = form.elements[field].value;
        data[field] = value;

    });
    data['password'] = await sha256(data['password']);
    sendData(data)
}

async function sendData(data){
    let response = await fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const responseData = await response.json();
    if (response.status !== 303) {
        document.getElementById('Error-Box').innerHTML = "This "+responseData['issue']+" is already in use.";
    }
    else{
        window.location.href = responseData['redirectURL'];
    }
;
}