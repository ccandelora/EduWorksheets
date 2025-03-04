document.addEventListener('DOMContentLoaded', function() {
    const worksheetForm = document.getElementById('worksheetForm');
    const templateSelect = document.getElementById('template');
    const contentTextarea = document.getElementById('content');

    // Sample templates (in a real application, these would be fetched from the server)
    const templates = {
        1: "Multiple Choice:\n1. Question\n   a) Option 1\n   b) Option 2\n   c) Option 3\n   d) Option 4\n\n2. Question\n   a) Option 1\n   b) Option 2\n   c) Option 3\n   d) Option 4",
        2: "Fill in the blanks:\n1. __________ is the capital of France.\n2. The largest planet in our solar system is __________.",
        3: "Matching:\n1. A) Item 1    [  ] Corresponding item\n2. B) Item 2    [  ] Corresponding item\n3. C) Item 3    [  ] Corresponding item"
    };

    templateSelect.addEventListener('change', function() {
        const selectedTemplateId = this.value;
        contentTextarea.value = templates[selectedTemplateId] || '';
    });

    worksheetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch('/create_worksheet', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Worksheet created successfully!');
                window.location.href = '/dashboard';
            } else {
                alert('Failed to create worksheet. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while creating the worksheet');
        });
    });
});
