document.addEventListener('DOMContentLoaded', (event) => {
    const flagInput = document.getElementById('FLAG');
    if (flagInput) {
        flagInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // 阻止默认的回车提交行为
                challenges_send(); // 调用你定义的函数
            }
        });
    }
    else
        console.log("not found");
});

function challenges_send() {
    let response_message = document.getElementById('response_message')
    const flag = document.getElementById('FLAG').value
    const currentPageUrl = window.location.href;
    fetch(currentPageUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                flag: flag
            }),
        })
        .then(response => response.json())
        .then(data => {
            response_message.innerHTML = data.result;
            response_message.classList.remove('hidden');
            response_message.classList.add('zoomer');
            if (data.result != "correct")
                response_message.classList.add('is-negative');
            else {
                response_message.classList.add('is-positive');
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
