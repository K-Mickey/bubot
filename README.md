## Установка
1. Скопируйте и настройте переменные окружения: `cp .env.example .env`
2. Поместите `google_creds.json` в папку `bin/` - документ с ключами, который можно получить в кабинете гугл
разработчика
3. Постройте образ: `docker build -t bubot .`
4. Запустите контейнер: `docker run -d bubot` или
`docker run -d --name bubot --restart always -v /opt/bubot:/usr/src bubot:latest`
