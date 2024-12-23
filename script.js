document.addEventListener('DOMContentLoaded', () => {
    // Функция для определения языка пользователя
    function getUserLanguage() {
        const savedLang = localStorage.getItem('preferred_language');
        if (savedLang) return savedLang;
        
        const browserLang = navigator.language.split('-')[0];
        return translations[browserLang] ? browserLang : 'en';
    }

    // Функция для перевода всего контента
    function translatePage(lang) {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const keys = key.split('.');
            let translation = translations[lang];
            
            for (const k of keys) {
                if (translation) {
                    translation = translation[k];
                }
            }
            
            if (translation) {
                if (element.tagName === 'INPUT' && element.type === 'placeholder') {
                    element.placeholder = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });

        // Обновляем активную кнопку языка
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });

        // Сохраняем выбор пользователя
        localStorage.setItem('preferred_language', lang);
    }

    // Инициализация переводов
    const currentLang = getUserLanguage();
    translatePage(currentLang);

    // Обработчики для кнопок переключения языка
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-lang');
            translatePage(lang);
        });
    });

    // Получение информации о релизах с GitHub
    fetch('https://api.github.com/repos/Eugeneofficial/PC-Manager-Bot/releases')
        .then(response => response.json())
        .then(releases => {
            if (releases && releases.length > 0) {
                const latestRelease = releases[0];
                
                const versionElements = document.querySelectorAll('.version-info h3');
                const versionInDownloadBox = document.querySelector('.download-box p');
                const downloadButton = document.querySelector('.download-button');
                const releaseDate = document.querySelector('.version-info p');
                const fileSizeElement = document.querySelector('.file-size');

                const exeAsset = latestRelease.assets.find(asset => 
                    asset.name.endsWith('.exe')
                );

                if (exeAsset) {
                    const version = latestRelease.tag_name.replace('v', '');
                    const currentLang = localStorage.getItem('preferred_language') || getUserLanguage();
                    
                    versionElements.forEach(el => {
                        el.textContent = `${translations[currentLang].download.version} ${version}`;
                    });
                    
                    versionInDownloadBox.textContent = `${translations[currentLang].download.version} ${version} ${translations[currentLang].download.forWindows}`;
                    
                    downloadButton.href = exeAsset.browser_download_url;
                    
                    const fileSizeMB = (exeAsset.size / 1048576).toFixed(1);
                    fileSizeElement.innerHTML = `<span>${translations[currentLang].download.fileSize}: ${fileSizeMB} MB</span>`;
                    
                    const releaseDateTime = new Date(latestRelease.published_at);
                    const options = { year: 'numeric', month: 'long' };
                    releaseDate.textContent = `${translations[currentLang].download.lastUpdate}: ${releaseDateTime.toLocaleDateString(currentLang === 'ru' ? 'ru-RU' : 'en-US', options)}`;

                    if (latestRelease.body && latestRelease.body.includes('FIX UPDATE')) {
                        const updateBadge = document.createElement('div');
                        updateBadge.className = 'update-badge';
                        updateBadge.innerHTML = `<i class="fas fa-sync-alt"></i> ${translations[currentLang].updates.available}`;
                        downloadButton.parentNode.insertBefore(updateBadge, downloadButton);
                    }
                }
            }
        })
        .catch(error => {
            console.error('Ошибка при получении данных о релизах:', error);
            const fileSizeElement = document.querySelector('.file-size');
            const currentLang = localStorage.getItem('preferred_language') || getUserLanguage();
            fileSizeElement.innerHTML = `<span style="color: #ff5722;"><i class="fas fa-exclamation-triangle"></i> ${translations[currentLang].updates.error}</span>`;
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