# Отчет об установке Прометея и Графаны

## Установка Прометея:

### 1. Создание пользователя:
`$ sudo useradd --system --no-create-home --shell /bin/false prometheus`

`--system` - Создает системный аккаунт. \
`--no-create-home` - В нашем случае нет необхобходимости в домашней дериктории. \
`--shell /bin/false` - Предотвращение входа в систему как прометей юзер. \
`prometheus` - Создает прометей юзера и группу с таким же именем.

### 2. Загрузка Прометея:

`$ wget https://github.com/prometheus/prometheus/releases/download/v2.32.1/prometheus-2.32.1.linux-amd64.tar.gz`

### 3. Извлечение:

`$ tar -xvf prometheus-2.32.1.linux-amd64.tar.gz`

### 4. Создание директории для Прометея и перестановка пакетов туда:

`$ sudo mkdir -p /data /etc/prometheus` \
`$ cd prometheus-2.32.1.linux-amd64` \
`$ sudo mv prometheus promtool /usr/local/bin/` \
`$ sudo mv prometheus.yml /etc/prometheus/prometheus.yml` 

### 5. Установка права собственности на каталог:

`$ sudo chown -R prometheus:prometheus /etc/prometheus/ /data/`

### 6. Проверка успешной установки и удаление ненужных файлов: 

`$ prometheus --version` \
`$ cd ..` \
`$ rm -rf prometheus*`

### 7. Создание файла конфигурации модуля systemd:

`$ sudo vim /etc/systemd/system/prometheus.service`

_prometheus.service:_

```
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=prometheus
Group=prometheus
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/data \
  --web.listen-address=0.0.0.0:9090 \
  --web.enable-lifecycle

[Install]
WantedBy=multi-user.target
```
`--config.file=/etc/prometheus/prometheus.yml` - Путь к основному фалу конфигурации Прометея. \
`--storage.tsdb.path=/data` - Место для хранения данных. \
`--web.listen-address=0.0.0.0:9090` - Настройка сетевых интерфейсов. \
`--web.enable-lifecycle` - Свободное управление конфигурациями без перезапуска службы.

### 8. Запуск Прометея:

`$ sudo systemctl enable prometheus` - Автоматический запуск Прометея после перезагрузки. \
`$ sudo systemctl start prometheus` - Запуск Прометея. \
`$ sudo systemctl status prometheus` - Проверка статуса Прометея.

_Веб-интерфейс Prometheus с виртуальной машины, доступ к которой осуществляется с локального компьютера.:_ \

![image info](/src/07/img/1.png)

## Установка Node Exporter:

_Node Exporter используется для сбора системных показателей Linux, таких как загрузка процессора и дисковый ввод-вывод. Node Exporter представит их как метрики в стиле Prometheus.._

### 1. Создание пользователя:
`$ sudo useradd --system --no-create-home --shell /bin/false node_exporter`

### 2. Загрузка:

`$ sudo useradd --system --no-create-home --shell /bin/false node_exporter`

### 3. Извлечение:

`$ tar -xvf node_exporter-1.3.1.linux-amd64.tar.gz`

### 4. Перемещение и чистка:

`$ sudo mv node_exporter-1.3.1.linux-amd64/node_exporter /usr/local/bin/` \
`$ rm -rf node_exporter*`

### 5. Проверка версии:

`$ node_exporter --version`

### 6. Создение файла конфигурации:

`$ sudo vim /etc/systemd/system/node_exporter.service`

_node_exporter.service:_

```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=node_exporter
Group=node_exporter
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/node_exporter \
    --collector.logind

[Install]
WantedBy=multi-user.target
```

### 7. Запуск Node Exporter:

`$ sudo systemctl enable node_exporter` - Для атоматического запуска после перезапуска. \
`$ sudo systemctl start node_exporter` - Запуск. \
`$ sudo systemctl status node_exporter` - Проверка статуса. 

### 8. Создание статической цели:

`$ sudo vim /etc/prometheus/prometheus.yml` 

_prometheus.yml:_

```
...
  - job_name: node_export
    static_configs:
      - targets: ["localhost:9100"]
```

_Targets in Prometheus web UI:_ \

![image info](/src/07/img/2.png)

## Установка Grafana:

### 1. Установка:
`$ sudo apt-get install -y apt-transport-https software-properties-common`

### 2. Добавление ключа GPG:

`$ get -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -`

### 3. Добавление этого репозитория для стабильных выпусков:
`$ echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list`

### 4. Обновление и установка Grafana:

`$ udo apt-get update`\
`$sudo apt-get -y install grafana`

### 5. Запуск Grafana:

`$sudo systemctl enable grafana-server` - Для автоматического запуска после перезагрузки. \
`$sudo systemctl start grafana-server` - Запуск. \
`$sudo systemctl status grafana-server` - Проверка статуса.

_Grafana web UI from virtual machine accessed from local:_ \
![image info](/src/07/img/3.png)

## Изучение Grafana:

_Добавлены метрики (ЦП, доступная оперативная память, свободное место и количество операций ввода-вывода на жестком диске, используемое пространство, сетевой трафик):_ \
![image info](/src/07/img/4.png)

_Скрипт для заполнения свободного дискового пространства сервера до 1Гб остался выполненным:_ \
![image info](/src/07/img/5.png)

## Утилита Stress: 

### Устаовка утилиты:
`$ sudo apt install -y stress`

### Запуск утилиты:
`$ stress -c 2 -i 1 -m 1 --vm-bytes 32M -t 10s`

![image info](/src/07/img/6.png)