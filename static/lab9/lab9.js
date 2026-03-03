function openGift(giftId) {
    const box = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    if (box.classList.contains('opened')) return showMsg('Уже открыто!', 'warning');
    
    const needAuth = box.dataset.requireAuth === 'true' || box.dataset.requireAuth === '1';
    if (needAuth && !auth()) return showMsg('Войдите в систему!', 'warning');

    fetch('/lab9/open_gift', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gift_id: giftId })
    })
    .then(r => r.json())
    .then(d => {
        if (!d.success) return showMsg(d.message || 'Ошибка', 'error');
        
        document.getElementById('opened-count').textContent = d.opened_count;
        document.getElementById('remaining-count').textContent = d.remaining;
        
        box.innerHTML = `<img src="${d.image}" class="gift-inside" alt="">`;
        box.classList.add('opened');
        
        showModal(d.message, d.image);
        showMsg('Подарок открыт!', 'success');
    })
    .catch(() => showMsg('Ошибка', 'error'));
}

function showModal(msg, img) {
    const m = document.getElementById('gift-modal');
    document.getElementById('modal-message').textContent = msg;
    document.getElementById('modal-image').src = img;
    m.classList.remove('hidden');
}

// Закрытие модалки
document.addEventListener('click', e => {
    if (e.target.matches('.modal-close, #gift-modal')) {
        document.getElementById('gift-modal').classList.add('hidden');
    }
});

let msgTimer;
function showMsg(txt, type='success') {
    let area = document.getElementById('msg-area');
    if (!area) {
        area = document.createElement('div');
        area.id = 'msg-area';
        area.style.cssText = 'position:fixed;top:20px;right:20px;padding:12px 20px;border-radius:8px;z-index:3000;color:white;';
        document.body.appendChild(area);
    }
    const colors = {success:'#4caf50', error:'#f44336', warning:'#ff9800'};
    area.style.background = colors[type];
    area.textContent = txt;
    area.style.display = 'block';
    clearTimeout(msgTimer);
    msgTimer = setTimeout(() => area.style.display = 'none', 3000);
}

function auth() {
    return document.getElementById('auth-status')?.dataset.authenticated === 'true';
}

function resetGifts() {
    if (!confirm('Сбросить подарки?')) return;
    fetch('/lab9/santa', { method: 'POST' })
        .then(r => r.json())
        .then(d => {
            showMsg(d.message, d.success ? 'success' : 'error');
            if (d.success) setTimeout(() => location.reload(), 1500);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.gift-box:not(.opened)').forEach(box => {
        box.addEventListener('click', () => openGift(box.dataset.id));
        
        box.addEventListener('mouseenter', () => {
            box.style.transform = 'scale(1.1)';
            box.style.boxShadow = '0 0 20px gold';
        });
        
        box.addEventListener('mouseleave', () => {
            box.style.transform = 'scale(1)';
            box.style.boxShadow = 'none';
        });
    });
    
    const santaBtn = document.getElementById('santa-btn');
    if (santaBtn) santaBtn.addEventListener('click', resetGifts);
});