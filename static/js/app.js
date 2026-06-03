/*
 * DecodeLabs Project 3 - Database Integration
 * Interactive JavaScript | Batch 2026
 */

document.addEventListener('DOMContentLoaded', function() {

    // ═══════════════════════════════════════════════════════════════
    // SIDEBAR TOGGLE (Mobile)
    // ═══════════════════════════════════════════════════════════════
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');

            // Create overlay if doesn't exist
            let overlay = document.querySelector('.sidebar-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.className = 'sidebar-overlay';
                document.body.appendChild(overlay);

                overlay.addEventListener('click', function() {
                    sidebar.classList.remove('open');
                    overlay.classList.remove('active');
                });
            }

            if (sidebar.classList.contains('open')) {
                overlay.classList.add('active');
            } else {
                overlay.classList.remove('active');
            }
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // AUTO-DISMISS FLASH MESSAGES
    // ═══════════════════════════════════════════════════════════════
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });

    // ═══════════════════════════════════════════════════════════════
    // ANIMATE PROGRESS BARS ON LOAD
    // ═══════════════════════════════════════════════════════════════
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function() {
            bar.style.width = width;
        }, 300);
    });

    // ═══════════════════════════════════════════════════════════════
    // ANIMATE PROGRESS RINGS
    // ═══════════════════════════════════════════════════════════════
    const progressRings = document.querySelectorAll('.progress-ring, .progress-circle');
    progressRings.forEach(function(ring) {
        const bar = ring.querySelector('.progress-bar');
        if (bar) {
            const dashArray = bar.getAttribute('stroke-dasharray');
            bar.setAttribute('stroke-dasharray', '0, 100');
            setTimeout(function() {
                bar.style.transition = 'stroke-dasharray 1s ease';
                bar.setAttribute('stroke-dasharray', dashArray);
            }, 500);
        }
    });

    // ═══════════════════════════════════════════════════════════════
    // STAT CARDS ANIMATION
    // ═══════════════════════════════════════════════════════════════
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(function() {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // ═══════════════════════════════════════════════════════════════
    // PROJECT CARDS ANIMATION
    // ═══════════════════════════════════════════════════════════════
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(function() {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease, box-shadow 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 80);
    });

    // ═══════════════════════════════════════════════════════════════
    // TASK CARDS ANIMATION
    // ═══════════════════════════════════════════════════════════════
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateX(-20px)';
        setTimeout(function() {
            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateX(0)';
        }, index * 60);
    });

    // ═══════════════════════════════════════════════════════════════
    // TABLE ROWS ANIMATION
    // ═══════════════════════════════════════════════════════════════
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(function(row, index) {
        row.style.opacity = '0';
        setTimeout(function() {
            row.style.transition = 'opacity 0.3s ease';
            row.style.opacity = '1';
        }, index * 50);
    });

    // ═══════════════════════════════════════════════════════════════
    // FORM INPUT FOCUS EFFECTS
    // ═══════════════════════════════════════════════════════════════
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // CONFIRM DELETE WITH CUSTOM DIALOG
    // ═══════════════════════════════════════════════════════════════
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm(this.getAttribute('onsubmit').match(/return confirm\('(.+?)'\)/)[1])) {
                e.preventDefault();
            }
        });
        form.removeAttribute('onsubmit');
    });

    // ═══════════════════════════════════════════════════════════════
    // SCROLL TO TOP BUTTON
    // ═══════════════════════════════════════════════════════════════
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-top';
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
        opacity: 0;
        transform: translateY(20px);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.transform = 'translateY(0)';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.transform = 'translateY(20px)';
        }
    });

    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ═══════════════════════════════════════════════════════════════
    // ACTIVE NAV ITEM INDICATOR
    // ═══════════════════════════════════════════════════════════════
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(function(item) {
        const href = item.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            item.classList.add('active');
        } else if (currentPath === '/' && href === '/') {
            item.classList.add('active');
        }
    });

    // ═══════════════════════════════════════════════════════════════
    // CARD HOVER EFFECT ENHANCEMENT
    // ═══════════════════════════════════════════════════════════════
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // LOADING STATE FOR BUTTONS
    // ═══════════════════════════════════════════════════════════════
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                this.disabled = true;

                // Re-enable after 3 seconds (fallback)
                setTimeout(function() {
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                }, 3000);
            }
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // TOOLTIP FOR ICON BUTTONS
    // ═══════════════════════════════════════════════════════════════
    const iconButtons = document.querySelectorAll('[title]');
    iconButtons.forEach(function(btn) {
        btn.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('title');
            tooltip.style.cssText = `
                position: fixed;
                background: var(--gray-800);
                color: white;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 0.8rem;
                white-space: nowrap;
                z-index: 3000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s ease;
            `;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';

            requestAnimationFrame(function() {
                tooltip.style.opacity = '1';
            });

            this._tooltip = tooltip;
        });

        btn.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });

    // ═══════════════════════════════════════════════════════════════
    // SEARCH FILTER FOR TABLES (if search input exists)
    // ═══════════════════════════════════════════════════════════════
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('.data-table tbody tr');

            tableRows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // PRINT STYLES
    // ═══════════════════════════════════════════════════════════════
    const printBtn = document.querySelector('.print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }

    console.log('✅ DecodeLabs Project 3 - App loaded successfully!');
});

// ═══════════════════════════════════════════════════════════════
// GLOBAL FUNCTIONS
// ═══════════════════════════════════════════════════════════════

function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function editTask(id, title, description, status, priority, projectId) {
    const form = document.getElementById('editTaskForm');
    if (form) {
        form.action = '/tasks/' + id + '/update';
        document.getElementById('editTitle').value = title;
        document.getElementById('editDescription').value = description;
        document.getElementById('editStatus').value = status;
        document.getElementById('editPriority').value = priority;
        document.getElementById('editTaskModal').style.display = 'flex';
    }
}

function editIntern(id, name, email, role, skills, bio, isActive) {
    const form = document.getElementById('editInternForm');
    if (form) {
        form.action = '/interns/' + id + '/update';
        document.getElementById('editInternName').value = name;
        document.getElementById('editInternEmail').value = email;
        document.getElementById('editInternRole').value = role;
        document.getElementById('editInternSkills').value = skills;
        document.getElementById('editInternBio').value = bio;
        document.getElementById('editInternActive').checked = isActive;
        document.getElementById('editInternModal').style.display = 'flex';
    }
}

function closeInternModal() {
    const modal = document.getElementById('editInternModal');
    if (modal) {
        modal.style.display = 'none';
    }
}
