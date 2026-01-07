// app.js

document.addEventListener('DOMContentLoaded', function () {
    const addBlogForm = document.getElementById('addBlogForm');
    const blogPostsContainer = document.getElementById('blogPosts');
    const addBlogBtn = document.getElementById('addBlogBtn'); // Get the button element

    addBlogBtn.addEventListener('click', function () { // Change event to 'click'
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;

        // Validate title and content (you can add more validation as needed)
        if (!title.trim() || !content.trim()) {
            alert('Please enter both title and content.');
            return;
        }

        // Create new blog post element
        const blogPost = document.createElement('div');
        blogPost.classList.add('bg-white', 'p-6', 'rounded', 'shadow-md');
        blogPost.innerHTML = `
            <h2 class="text-xl font-bold mb-2">${title}</h2>
            <p class="text-gray-700">${content}</p>
        `;

        // Append new blog post to the container
        blogPostsContainer.appendChild(blogPost);

        // Clear the form fields after adding blog
        document.getElementById('title').value = '';
        document.getElementById('content').value = '';
    });
});
