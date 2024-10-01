## **Часть 1. Готовый докер**

- Взять официальный докер образ с nginx и выкачать его при помощи `docker pull`

	![image info](/src/img/part1/1.png)

- Проверить наличие докер образа через `docker images`

	![image info](/src/img/part1/2.png)

- Запустить докер образ через`docker run -d 2d21d843073b`

	![image info](/src/img/part1/3.png)

- Проверить, что образ запустился через `docker ps`

	![image info](/src/img/part1/4.png)

- Посмотреть информацию о контейнере через `docker inspect cranky_hofstadter`

	![image info](/src/img/part1/5.png)
	![image info](/src/img/part1/6.png)
	![image info](/src/img/part1/7.png)
	![image info](/src/img/part1/8.png)
    ![image info](/src/img/part1/9.png)

- По выводу команды определить и поместить в отчёт размер контейнера, список замапленных портов и ip контейнера:
1. Размер контейнера:\
![image info](/src/img/part1/10.png)
2. Список отображаемых портов:\
![image info](/src/img/part1/11.png)
3. ip контейнеры:\
![image info](/src/img/part1/12.png)

- Остановить докер образ через `docker stop cranky_hofstadter`

![image info](/src/img/part1/13.png)

- Проверить, что образ остановился через `docker ps`

![image info](/src/img/part1/14.png)

- Запустить докер с портами 80 и 443 в контейнере, замапленными на такие же порты на локальной машине, через команду run

![image info](/src/img/part1/15.png)

- Проверить, что в браузере по адресу localhost:80 доступна стартовая страница nginx

![image info](/src/img/part1/16.png)

- Перезапустить докер контейнер через `docker restart run-nginx`

![image info](/src/img/part1/17.png)

## **Часть 2. Операции с контейнером**

 - Прочитать конфигурационный файл *nginx.conf* внутри докер контейнера через команду *exec*

![image info](/src/img/part2/1.png)

- Создать на локальной машине файл *nginx.conf*

![image info](/src/img/part2/2.png)

- Настроить в нем по пути */status* отдачу страницы статуса сервера **nginx**

![image info](/src/img/part2/3.png)

- Скопировать созданный файл *nginx.conf* внутрь докер образа через команду  `cp command`

![image info](/src/img/part2/4.png)

- Перезапустить **nginx** внутри докер образа через команду exec

![image info](/src/img/part2/5.png)

- Проверить, что по адресу *localhost:80/status* отдается страничка со статусом сервера **nginx**

![image info](/src/img/part2/6.png)

- Экспортировать контейнер в файл *container.tar* через команду *export*

![image info](/src/img/part2/7.png)

- Остановить контейнер

![image info](/src/img/part2/8.png)

- Удалить изображение с помощью, docker rmi [image_id|repository]не удаляя сначала контейнер

![image info](/src/img/part2/9.png)

- Удалить остановленный контейнер

![image info](/src/img/part2/10.png)

- Импортируйте контейнер обратно с помощью команды *import*

![image info](/src/img/part2/11.png)

- Запустите импортированный контейнер

![image info](/src/img/part2/12.png)

- Проверить, что по адресу *localhost:80/status* отдается страничка со статусом сервера **nginx**

![image info](/src/img/part2/13.png)

## **Часть 3. Мини веб-сервер**

- Написать мини сервер на *C* и *FastCgi*, который будет возвращать простейшую страничку с надписью **Hello World!**

`docker pull nginx` - загрузить образ nginx  
`docker images` - проверить идентификатор изображения 
`docker run -d -p 80:80 -p 81:81 *IMAGE_ID*` - запустить докер с поставленными портами 

![image info](/src/img/part3/1.png)

1. Поместить файл мини-веб-сервера в каталог

![image info](/src/img/part3/2.png)

2. Содержимое файла `main.c`

![image info](/src/img/part3/3.png)

- Запустить написанный мини сервер через *spawn-fcgi* на порту 8080

1. Обновление контейнера. Установка gcc, spawn-dcgi, libfcgi-dev

![image info](/src/img/part3/4.png)

2. Компилируем и запускаем наш сервер

![image info](/src/img/part3/5.png)

- Написать свой nginx.conf, который будет проксировать все запросы с 81 порта на 127.0.0.1:8080

![image info](/src/img/part3/6.png)

- Проверить, что в браузере по localhost:81 отдается написанная вами страничка

1. Перезагрузка контейнера и проверка страницы в браузере  

![image info](/src/img/part3/7.png)
![image info](/src/img/part3/8.png)

- Положить файл nginx.conf по пути *./nginx/nginx.conf* (это понадобится позже)

![image info](/src/img/part3/9.png)

## **Часть 4. Свой докер**

- Написать свой докер образ

![image info](/src/part4/1.png)

- Запуск через скрипт докера

![image info](/src/part4/2.png)

- Соберать написанный образ докера с помощью *docker build*, указав имя и тег

![image info](/src/part4/3.png)

- Проверяем, `docker images`, что все построено правильно

![image info](/src/part4/4.png)

- Запустить созданный образ докера, сопоставив порты 81 и 80 на локальном компьютере и сопоставив папку *./nginx* внутри контейнера с адресом, где расположены файлы конфигурации nginx.

![image info](/src/part4/5.png)

- Проверить, что страница написанного мини-сервера доступна на localhost:80

![image info](/src/part4/6.png)

- Добавить проксирование страницы /status в ./nginx/nginx.conf для возврата статуса сервера **nginx** .

![image info](/src/part4/7.png)

- Перезапуск образа докера

- Убедится, что localhost:80/status теперь возвращает страницу со статусом **nginx** .

![image info](/src/part4/8.png)

## **Часть 5. Dockle**

- Проверить изображение из предыдущей задачи с помощью докла `[image_id|repository]`

1. Установка **dockle**

![image info](/src/part5/1.png)

2. Сканирование изображения

![image info](/src/part5/2.png)
![image info](/src/part5/3.png)

- Исправить образ, чтобы не было ошибок или предупреждений при проверке с помощью **dockle**

1. Изменение **Dockerfile**

![image info](/src/part5/4.png)

2. Создать новую сборку и убедиться, что образы созданы.

![image info](/src/part5/5.png)

3. Запустить новый докер

![image info](/src/part5/6.png)

4. Проверка нового докера через **dockle**

![image info](/src/part5/7.png)

5. Проверка `localhost:80`

![image info](/src/part5/8.png)

## **Часть 6. Базовая компоновка докера**

- Написать файл docker-compose.yml, используя который:

1. Запустить док-контейнер из части 5 (он должен работать в локальной сети, т.е. вам не нужно использовать инструкцию EXPOSE и сопоставлять порты с локальной машиной)

2. Запустить контейнер Docker с помощью nginx, который будет проксировать все запросы с порта 8080 на порт 81 первого контейнера.

- Сопоставить порт 8080 второго контейнера с портом 80 локальной машины.

![image info](/src/part6/1.png)

- Остановить контейнеры

- Создать и запустить проект с помощью команд `docker-compose build` и `docker-compose up`

![image info](/src/part6/2.png)
![image info](/src/part6/3.png)


- Убедится, что браузер возвращает страницу, которую вы написали на localhost: 80, как и раньше.

![image info](/src/part6/4.png)

