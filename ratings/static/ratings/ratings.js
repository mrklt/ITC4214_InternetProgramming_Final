var isAuthenticated = true;

document.addEventListener('DOMContentLoaded', function() {
    // Load recommendations for logged-in users
    loadRecommendations();

    // Handle star ratings
    document.querySelectorAll('.rating-container').forEach(container => {
        const stars = container.querySelectorAll('.star');
        const itemId = container.dataset.itemId;
        
        stars.forEach(star => {
            star.addEventListener('click', function() {
                if (!isAuthenticated) {
                    alert('Please log in to rate items');
                    return;
                }
                
                const value = this.dataset.value;
                submitRating(itemId, value);
                
                // Show review form
                container.querySelector('.review-form').style.display = 'block';
            });
        });
    });
});

function submitRating(itemId, stars) {
    fetch('/ratings/rate/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `item_id=${itemId}&stars=${stars}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateStarDisplay(itemId, data.avg_rating);
            loadRecommendations();  // Refresh recommendations
        }
    });
}

function loadRecommendations() {
    if (!isAuthenticated) return;
    
    fetch('/ratings/recommendations/')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('recommendations-container');
        container.innerHTML = data.recommendations.map(item => `
            <div class="col-md-4">
                <div class="item-card">
                    <h5>${item.name}</h5>
                    <div class="rating">★ ${item.avg_rating || 0}/5</div>
                </div>
            </div>
        `).join('');
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
