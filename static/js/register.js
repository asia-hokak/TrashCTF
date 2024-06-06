function register() {
    let response_message = document.getElementById('response_message')
    const username = document.getElementById('username').value
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value;


    fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            }),
        })
        .then(response => response.json())
        .then(data => {
            response_message.innerHTML = data.result;
            response_message.classList.remove('hidden');
            response_message.classList.add('zoomer');
            if (data.result != "register successfully, redirecting to login...")
                response_message.classList.add('is-negative');
            else {
                response_message.classList.add('is-positive');
                redirect_to_home()
            }
            setTimeout(function() {
                response_message.classList.add('zoomerOut');
                
                setTimeout(function () {
                    response_message.classList.remove('is-positive');
                    response_message.classList.remove('is-negative');
                    response_message.classList.remove('zoomerOut');
                    response_message.classList.remove('zoomer');
                    response_message.classList.add('hidden');
                }, 1000);
            }, 2000)
        

        })
        .catch((error) => {
            console.error('Error:', error);
            response_message.innerHTML = 'Error';
        });
}

function redirect_to_home() {
    setTimeout(() => {
        window.location.href = '/login';  
    }, 1000);
}