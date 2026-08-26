// ---------- Utilities ----------
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
  return null;
}

function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove('show'), 3200);
}

// ---------- Mobile nav ----------
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
    });
  }
});

// ---------- Order placement (dummy backend call + dummy delivery) ----------
async function placeOrder(itemId, btn, statusElId) {
  const statusEl = document.getElementById(statusElId);
  const csrftoken = getCookie('csrftoken');

  btn.disabled = true;
  const originalLabel = btn.textContent;
  btn.textContent = 'Placing order...';

  try {
    const res = await fetch(`/order/${itemId}/place/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
    });
     const data = await res.json();

    if (data.success) {
      btn.textContent = '✅ Order Placed';
      if (statusEl) {
        statusEl.textContent = 'Order placed — preparing your food...';
        statusEl.className = 'order-status placed';
      }
      showToast(`Order placed for ${data.item_name}!`);
      updateTracker(statusElId, 'placed');

      // Dummy delivery simulation (client-side, for demo purposes)
      setTimeout(() => {
        if (statusEl) {
          statusEl.textContent = '🎉 Delivered! Enjoy your meal.';
          statusEl.className = 'order-status delivered';
        }
        btn.textContent = '🎉 Delivered';
        showToast(`${data.item_name} delivered (demo)!`);
        updateTracker(statusElId, 'delivered');
      }, 3000);
    } else {
      btn.disabled = false;
      btn.textContent = originalLabel;
      showToast('Something went wrong. Please try again.');
    }
  } catch (err) {
    btn.disabled = false;
    btn.textContent = originalLabel;
    showToast('Network error — could not place order.');
  }
}

function updateTracker(statusElId, stage) {
  const tracker = document.querySelector(`[data-tracker-for="${statusElId}"]`);
  if (!tracker) return;
  const steps = tracker.querySelectorAll('.step');
  const order = ['placed', 'preparing', 'delivered'];
  const idx = stage === 'placed' ? 1 : order.indexOf(stage) + 1;
  steps.forEach((step, i) => {
    step.classList.toggle('done', i < (stage === 'placed' ? 2 : 3));
  });
}

// ---------- Menu category filter (client-side, no reload) ----------
function filterMenu(category, btn) {
  document.querySelectorAll('.filter-pill').forEach((p) => p.classList.remove('active'));
  btn.classList.add('active');

  document.querySelectorAll('.menu-grid .card').forEach((card) => {
    const cat = card.getAttribute('data-category');
    card.style.display = category === 'all' || cat === category ? '' : 'none';
  });
}