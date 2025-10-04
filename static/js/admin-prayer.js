// JavaScript for Prayer Management Page
document.addEventListener('DOMContentLoaded', function() {
    // User accordion functionality
    const userHeaders = document.querySelectorAll('.user-header');

    userHeaders.forEach(header => {
        header.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const userItems = document.querySelectorAll('.user-item');

            userItems.forEach(item => {
                const userName = item.querySelector('.user-name').textContent.toLowerCase();
                const requests = item.querySelectorAll('.request-item');
                let showUser = false;

                // Search in user name
                if (userName.includes(searchTerm)) {
                    showUser = true;
                } else {
                    // Search in requests
                    requests.forEach(request => {
                        const requestContent = request.querySelector('.request-content').textContent.toLowerCase();
                        const requestTitle = request.querySelector('.request-title').textContent.toLowerCase();

                        if (requestContent.includes(searchTerm) || requestTitle.includes(searchTerm)) {
                            showUser = true;
                        }
                    });
                }

                item.style.display = showUser ? 'block' : 'none';
            });
        });
    }

    // Filter functionality
    const filterSelect = document.getElementById('status-filter');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            const selectedStatus = this.value.toLowerCase();
            const requestItems = document.querySelectorAll('.request-item');

            if (selectedStatus === 'all') {
                // Show all requests
                requestItems.forEach(item => {
                    item.style.display = 'block';
                });

                // Show all users
                document.querySelectorAll('.user-item').forEach(user => {
                    user.style.display = 'block';
                });
            } else {
                // Filter requests by status
                requestItems.forEach(item => {
                    const statusElement = item.querySelector('.status-badge');
                    if (statusElement) {
                        const status = statusElement.classList.contains(`status-${selectedStatus}`);
                        item.style.display = status ? 'block' : 'none';
                    }
                });

                // Hide users with no visible requests
                document.querySelectorAll('.user-item').forEach(user => {
                    const visibleRequests = user.querySelectorAll('.request-item[style="display: block"]');
                    user.style.display = visibleRequests.length > 0 ? 'block' : 'none';
                });
            }
        });
    }

    // Reply form toggle
    const replyButtons = document.querySelectorAll('.reply-btn');

    replyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            // Get the associated form
            const requestItem = this.closest('.request-item');
            const replyForm = requestItem.querySelector('.reply-form');

            // Toggle the form visibility
            if (replyForm) {
                if (replyForm.style.display === 'none' || replyForm.style.display === '') {
                    replyForm.style.display = 'block';
                } else {
                    replyForm.style.display = 'none';
                }
            }
        });
    });
});