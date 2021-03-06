# Пакет linis-scripts: LDA по-русски

Основная задача коллекции скриптов linis-scripts — обеспечить
возможность тематического моделирования больших массивов текстов на
русском языке с использованием алгоритмов семейства Latent Dirichlet
Allocation (LDA).

Скрипты обеспечивают: 
 * подготовку скаченных с web текстов (чистка html, xml-разметки и всяческого оставшегося от нее мусора), преобразование в таблицу 1 текст на строку;
 * лемматизацию текстов;
 * запуск LDA (с использованием пакета STMT);
 * оформление результатов работы STMT в удобном для анализа виде (топ-слова + топ-тексты тем, матрица веса слов в темах).

(с\) Кирилл Маслинский 2011—2012 

Пакет распространяется в соответствии с условиями лицензии GNU GPL версии 2 или любой более поздней версии. 

## Зависимости ##

 * UNIX-подобная операционная система ИЛИ окружение, предоставляющее bash и coreutils на платформе Windows, например cygwin;
 * [Stanford Topic Modeling Toolbox](http://nlp.stanford.edu/software/tmt/tmt-0.4/);
 * GNU make;
 * awk;
 * sed;
 * html-xml-utils;
 * [mystem](http://company.yandex.ru/technologies/mystem/);
 * python;
 * zip, gzip.

## Подготовка текстов ##

Исходными данными для работы является каталог (стандартное имя — txt), в котором каждый текст коллекции представлен в отдельном файле в текстовом формате (бв кодировке UTF-8). Файлы должны иметь расширение `.txt`. Имя файла (без расширения) будет использовано в качестве идентификатора текста при дальнейшей обработке. 

Процедура подготовки текста к анализу проходит в несколько этапов, на каждом этапе создаются промежуточные файлы данных, отражающие состояние текстов на текущей фазе обработки. Промежуточный файл используется как входные данные для следующего этапа обработки текстов.

Промежуточные файлы сохраняются после завершения обработки текстов и могут быть затем использованы для различных целей анализа и представления результатов. Кодировка всех файлов данных — UTF-8.

Ниже поэтапно описаны промежуточные файлы данных и операции, выполняемые при подготовке этих файлов. 

### Файл `source.txt`

В этом файле текстовая коллекция объединяется из множества файлов в одну текстовую таблицу, где каждый текст вытянут в одну строку. В таблице две колонки: 
 * индентификатор текста (имя исходного файла без расширения);
 * исходный текст, вытянутый в одну строку.

Разделителем полей служит запятая. 

Пример строки:

~~~~~~~
000000000004,<span style="font-size:small;"><span style="color: rgb(0, 0, 0); font-family: 'lucida grande', tahoma, verdana, arial, sans-serif; line-height: 14px; text-align: left; background-color: rgb(255, 255, 255); ">У нас тепло. Дети вчера ловили в озере раков. по английски рак - крейфиш. Наловили несколько и положили в ведеорко. К нам подходят соседи и спрашивают детей, что там у них. Соня радостно отвечает: " У нас целове ведро крэка!"</span></span><br />
~~~~~~~

Обработку выполняет скрипт `txtdir2csv.sh`.

При обработке исходного текста последовательно выполняются следующие операции: 
 * замена HTML entities (вида `&#149; &quot; &nbsp;`) на соответствующие Unicode-символы (с помощью утилиты `hxunent` из пакета `html-xml-utils`);
 * замена всех символов возврата каретки и перевода строки (`^M\n`) пробелами.


### Файл `clean.txt`

Следующий этап обработки — удаление HTML и XML-разметки и прочего
шума, характерного для текстов, автоматически скаченных с
web.  

При удалении разметки решаются следующие задачи: 
 * преобразовать ценную для анализа информацию из разметки в *псевдослова*, которые пройдут неизменными через процедуру лемматизации (например, URL, специфические теги LiveJournal и т. п.);
 * извлечь из разметки максимум значимой текстовой информации, в том числе
той, которая находится в атрибутах HTML-тегов (например, подписи к
изображениям в атрибуте `alt`);
 * удалить любую разметку, в том числе синтаксически невалидный HTML (несбалансированные теги, фрагменты разметки, стилей MS Word и т.п.), основная цель при этом — не потерять значимый текст, удалив максимум мусора.

Скрипт удаления разметки ориентирован на тексты, полученные из LiveJournal, поэтому содержит некоторые специфические правила замен, необходимые для этой коллекции.

В файле `clean.txt` те же колонки, что и в `source.txt`, отличие в том, что в тексте удалена вся разметка. 

Пример строки файла:

~~~~~~~
000000000004,  У нас тепло. Дети вчера ловили в озере раков. по английски рак - крейфиш. Наловили несколько и положили в ведеорко. К на      м подходят соседи и спрашивают детей, что там у них. Соня радостно отвечает: " У нас целове ведро крэка!"
~~~~~~~

Обработку выполняет скрипт `clean.sed`.

При обработке выполняются следующие операции:
 * Замена всех непечатаемых символов пробелами (например, управляющие символы, занимающие первые десятки позиций в кодировках ASCII и UTF-8).
 * Замена символа неразрывного пробела (unicode 00A0) обычным пробелом.
 * Замена тега `<img>` (изображение) псевдословом вида `IMGurl`. В ссылка на исходное изображение (атрибут `href`) удаляется префикс `http://`, в оставшейся части удаляются все пунктуационные символы (.,/& и т.п.). Если в теге имеется текст подписи в атрибуте `alt`, этот текст вставляется после псевдослова `IMG`. 

   Например, `<img href="http://fotki.ru/fotka.jpg" alt="подпись к ней">` будет преобразовано в `IMGfotkirufotkajpg подпись к ней`. 

 * Замена тега `<a>` псевдословом `HREFurl`. Обработка производится аналогично тегу `<img>`.
 * Замена тега `<lj user="имя_пользователя">` псевдословом `LJUSERимя_пользователя`.
 * Замена всех тегов вида `<lj-тег>` псевдословом LJтег.
 * Замена смайликов вида `:) ;) :-) ;-) ))` и т.д. псевдословом SMILEA;
 * Замена смайликов вида `)))` (и более скобок) псевдословом SMILEAA;
 * Замена смайликов вида `:( :-( :-\` псевдословом SMILEU;
 * Замена смайликов вида `((` (и более скобок) псевдословом SMILEUU;
 * Замена всех оставшихся тегов (текст в угловых скобках) пробелами;
 * Замена всех URL в тексте, не оформленных тегами `<a>`, на псевдослова вида `HREFurl`.

### Файл `lemmatized.txt` ###

Следующий этап обработки — лемматизация текста (приведение всех слов к начальной форме). Поскольку при автоматической лемматизации существует проблема грамматической омонимии (одной и той же форме слова могут соответствовать несколько исходных форм, например, `стекло` и `стекать`), на этом этапе выполняется также автоматическое снятие омонимии. 

 * Лемматизация выполняется командой `mystem -lcf -e utf-8`. Для каждой словоформы mystem выводит список возможных начальных форм с их частотностями (оценеными по большому корпусу текстов со снятой омонимией).
 * Автоматическое снятие омонимии выполняется скриптом `demystem.py` по следующему алгоритму:
     + Для каждой словоформы выбирается лемма (начальная форма) с наибольшей частотностью;
     + Если mystem не дает данных о частотности, выбирается первая словоформа.

Пример строки файла: 

~~~~~~
000000000004,  у мы теплый. ребенок вчера ловить в озеро рак. по английский рак - крейфиш. налавливать несколько и положить в ведеоркий      . к мы подходить сосед и спрашивать ребенок, что там у они. соня радостно отвечать: " у мы целов ведро крэк!"
~~~~~~

### Файл `lemmatized.csv` ###

На этом этапе производится удаление из текстов всей пунктуации, кроме дефисов.

Преобразование выполняется правилом в `Makefile`.

Пример строки файла: 

~~~~~~
000000000004,  у мы теплый ребенок вчера ловить в озеро рак по английский рак - крейфиш налавливать несколько и положить в ведеоркий к       мы подходить сосед и спрашивать ребенок что там у они соня радостно отвечать  у мы целов ведро крэк
~~~~~~

## Настройка и выполнение LDA

Тематическое моделирование выполняется с помощью Stanford Topic MIdeling Toolbox (далее — `tmt`). Исходными данными для работы tmt является файл `lemmatized.csv`. 

Параметры расчета LDA задаются в конфигурационном файле. Шаблон такого файла с параметрами, используемыми в linis по умолчанию, включен в пакет — `config100.scala`.

В ходе работы tmt используются следующие параметры по умолчанию:
 * текст извлекается из второй колонки входного файла,
 * идентификаторы текстов — из первой колонки,
 * строка текста токенизируется (разделяется на слова) по пробелам,
 * из рассмотрения удаляются все слова, которые встречаются менее чем в пяти разных документах коллекции,
 * из рассмотрения удаляются 100 самых частотных слов коллекции,
 * из рассмотрения удаляются все тексты, длина которых оказалась менее пяти слов после удаления редких и частотных терминов по вышеописанным правилам,
 * выполняется обучение модели LDA с использованием параметров: 
     + 100 тем,
     + эвристический алгоритм, используемый для оценки модели — Gibbs Sampling,
     + 1500 итераций,
     + параметр сглаживания тем — симметричные параметры Дирихле `0.01`,
     + параметр сглаживания терминов — симметричные параметры Дирихле `0.01`.

## Оформление результатов LDA

Результат расчета модели сохраняется в каталоге `lda<число_тем>`, при использовании конфигурационного файла по умолчанию — `lda100`. 

Ниже описаны все файлы, содержащие результаты моделирования. 
Все файлы в кодировке UTF-8.

### Файл `document-topic-distributions.csv`

Файл содержит матрицу вероятностей тексты × темы. Таблица представлена в формате CSV и содержит следующие колонки: 
 * идентификатор текста,
 * N колонок (по числу тем) с вероятностью принадлежности данного текста к данной теме. Колонки расположены в порядке нумерации тем.

Файл генерируется `tmt`.

### Файл `topic-term-distributions.csv`

Файл содержит матрицу весов терминов (слов) в каждой теме. Таблица представлена в формате CSV и содержит следующие колонки: 
 * термин,
 * N колонок (по числу тем) с весом данного термина в данной теме (≈ число употреблений данного термина в данной теме). 

Файл генерируется правилом в `Makefile`.

### Файл `top50.txt`

Текстовый файл, который содержит для каждой из N выделенных тем: 
 * топ-20 слов (терминов с наибольшим весом в данной теме);
 * топ-50 текстов (текстов, отнесенных к данной теме с наибольшей вероятностью). Тексты приводятся в форме, очищенной от разметки, соответствующей файлу `clean.txt`.

Файл формируется скриптом `topntexts.py`.

## Использование

1. Создать каталог для обработки данных. 
2. Поместить в этом каталоге подкаталог `txt` с файлами исходных текстов (по одному тексту в каждом файле). 
3. Скопировать в этот каталог из каталога скриптов файл `Makefile.in` и переименовать его в `Makefile`.
4. Заменить в файле `Makefile` путь к каталогу скриптов на путь, соответствующий размещению скриптов на Вашем диске: `SCRIPTS="$$HOME/lab/linis/scripts"`.
4. Скопировать в этот каталог из каталога скриптов файл `config100.scala`.
5. В командной строке, перейдя в каталог с данными, выполнить команду `make` (этап подготовки текстов).
6. Выполнить команду `make lda-default` (расчет модели LDA).
7. Выполнить команду `make dist-lda` (формирование zip-архива с файлами результатов расчета LDA).
8. Выполнить команду `make dist-data` (формирование zip-архива с промежуточными файлами исходных данных).

