document.getElementById('run-code').addEventListener('click', function() {
    const code = document.getElementById('code-editor').value;
    
    fetch('/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').textContent = data.output;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').textContent = 'An error occurred';
    });
});
