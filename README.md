# Архиватор

## Краткая информация
В данном задании вам предстоит реализовать программу, кодирующую и декодирующую текстовые данные. В зависимости от выбранного варианта задания, помимо кодирования, будет производиться более или менее эффективное сжатие данных. Программа будет состоять из двух частей: кодирующей и декодирующей.
Обязательно прочтите задание целиком, даже если собираетесь выполнять вариант на “5”. В каждом варианте могут быть полезные советы, которые помогут вам при выполнении задания.
Помните, что по статистике чем проще код, тем меньше в нем ошибок. Избегайте копирования сложных конструкций, которые вам непонятны.
Оценка за задание пойдет во 2-е полугодие.

## Сроки сдачи
Напомню, что для того, чтобы сдать задание, необходимо добавить вашего преподавателя с правами `Reporter` в ваш проект до наступления дедлайна. Дедлайн означает время, до которого можно сделать последний коммит в свой проект:
- Группы 10-1 и 10-3: 09.01.2023 23:59
- Группы 10-2, 10-4 и 10-5: 10.01.2023 23:59

## Требования к программе
Вне зависимости от выбранного варианта задания, программа должна удовлетворять следующему набору требований (в случае их несоблюдения будет высталена оценка "2" вне зависимости от оценки, на которую претендует ученик).

### Оформление кода
Код должен соответствовать `pep8` и проходить соответствующую проверку `flake8`, как это было с первым заданием практикума.

### Запуск программы
Программа должна запускаться с двумя аргументами командной строки (при выполнении вариантов задания на "3" и "4") и с тремя аргументами привыполнении задания на "5". Первый из них указывает режим запуска программы, второй -- имя файла, третий -- ключ шифрования.<br>
Примеры запуска программы:<br>
Кодирование файла example.txt:<br>
`> python main.py -e example.txt`<br>
Декодирование файла example.par:<br>
`> python main.py -d example.par`

Про использование аргументов командной строки можно прочитать [тут](https://foxford.ru/wiki/informatika/analiz-argumentov-komandnoy-stroki-v-python).

### Результат работы программы
Результатом работы программы должен быть новый файл. Его имя должно соответствовать имени исходного файла, расширение требуется указать соответствующим режиму, в котором была запущена программа. Например, мы попросили программу закодировать файл `abc.txt` с помощью такой команды: `python3 main.py -e abc.txt`. В результате работы программа должна создать новый файл, содержащий закодированный текст, с названием `abc.par`.

### Тестирование программы
Как и первое задание практикума, это задание будет тестироваться при помощи автоматических тестов. Набор тестов будет зависеть от того, на какую оценку вы выполняли задание. Ее требуется указать в файле mark.txt. По умолчанию там стоит "5".

## Вариант выполнения на “3”
На тройку требуется реализовать алгоритм равномерного кодирования. Напомню, это означает, что коды для всех символа текста необходимо выбрать одной (минимально возможной) длины.
### Алгоритм кодирования
1. Строим список всех символов исходного текста (символы в этом списке должны быть уникальны).
2. По длине полученного списка выбираем разрядность кодировки (количество бит в кодовом слове). Гарантируется, что различных символов будет не более 255. Одно кодовое слово оставьте прозапас. Например, если у нас получилось 13 различных символов, нам хватит 4 бит в качестве длины кодовых слов.
3. Каждому символу ставим в соответствие кодовое слово выбранной в п.2 длины, состоящее из нулей и единиц.
4. Кодируем исходный текст, заменяя его исходные символы на соответствующие им кодовые слова. В результате получим длинную строку, содержащую только нули и единицы.
5. Теперь “нарежем” эту последовательность кусочками по 8 бит и каждый байт переведем в десятичную систему счисления. Это можно сделать так: `int(x, 2)`, где x -- строка, содержащая двоичное число. Таким образом у нас получится список чисел, не превосходящих 255.
6. Теперь возьмем символы, которые соответствуют полученным кодам по ASCII таблице, а затем склеим эти символы в одну строку. Получится закодированный (и возможно сжатый) текст. В python это можно сделать одним вызовом функции `bytes()`. Она принимает в качестве параметра список ASCII-кодов символов. Обратите внимание, что получится не строка, а байтовая строка. Это нормально, именно этого мы и хотели добиться. Обратите внимание, что для того чтобы записать такую строку в файл, его нужно открыть следующим образом: `open('name.par’, 'wb')`.

Если оставить все, как есть, декодировать текст обратно не получится, т.к. программа ничего не будет знать о выбранной кодировке. Эту информацию нужно приклеить к началу строки. Можно сделать это так: первый байт закодированного сообщения кодирует количество различных символов исходного текста (используя это число, можно будет вычислить разрядность кодировки). Далее байты идут парами: первый содержит ASCII код закодированного символа (его можно получить при помощи функции `ord()`), во втором -- его кодовое слово (расположите его в начале или в конце байта). Возможны и другие, более "компактные" подходы.

### Пример
Попробуем закодировать строку: “Предуниверсарий МАИ”.
1. Список символов: {'в', ' ', 'и', 'а', 'с', 'П', 'е', 'А', 'й', 'д', 'М', 'у', 'И', 'р', 'н'}.
2. Список имеет длину 15 (вместе с дополнительным кодовым словом 16), значит минимальная разрядность кодировки должна быть 4.
3. Закодируем символы:
- 'в' - 0000
- ' ' - 0001
- 'и' - 0010
- 'а' - 0011
- 'с' - 0100
- 'П' - 0101
- 'е' - 0110
- 'А' - 0111
- 'й' - 1000
- 'д' - 1001
- 'М' - 1010
- 'у' - 1011
- 'И' - 1100
- 'р' - 1101
- 'н' - 1110
У нас остался один невостребованный код: 1111. Он будет играть роль маркера конца сообщения.
4. Закодируем текст и добавим в его конец маркер конца сообщения 1111: 0101110011010011011110100100000011011000100001111000010100000011010011110111111
5. Нарежем по 8 бит: 01011100 11010011 01111010 01000000 11011000 10000111 10000101 00000011 01001111 0111111. Последняя "восьмерка" оказалась "семеркой". Но в этом нет ничего страшного, просто добавим в конец "0" или "1". Теперь получим список чисел: [92, 211, 122, 64, 216, 135, 133, 3, 79, 127].
6. Получилась байтовая строка `b'\\\xd3z@\xd8\x87\x85\x03O\x7f'`
7. Осталось только приклеить к строке служебную информацию, необходимую для декодирования, и сохранить файл с расширением `.par`. Это ученикам предлагается релизовать самостоятельно.

### Алгоритм декодирования
С декодированием все очень просто: достаточно выполнить все шаги кодирования в обратном порядке. Обратите внимание, что и прочитать из файла нужно байтовую строку, а не обычную. Для этого открыть файл нужно следующим образом: `open('text.par', 'rb')`.


## Вариант выполнения на “4”
На четверку вместо равномерного кодирования предлагается использовать алгоритм кодирования Хаффмана. 

### Алгоритм кодирования
1. В отличие от предыдущего варианта, на первом шаге необходимо подсчитать частоту употребления каждого символа. Возможно, вам поможет [`Counter`](https://docs.python.org/3/library/collections.html#collections.Counter).
2. Процесс построения дерева кодирования должен быть реализован при помощи рекурсивной функции.
4. Аналогично пунктам 4-6 из варианта выполнения “на 3”.
7. Проблема, описанная в пункте 7 варианта выполнения на “3”, актуальна и для данного метода. Служебную метаинформацию также нужно приклеить в получившейся закодированной строке, но из-за неравномерности кода это будет сделать не так тривиально. Предложение будет следующим: сделаем это аналогично равномерному кодированию, но в список будем писать тройки байт: символ - длина кода - код. Возможны и другие подходы.

### Алгоритм декодирования
Как и в случае выполнения на “3”, достаточно повторить все шаги кодирования в обратном порядке, а результат сохранить в файл.

## Вариант выполнения на “5”
В дополнение к кодированию при помощи алгоритма Хаффмана реализуйте опциональное шифрование текста при помощи шифра Виженера. Опциональность означает, что если ключ в качестве аргумента не передавался, т.е. запуск был идентичен запуску программы при выполнении на "3" и "4", шифрование производить не следует, результаты работы программы должны быть такими же, как и во варианте на "4". Если же аргумент с ключом передали, т.е. вызов был следующего вида: `python3 main.py -e text.txt pum`, текст следует зашифровать, используя в качестве ключа `pum`. Естесственно, совержить обратное преобразование без ключа теперь не получится, так что для декодирования потребуется выполнить следующую команду: `python3 main.py -d text.par pum`.