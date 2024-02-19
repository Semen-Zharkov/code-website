# UDV LLM 

- Генерация тестовых вопросов 
- Поиск ответов на вопросы
- Работа с документами на естественном языке и технической документацией
___
# 🛠️ Getting Started

Чтобы начать использовать это приложение, выберите один из вариантов:

## Docker

### 1. First, ensure you have both Docker and Docker Compose installed.

   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

### 2. Клонируйте репозиторий
Выполните следующую команду в терминале:

   ```bash
   git clone https://github.com/Semen-Zharkov/-code-website.git
   ```
### 3. Перейдите в директорию проекта
   ```bash
   cd code-website
   ```
### 4. Создайте файл окружения
Создайте файл с именем .env и добавьте в него вашу авторизационную информацию следующей командой:
   ```bash
   echo 'AU_DATA=ваши_авторизационные_данные' > .env
   ```

   > **Примечание:** О том, как получить авторизационные данные для доступа к GigaChat, читайте в [официальной документации](https://developers.sber.ru/docs/ru/gigachat/api/integration).

### 5. Запустите приложение с помощью Docker Compose:
   ```bash
   docker compose up
   ```

**Теперь ваш сервер будет работать по адресу http://localhost:5000**

### Чтобы остановить контейнеры Docker, просто запустите:
   ```bash
   docker compose dowm
   ```

## Simply cloning repo

### 1. Установите необходимые зависимости, запустив следующую команду в терминале:
 ```bash
 pip install -r requirements.txt
 ```

### 2. В директории `gigachatAPI` создайте файл `.env` и вставьте в него следующее:

 ```bash
 AU_DATA=ваши_авторизационные_данные
 ```

    