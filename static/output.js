document.querySelector('form').addEventListener('submit', function (e) {
            e.preventDefault();

            var formData = new FormData(this);

            fetch('/process_file', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('gen_que_output').innerHTML = '<p>' + data.result + '</p>';
            })
            .catch(error => console.error('Ошибка:', error));
        });