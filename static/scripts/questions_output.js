document.querySelector('form[action="/process_answer_questions"]').addEventListener('submit', function (e) {
            e.preventDefault();

            var formData = new FormData(this);

            fetch('/process_answer_questions', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('answer_output').innerHTML = '<p>' + data.result + '</p>';
            })
            .catch(error => console.error('Ошибка:', error));
        });