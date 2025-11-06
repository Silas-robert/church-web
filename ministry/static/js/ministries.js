document.querySelectorAll('.filter-btn').forEach(button => {
    button.addEventListener('click', () => {
        const filter = button.getAttribute('data-filter');
        filterItems(filter);
    });
});

function filterItems(category) {
    const items = document.querySelectorAll('.ministry-item');
    const msg = document.getElementById('no-results');

    let visibleCount = 0;

    items.forEach(item => {
        if (match) {
            wrapper.classList.remove('hide');
            visible++;
        } else {
            wrapper.classList.add('hide');
        }

    });

    // Show message if no items
    if (visibleCount === 0) {
        msg.innerHTML = `<p class="no-results-text">No ${category.replace('-', ' ')} available at the moment.</p>`;
    } else {
        msg.innerHTML = '';
    }
}



document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.filter-buttons [data-filter]');
    const cards = Array.from(document.querySelectorAll('.ministry-card'));
    const container = document.getElementById('ministries-container') || document.querySelector('.row');
    const msgContainer = document.getElementById('no-results-container');

    if (!cards.length || !buttons.length) return;

    const normalize = s => String(s || '').toLowerCase().trim();

    const filterLabels = {
        all: 'ministries or projects',
        youth: 'Youth',
        women: 'Women',
        men: 'Men',
        children: 'Children',
        choir: 'Choir & worship team',
        worship: 'Church projects'
    };

    function removeNoResults() {
        msgContainer.innerHTML = '';
    }

    function showNoResults(filter) {
        removeNoResults();
        const label = filterLabels[filter] || filter;
        const msg = document.createElement('p');
        msg.style.color = '#9c405c';
        msg.style.fontWeight = 'bold';
        msg.style.textAlign = 'center';
        msg.style.margin = '10px 0';
        msg.innerText = `No ${label} content yet.`;
        msgContainer.appendChild(msg);

        // auto-hide after 4 seconds
        setTimeout(() => {
            msg.remove();
        }, 4000);
    }

    buttons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const filter = normalize(this.dataset.filter || '');
            let visible = 0;

            cards.forEach(card => {
                const cat = normalize(card.dataset.category || card.className);
                const wrapper = card.closest('.col') || card;
                const tokens = cat.split(/\s+/);
                const match = (filter === 'all') || tokens.includes(filter) || cat.includes(filter);

                wrapper.style.display = match ? '' : 'none';
                if (match) visible++;
            });

            buttons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            if (visible === 0) showNoResults(filter);
            else removeNoResults();
        });
    });

    // trigger 'all' initially
    const first = document.querySelector('.filter-buttons [data-filter="all"]') || buttons[0];
    if (first) first.click();
});




