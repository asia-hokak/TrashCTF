function login() {
    let response_message = document.getElementById('response_message');
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        response_message.innerHTML = data.result;
        appear()
        if (data.result !== "login successful") {
            response_message.classList.add('is-negative');
        }
        else {
            response_message.classList.add('is-positive');
            redirect_to_home();
           
        }
        setTimeout(function() {
            response_message.classList.add('zoomerOut');
            remove_class();
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        response_message.innerHTML = 'Error';
        appear()
        response_message.classList.add('is-negative');
        setTimeout(function() {
            response_message.classList.add('zoomerOut');
            remove_class()
        }, 2000);
    });
}

function remove_class() {
    setTimeout(function() {
        response_message.classList.remove('is-positive');
        response_message.classList.remove('is-negative');
        response_message.classList.remove('zoomerOut');
        response_message.classList.remove('zoomer');
        response_message.classList.add('hidden');
    }, 1000);
}

function redirect_to_home() {
    setTimeout(() => {
        window.location.href = '/';  // Redirect to home page
    }, 1000);
}

function appear() {
    response_message.classList.remove('hidden');
    response_message.classList.add('zoomer');
}