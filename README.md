
**FIXPRICE_PARSER**

Установите программу на ваш компьютер, скачав файлы вручную из данного репозитория или из терминала с помощью команды 
`git clone https://github.com/ReptiloidAnunak/fixprice_parser.git`

Убедитесь , что на вашем компьютере установлен хром-браузер. 
Затем перейдите в корневую папку проекта, положите в нее файл .env. 
<br>Запустите в терминале команды:<br>
`python3 -m venv .venv`<br>
`source .venv/bin/activate`<br>
`pip install --upgrade pip`<br>
`pip install -r requirements.txt`<br>
`scrapy crawl fix_price`<br>
<br>
Файл базы данных с результатами находится здесь: db_json/fixprice_result.json
