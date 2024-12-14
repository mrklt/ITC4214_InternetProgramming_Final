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
            updateStarDisplay(itemId, stars);
            loadRecommendations();  // Refresh recommendations
        }
    });
}

function updateStarDisplay(itemId, stars) {
    const container = document.querySelector(`.rating-container[data-item-id="${itemId}"]`);
    const starElements = container.querySelectorAll('.star');
    
    starElements.forEach((star, index) => {
        if (index < stars) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function loadRecommendations() {
    if (!isAuthenticated) return;

    fetch('/ratings/recommendations/')
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector('#recommendations-container');
            
            if (data.recommendations.length === 0) {
                container.innerHTML = '<p class="text-center">No recommendations available.</p>';
                return;
            }

            container.innerHTML = data.recommendations.map(item => `
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        ${item.image_url ? `<img src="${item.image_url}" class="card-img-top" alt="${item.name}" style="height: 200px; object-fit: cover;">` : ''}
                        <div class="card-body">
                            <h5 class="card-title">${item.name}</h5>
                            <p class="card-text">Rating: ★ ${item.avg_rating ? item.avg_rating.toFixed(1) : 0}/5</p>
                            <a href="/products/${item.id}/" class="btn btn-primary mt-auto">More Details</a>
                        </div>
                    </div>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading recommendations:', error);
            container.innerHTML = '<p class="text-center">Failed to load recommendations. Please try again later.</p>';
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