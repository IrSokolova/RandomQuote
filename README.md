<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/IrSokolova/RandomQuote">
    <img src="лого.png" alt="Logo" width="160" height="160">
  </a>
</div>

<h2 align="center">Генератор случайных цитат</h2>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#getting-started">Getting Started</a></li>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Генератор случайных цитат — это веб-приложение для отображения, добавления и оценки цитат.

Основные возможности:

📜 Случайная цитата — на главной странице отображается случайная цитата с возможностью поставить лайк или дизлайк.

➕ Добавление цитат — пользователи могут добавлять свои цитаты, указывая текст, источник, тип источника (книга, фильм, сериал, известный человек и др.) и вес цитаты (влияет на частоту её появления).

🏆 Топ-10 цитат — раздел, где выводятся самые популярные цитаты, отсортированные по количеству лайков.

📊 Дашборд статистики — админ-панель со сводной аналитикой:

общее количество цитат, просмотров, лайков и дизлайков,

распределение цитат по типам источников,

рейтинг источников по лайкам,

список последних добавленных цитат.


### Built With

Проект создан с использованием следующих технологий:

1. Python 3.9
 — основной язык программирования

2. Django 4.2.23
 — веб-фреймворк для разработки приложения


## Prerequisites

Перед запуском убедитесь, что у вас установлены:

Python 3.9

pip
 (менеджер пакетов Python)

virtualenv
 (рекомендуется для создания изолированного окружения)

Рекомендации:

Создайте и активируйте виртуальное окружение:

```sh
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows
```

## Getting Started

1. Клонируйте репозиторий
   ```sh
   git clone https://github.com/IrSokolova/RandomQuote
   ```
3. Перейдите в директорию проекта
   ```sh
    cd testproject
   ```
4. Установите зависимости
   ```sh
   pip install -r requirements.txt
   ```
5. Создайте файлы миграций
   ```sh
   python manage.py makemigrations
   ```
6. Примените миграции к базе данных
   ```sh
   python manage.py migrate
   ```
7. Запустите сервер разработки
   ```sh
   python manage.py runserver
   ```

После запуска сервер будет доступен по адресу: http://127.0.0.1:8000/
