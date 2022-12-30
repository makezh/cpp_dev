================================================================

## Разбор JSON

Студент (выполнил): __М. Кежаев__  
Студент (проверил): __А. Усцов__

Преподаватель: __Ф.Петряйкин__

### Описание:

Реализуйте разбор JSON. Каждая Node может быть:
- Словарем: name (string) <-> Node
- Массивом [Node]
- Числом
- Строкой
  
Нужно сделать метод установления типа Node, а также вывода на экран (т.е. когда рекурсивно распечатывается Node). Пробелы и новые строки должны игнорироваться.


Ссылка на распределение - [здесь](https://docs.google.com/spreadsheets/d/1SBwOcvxeQsJSgYD9QoMnDZc5UwioBjbNM4z8Ojmn25Y/edit#gid=0)

__Code:__
- ЯП: C++20
- Codestyle: snake_case, format=Google

__Решение:__
Работа будет осуществляться с чтением из консоли строки в формате json.

В качестве решения будет представлен класс JSONValue, 
который будет содержать в себе все возможные типы данных, 
которые могут быть в json. 

---

Также будет реализована функция parse, 
которая будет принимать строку в формате json и 
возвращать пару из JSONValue и строки с ошибкой. 
~~~cpp
std::tuple<json::JSONValue, std::string> parse(std::string);
~~~
_В случае ошибки парсинга, второй элемент пары будет содержать 
строку с описанием ошибки. В случае успеха, второй элемент пары будет пустой._
---

Также будет реализована функция deparse, 
которая будет принимать JSONValue и возвращать строку в формате json. 
~~~cpp
std::string deparse(json::JSONValue);
~~~
_В случае ошибки парсинга, функция вернет пустую строку._

---

## Запуск

~~~bash
sudo apt-get update && sudo apt-get install -y gcc g++
sudo apt-get update && sudo apt-get install -y cmake
sudo apt-get update && sudo apt-get install -y valgrind
sudo apt-get update && sudo apt-get install -y lcov
sudo apt-get update && sudo apt-get install -y python3-pip
~~~

Сборка проекта (динамическая библиотека, включение тестов, включение покрытия)
~~~bash
mkdir build && cd build
sudo cmake -DBUILD_DYNAMIC=ON ..
make
~~~

Запуск программы
~~~bash
./parse_json "$(cat ../data/*insert json file*)"  
~~~

Запуск интеграционных тестов
(Запускать из главной директории проекта)
~~~bash
python3 test/integrity_tests.py
~~~