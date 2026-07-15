(function () {
    const badgeEl = document.getElementById('notificationsBadge');
    const listEl = document.getElementById('notificationsList');
    const emptyEl = document.getElementById('notificationsEmpty');
    const markAllBtn = document.getElementById('markAllReadBtn');
    
    // Read from global config object initialized in base.html
    const markReadTemplate = window.DjangoConfig.markReadTemplate;
    const notificationsFeedUrl = window.DjangoConfig.notificationsFeedUrl;
    const markAllReadUrl = window.DjangoConfig.markAllReadUrl;

    function getCookie(name) {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='));
        return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
    }

    function renderNotifications(data) {
        const unread = Number(data.unread_count || 0);
        if (unread > 0) {
            badgeEl.textContent = unread;
            badgeEl.classList.remove('d-none');
        } else {
            badgeEl.classList.add('d-none');
        }

        const items = Array.isArray(data.items) ? data.items : [];
        if (!items.length) {
            listEl.innerHTML = '';
            emptyEl.classList.remove('d-none');
            return;
        }

        emptyEl.classList.add('d-none');
        listEl.innerHTML = items.map(item => {
            const unreadClass = item.is_read ? '' : 'unread';
            const href = item.link && item.link.trim() ? item.link : '#';
            return `
                <div class="dropdown-item border-bottom notification-item ${unreadClass}" data-id="${item.id}" data-href="${href}">
                    <div class="d-flex justify-content-between align-items-start gap-2">
                        <div>
                            <div class="title">${item.title}</div>
                            <div class="small text-muted">${item.message}</div>
                            <div class="meta mt-1">${item.created}</div>
                        </div>
                        ${item.is_read ? '' : '<span class="badge bg-primary" style="padding:0.2rem 0.4rem; border-radius:999px;">new</span>'}
                    </div>
                </div>
            `;
        }).join('');
    }

    async function markOneRead(notificationId) {
        const url = markReadTemplate.replace('/0/', `/${notificationId}/`);
        await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') || '',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
    }

    async function loadNotifications() {
        if (!notificationsFeedUrl) return;
        try {
            const res = await fetch(notificationsFeedUrl, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
            if (!res.ok) return;
            const data = await res.json();
            renderNotifications(data);
        } catch (e) {
            // Silent failure keeps page UX stable.
        }
    }

    if (markAllBtn) {
        markAllBtn.addEventListener('click', async function () {
            try {
                await fetch(markAllReadUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken') || '',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                loadNotifications();
            } catch (e) {
                // Silent failure keeps page UX stable.
            }
        });
    }

    if (listEl) {
        listEl.addEventListener('click', async function (e) {
            const item = e.target.closest('.notification-item');
            if (!item) {
                return;
            }
            const id = item.getAttribute('data-id');
            const href = item.getAttribute('data-href') || '#';
            try {
                await markOneRead(id);
            } catch (err) {
                // Best effort only.
            }
            if (href !== '#') {
                window.location.href = href;
            } else {
                loadNotifications();
            }
        });
    }

    loadNotifications();
    setInterval(loadNotifications, 10000);
})();
