document.addEventListener('DOMContentLoaded', () => {
    // Получение информации о последней версии с GitHub
    fetch('https://api.github.com/repos/Eugeneofficial/PC-Manager-Bot/releases/latest')
        .then(response => response.json())
        .then(data => {
            // Обновляем информацию о версии
            const versionElements = document.querySelectorAll('.version-info h3');
            const versionInDownloadBox = document.querySelector('.download-box p');
            const downloadButton = document.querySelector('.download-button');
            const releaseDate = document.querySelector('.version-info p');

            if (data.tag_name) {
                const version = data.tag_name.replace('v', '');
                versionElements.forEach(el => el.textContent = `Версия ${version}`);
                versionInDownloadBox.textContent = `Версия ${version} для Windows`;
                
                // Обновляем ссылку на скачивание
                if (data.assets && data.assets[0]) {
                    downloadButton.href = data.assets[0].browser_download_url;
                    // Обновляем размер файла
                    const fileSizeElement = document.querySelector('.file-size');
                    const fileSizeMB = (data.assets[0].size / 1048576).toFixed(1);
                    fileSizeElement.textContent = `Размер: ${fileSizeMB} MB`;
                }

                // Обновляем дату релиза
                const releaseDateTime = new Date(data.published_at);
                const options = { year: 'numeric', month: 'long' };
                releaseDate.textContent = `Последнее обновление: ${releaseDateTime.toLocaleDateString('ru-RU', options)}`;
            }
        })
        .catch(error => console.error('Ошибка при получении данных о релизе:', error));

    // Анимация загрузки главной страницы
    setTimeout(() => {
        document.querySelector('.logo').classList.add('animated');
        
        // Анимация навигационных ссылок с задержкой
        document.querySelectorAll('.nav-links a').forEach((link, index) => {
            setTimeout(() => {
                link.classList.add('animated');
            }, 100 * (index + 1));
        });

        // Анимация hero секции
        const heroContent = document.querySelector('.hero-content');
        const heroTitle = document.querySelector('.hero-content h1');
        const heroText = document.querySelector('.hero-content p');
        const ctaButtons = document.querySelector('.cta-buttons');

        heroContent.classList.add('animated');
        heroTitle.classList.add('animated');
        heroText.classList.add('animated');
        ctaButtons.classList.add('animated');
    }, 100);

    // Плавная прокрутка для навигационных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Переключение табов в документации
    const docsNavItems = document.querySelectorAll('.docs-nav-item');
    const docsTabs = document.querySelectorAll('.docs-tab');

    docsNavItems.forEach(item => {
        item.addEventListener('click', () => {
            // Удаляем активный класс у всех табов и навигационных элементов
            docsNavItems.forEach(navItem => navItem.classList.remove('active'));
            docsTabs.forEach(tab => tab.classList.remove('active'));

            // Добавляем активный класс к выбранному табу
            item.classList.add('active');
            const tabId = item.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');

            // Анимация появления контента
            const activeTab = document.getElementById(tabId);
            activeTab.style.opacity = '0';
            activeTab.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                activeTab.style.opacity = '1';
                activeTab.style.transform = 'translateY(0)';
                activeTab.style.transition = 'all 0.4s ease';
            }, 50);
        });
    });

    // Анимация появления карточек при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.6s ease';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .command-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transitionDelay = `${index * 0.2}s`;
        observer.observe(card);
    });
}); 