# SQLStream
SQL Streaming Data

Описание проекта
Этот проект представляет собой систему для анализа потоковых данных событий веб-страницы в реальном времени. Система моделирует интернет-магазин, где пользователи генерируют события (просмотры страниц — view, клики — click), отправляемые в Apache Kafka, обрабатываемые Apache Flink с использованием SQL и анализируемые альтернативно с помощью Python. Цель — подсчёт количества событий по типам за 5-минутные временные окна для сравнения производительности подходов Flink SQL и Python.
Основные компоненты

    Apache Kafka (3.6.1): Распределённая система для передачи и хранения событий.
    Apache Flink (1.19.1, Scala 2.12): Платформа для потоковой обработки данных с использованием Flink SQL.
    Flask-приложение: Веб-сайт для генерации событий.
    Python-скрипты: Альтернативный анализ с использованием kafka-python.

Версии зависимостей

    Kafka: 3.6.1
    Flink: 1.19.1 (Scala 2.12)
    Flink Kafka Connector: 3.2.0-1.19
    Python: 3.x (с библиотеками flask и kafka-python)

Установка и настройка
Требования

    Операционная система: Linux (WSL 2 на Windows 10/11, Ubuntu).
    Java: Oracle JDK 11 или OpenJDK 11.
    Python: 3.8 или новее.
    Установленные пакеты:
        wget, unzip, python3, python3-pip, apt.

Установка компонентов
1. Установка Apache Kafka (3.6.1)

    Скачивание и распаковка:
        Перейдите в домашнюю директорию:
        bash

cd ~

Скачайте Kafka 3.6.1:
bash

    wget https://kafka.apache.org/downloads/kafka_2.13-3.6.1.tgz
    tar -xzf kafka_2.13-3.6.1.tgz
    mv kafka_2.13-3.6.1 kafka

    Убедитесь, что путь установлен (например, /home/test/kafka/).

Запуск Kafka:

    Требуются два терминала WSL:
        Первый терминал (Zookeeper):
        bash

~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties &

Второй терминал (Kafka):
bash

    ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties &

Проверьте процессы:
bash

    ps aux | grep kafka

Создание топика:

    В любом терминале создайте топик для событий:
    bash

        ~/kafka/bin/kafka-topics.sh --create --topic website_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

2. Установка Apache Flink (1.19.1)

    Скачивание и распаковка:
        Скачайте Flink 1.19.1:
        bash

    wget https://archive.apache.org/dist/flink/flink-1.19.1/flink-1.19.1-bin-scala_2.12.tgz
    tar -xzf flink-1.19.1-bin-scala_2.12.tgz
    mv flink-1.19.1 flink

    Убедитесь, что путь установлен (например, /home/test/flink/).

Установка Kafka-коннектора:

    Скачайте и установите flink-connector-kafka-3.2.0-1.19.jar:
    bash

    wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/3.2.0-1.19/flink-connector-kafka-3.2.0-1.19.jar
    mv flink-connector-kafka-3.2.0-1.19.jar ~/flink/lib/

    Убедитесь, что версия совместима с Scala 2.12 (имя файла должно содержать _2.12).

Запуск Flink:

    Запустите локальный кластер:
    bash

        ~/flink/bin/start-cluster.sh

        Проверьте веб-интерфейс: http://localhost:8081.

3. Установка Python-зависимостей

    Установите Python и необходимые библиотеки:
    bash

    sudo apt update
    sudo apt install python3 python3-pip -y
    pip3 install flask kafka-python

Конфигурация
Конфигурация Kafka

    Файл ~/kafka/config/server.properties:
        Убедитесь, что listeners=PLAINTEXT://:9092 настроен.
        num.io.threads и num.network.threads могут быть увеличены для повышения производительности.
    Файл ~/kafka/config/zookeeper.properties:
        Убедитесь, что dataDir=/tmp/zookeeper настроен (или измените на другой путь).

Конфигурация Flink

    Файл ~/flink/conf/flink-conf.yaml:
        Настройте jobmanager.rpc.address: localhost.
        Установите taskmanager.numberOfTaskSlots: 1 для локального тестирования.
        Убедитесь, что parallelism.default: 1 для начального тестирования.

Конфигурация веб-приложения и Python-скриптов

    Все файлы размещены в /home/test/.
    Убедитесь, что пути к шаблонам (templates/) корректны в файле website.py.
    Код доступен в отдельных файлах: website.py, templates/home.html, templates/product.html, analyze.py (см. инструкции по использованию).

Использование
Запуск системы

    Запустите Kafka (см. раздел "Установка").
    Запустите Flink (см. раздел "Установка").
    Создайте или проверьте файлы в /home/test/:
        Скопируйте или создайте файлы website.py, templates/home.html, templates/product.html, analyze.py (см. инструкции по установке и примеры кода в документации проекта).
    Запустите веб-приложение:
    bash

python3 ~/website.py

    Откройте http://localhost:5000 в браузере и взаимодействуйте с сайтом (переходите по ссылкам и кликайте).

Запустите Flink SQL Client:
bash

~/flink/bin/sql-client.sh

    Выполните SQL-запросы, описанные в документации проекта (доступны в отдельном файле или проекте).

Запустите Python-анализ:
bash

    python3 ~/analyze.py

Тестирование

    Генерируйте события (1000 событий/мин) в течение 10 минут, взаимодействуя с сайтом.
    Измерьте производительность:
        Латентность: Используйте time для измерения времени обработки запросов в Flink SQL и Python-скриптах.
        CPU: Используйте top в WSL для мониторинга использования ресурсов.
    Сравните результаты Flink SQL и Python, фиксируя точность подсчётов событий и время обработки (см. примеры метрик в документации проекта).

Отладка и устранение неисправностей
Общие ошибки

    Kafka не запускается: Проверьте, запущен ли Zookeeper, и убедитесь, что порты (2181 для Zookeeper, 9092 для Kafka) свободны. Проверьте логи в /home/test/kafka/logs/.
    Flink не видит Kafka: Убедитесь, что flink-connector-kafka-3.2.0-1.19.jar находится в ~/flink/lib/ и перезапустите Flink. Проверьте логи в /home/test/flink/log/.
    Ошибки JSON в Flink: Проверьте данные в Kafka через kafka-console-consumer.sh --topic website_events --bootstrap-server localhost:9092 --from-beginning. Убедитесь, что website.py отправляет корректный JSON (например, {"event_type": "view", "page": "/home", "ts": 1677050132000}).
    Python не подключается к Kafka: Проверьте настройки bootstrap_servers в website.py и analyze.py. Убедитесь, что Kafka запущена и доступна на localhost:9092.

Логи

    Kafka: Логи доступны в /home/test/kafka/logs/.
    Flink: Логи доступны в /home/test/flink/log/.
    Python: Выводятся в консоль при запуске website.py и analyze.py.

Лицензия
Проект распространяется под лицензией MIT. См. файл LICENSE (если требуется, добавьте его в репозиторий).
Контакты для поддержки

    Автор: Дацык Р.В. (r.datsyk@spbu.ru)
    Руководитель: Профессор Богданов А.В. (a.bogdanov@spbu.ru)
    Репозиторий: [Не указан, создайте на GitHub/GitLab для открытого доступа]
