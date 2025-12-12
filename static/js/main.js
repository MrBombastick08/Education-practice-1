// main.js - Клиентский JavaScript для интерактивности интерфейса

document.addEventListener('DOMContentLoaded', function() {
    console.log('Приложение "Комфорт" загружено');

    // 1. Функция подтверждения при удалении
    setupDeleteConfirmation();
    
    // 2. Подсветка активного пункта меню
    highlightActiveMenu();
    
    // 3. Валидация форм
    setupFormValidation();
    
    // 4. Динамическое обновление интерфейса
    setupDynamicUI();
    
    // 5. Фиксация sidebar при скролле
    setupFixedSidebar();
});

// Функция для настройки подтверждения при удалении
function setupDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-delete, .btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const action = button.dataset.action || 'удалить этот элемент';
            if (!confirm(`Вы уверены, что хотите ${action}? Это действие нельзя отменить.`)) {
                e.preventDefault();
            }
        });
    });
}

// Функция для подсветки активного пункта меню
function highlightActiveMenu() {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a, .nav-menu a, .logo');
    
    menuLinks.forEach(link => {
        const linkPath = link.tagName === 'A' ? new URL(link.href).pathname : '/';
        
        // Сравниваем пути с учетом возможных параметров
        if (currentPath.startsWith(linkPath) || (link.classList && link.classList.contains('logo') && currentPath === '/')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Функция для валидации форм
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const formData = new FormData(form);
            
            // Валидация стоимости (не может быть отрицательной)
            if (formData.has('min_cost_for_partner')) {
                const costStr = formData.get('min_cost_for_partner').replace(',', '.');
                const cost = parseFloat(costStr);
                if (isNaN(cost) || cost < 0) {
                    alert('Стоимость не может быть отрицательной или пустой');
                    isValid = false;
                }
            }
            
            // Валидация параметров (должны быть положительными числами)
            if (formData.has('param1') || formData.has('param2')) {
                const param1Str = formData.get('param1') ? formData.get('param1').replace(',', '.') : '0';
                const param2Str = formData.get('param2') ? formData.get('param2').replace(',', '.') : '0';
                const param1 = parseFloat(param1Str);
                const param2 = parseFloat(param2Str);
                
                if ((param1 <= 0 && formData.has('param1')) || 
                    (param2 <= 0 && formData.has('param2'))) {
                    alert('Параметры должны быть положительными числами');
                    isValid = false;
                }
            }
            
            // Валидация количества (для калькулятора)
            if (formData.has('quantity')) {
                const quantity = parseInt(formData.get('quantity'));
                if (isNaN(quantity) || quantity <= 0) {
                    alert('Количество должно быть положительным целым числом');
                    isValid = false;
                }
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// Функция для динамического обновления интерфейса
function setupDynamicUI() {
    // Добавление плавных переходов для таблиц
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach((row, index) => {
        row.style.transition = 'all 0.3s ease';
        row.style.opacity = '0';
        row.style.transform = 'translateY(10px)';
        
        // Появление строк с задержкой для эффекта
        setTimeout(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, 100 + index * 30);
    });
    
    // Обработка закрытия уведомлений
    const closeButtons = document.querySelectorAll('.alert .close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });
    
    // Отображение уведомлений при загрузке
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            alert.style.opacity = '0.8';
        }, 100);
        
        // Автоматическое скрытие уведомлений через 5 секунд
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
}

// Функция для фиксации sidebar при скролле
function setupFixedSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const footer = document.querySelector('.footer');
    
    if (sidebar && content && footer) {
        // Устанавливаем высоту sidebar на всю высоту контента
        const updateSidebarHeight = () => {
            const contentHeight = content.offsetHeight;
            const footerHeight = footer.offsetHeight;
            const viewportHeight = window.innerHeight;
            
            // Устанавливаем минимальную высоту sidebar
            sidebar.style.minHeight = `${Math.max(contentHeight, viewportHeight - 70 - footerHeight)}px`;
        };
        
        // Обновляем высоту при загрузке и изменении размера окна
        updateSidebarHeight();
        window.addEventListener('resize', updateSidebarHeight);
        
        // Фиксируем позицию footer
        const updateFooterPosition = () => {
            const contentHeight = content.offsetHeight;
            const viewportHeight = window.innerHeight;
            const headerHeight = document.querySelector('.header').offsetHeight;
            
            if (contentHeight < viewportHeight - headerHeight - footer.offsetHeight) {
                footer.style.position = 'fixed';
                footer.style.bottom = '0';
                footer.style.width = 'calc(100% - 250px)';
                content.style.paddingBottom = `${footer.offsetHeight + 20}px`;
            } else {
                footer.style.position = 'static';
                content.style.paddingBottom = '60px';
            }
        };
        
        // Обновляем позицию footer при загрузке и изменении размера окна
        updateFooterPosition();
        window.addEventListener('resize', updateFooterPosition);
    }
}

// Функция для плавной прокрутки к элементу
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Функция для обновления данных без перезагрузки страницы
// (для будущего расширения функционала)
function refreshData(containerId, url) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Загрузка...</div>';
    
    fetch(url)
        .then(response => response.text())
        .then(data => {
            container.innerHTML = data;
            // Повторно инициализируем обработчики событий для новых элементов
            setupDeleteConfirmation();
            setupFormValidation();
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных:', error);
            container.innerHTML = '<div class="error">Ошибка при загрузке данных</div>';
        });
}

// Экспортируем функции для возможного использования в других скриптах
window.app = {
    scrollToElement: scrollToElement,
    refreshData: refreshData,
    highlightActiveMenu: highlightActiveMenu
};