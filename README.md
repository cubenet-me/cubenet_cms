# CubeNet CMS

cms с бэкендом на FastAPI и фронтендом на Vite/React.

## Требования
- Python 3.10+
- Node.js 18+
- npm 8+
- (Опционально) Nginx для обслуживания статических файлов

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/cubenet-me/cubenet_cms.git
   cd cubenet_cms
   ```

2. **Настройте виртуальное окружение (бэкенд)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или .\venv\Scripts\activate  # Windows
   ```

3. **Установите зависимости бэкенда**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Проверьте `roles.json`**:
   Убедитесь, что файл `engine/core/security/role/roles.json` существует:
   ```json
   {
       "roles": {
           "admin": {"permissions": 100},
           "moderator": {"permissions": 50},
           "user": {"permissions": 10}
       }
   }
   ```

6. **Установите зависимости фронтенда**:
   Перейдите в папку `web/`:
   ```bash
   cd web
   npm install
   cd ..
   ```

## Запуск

1. **Запустите бэкенд**:
   ```bash
   uvicorn engine.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - API: `http://localhost:8000`
   - Swagger: `http://localhost:8000/docs`
   - Redoc: `http://localhost:8000/redoc`

2. **Запустите фронтенд**:
   ```bash
   cd web
   npm run dev
   ```
   - Фронтенд: `http://localhost:5173` (порт указан в `web/vite.config.js`)

## Настройка Nginx (опционально)
Для обслуживания фронтенда через Nginx:

1. Установите Nginx:
   ```bash
   sudo pacman -S nginx  # Arch Linux
   # или sudo apt install nginx  # Ubuntu
   ```

2. Настройте конфигурацию (`/etc/nginx/nginx.conf`):
   ```nginx
   server {
       listen 80;
       server_name localhost;

       root /path/to/cubenet_cms/web;
       index index.html;

       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location / {
           try_files $uri $uri/ /index.html;
       }
   }
   ```

3. Перезапустите Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

## Структура проекта
```
cubenet_cms/
├── engine/                    # Бэкенд (FastAPI)
│   ├── api/                  # Публичные API-роутеры
│   │   ├── public/
│   │   │   ├── example/
│   │   │   └── launcher/
│   │   └── loader.py
│   ├── core/                 # Ядро
│   │   ├── config/          # Настройки
│   │   ├── events/          # События и middleware
│   │   ├── logger/          # Логирование
│   │   ├── security/        # Аутентификация и роли
│   │   └── loader.py        # Динамическая загрузка модулей
│   └── main.py              # Точка входа FastAPI
├── web/                     # Фронтенд (Vite/React)
│   ├── src/                # Исходники React
│   │   ├── components/     # Компоненты (Header, Footer)
│   │   ├── styles/         # CSS
│   │   └── App.jsx         # Главный компонент
│   ├── index.html          # Точка входа фронтенда
│   ├── vite.config.js      # Конфигурация Vite
│   └── package.json        # Зависимости фронтенда
├── requirements.txt         # Зависимости бэкенда
├── README.md          # Документация
└── upload.sh               # Скрипт для деплоя
```

## Возможные проблемы
- **Бэкенд не запускается**:
  - Проверьте `.env` и `roles.json`.
  - Убедитесь, что установлены зависимости: `pip install -r requirements.txt`.
  - Проверьте синтаксис в `engine/core/config/config.py`.
- **Фронтенд не запускается**:
  - Убедитесь, что зависимости установлены: `cd web && npm install`.
  - Проверьте `vite.config.js` на корректность.
- **CORS-ошибки**: CORS настроен для всех источников (`*`) в `engine/core/events/middleware.py`.