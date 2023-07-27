

//handle comment edit send
document.addEventListener('DOMContentLoaded', () => {
    const editCommentButtons = document.querySelectorAll('.edit-comment-button');
    editCommentButtons.forEach(button => {
        button.addEventListener('click', () => {
            const commentDiv = button.closest('.comment');
            const editForm = commentDiv.querySelector('.edit-comment-form');
            editForm.classList.toggle('hidden');
        });
    });

    const editCommentForms = document.querySelectorAll('.edit-comment-form');
    editCommentForms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const commentId = form.dataset.commentId;
            const formData = new FormData(form);
            const response = await fetch('', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData,
            });
            if (response.ok) {
                const data = await response.json();
                // Update the comment content on success
                const commentDiv = form.closest('.comment');
                const commentContent = commentDiv.querySelector('.comment-content');
                commentContent.innerHTML = data.new_comment_html;
                form.classList.add('hidden');
            } else {
                // Handle error if needed
            }
        });
    });
});