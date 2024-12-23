document.addEventListener('DOMContentLoaded', () => {
    // Получение информации о релизах с GitHub
    fetch('https://api.github.com/repos/Eugeneofficial/PC-Manager-Bot/releases')
        .then(response => response.json())
        .then(releases => {
            if (releases && releases.length > 0) {
                // Берем последний релиз (первый в массиве)
                const latestRelease = releases[0];
                
                // Обновляем информацию о версии
                const versionElements = document.querySelectorAll('.version-info h3');
                const versionInDownloadBox = document.querySelector('.download-box p');
                const downloadButton = document.querySelector('.download-button');
                const releaseDate = document.querySelector('.version-info p');
                const fileSizeElement = document.querySelector('.file-size');

                // Находим .exe файл в ассетах
                const exeAsset = latestRelease.assets.find(asset => 
                    asset.name.endsWith('.exe')
                );

                if (exeAsset) {
                    // Обновляем версию
                    const version = latestRelease.tag_name.replace('v', '');
                    versionElements.forEach(el => el.textContent = `Версия ${version}`);
                    versionInDownloadBox.textContent = `Версия ${version} для Windows`;
                    
                    // Обновляем ссылку на скачивание
                    downloadButton.href = exeAsset.browser_download_url;
                    
                    // Обновляем размер файла
                    const fileSizeMB = (exeAsset.size / 1048576).toFixed(1);
                    fileSizeElement.innerHTML = `<span>Размер: ${fileSizeMB} MB</span>`;
                    
                    // Обновляем дату релиза
                    const releaseDateTime = new Date(latestRelease.published_at);
                    const options = { year: 'numeric', month: 'long' };
                    releaseDate.textContent = `Последнее обновление: ${releaseDateTime.toLocaleDateString('ru-RU', options)}`;

                    // Добавляем информацию о новой версии, если это обновление
                    if (latestRelease.body && latestRelease.body.includes('FIX UPDATE')) {
                        const updateBadge = document.createElement('div');
                        updateBadge.className = 'update-badge';
                        updateBadge.innerHTML = '<i class="fas fa-sync-alt"></i> Доступно обновление';
                        downloadButton.parentNode.insertBefore(updateBadge, downloadButton);
                    }
                }
            }
        })
        .catch(error => {
            console.error('Ошибка при получении данных о релизах:', error);
            // Показываем сообщение об ошибке пользователю
            const fileSizeElement = document.querySelector('.file-size');
            fileSizeElement.innerHTML = '<span style="color: #ff5722;"><i class="fas fa-exclamation-triangle"></i> Ошибка загрузки данных</span>';
        });

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