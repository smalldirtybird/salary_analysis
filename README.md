# Magic salary analysis for programmers

Just run script and get info about programmer's salaries from two biggest russian servises of job searching.
```
+-----------------------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| TypeScript            | 532              | 433                 | 207421           |
| C                     | 1331             | 1258                | 173444           |
| C#                    | 586              | 524                 | 183740           |
| C++                   | 536              | 483                 | 180810           |
| PHP                   | 952              | 886                 | 170441           |
| Python                | 909              | 811                 | 199806           |
| Java                  | 899              | 809                 | 225807           |
| JavaScript            | 1754             | 1532                | 180910           |
+-----------------------+------------------+---------------------+------------------+

```
 
## How to prepare:
1. Make sure Python installed on your PC - you can get it from [official website](https://www.python.org/).
   

2. Install libraries with pip:
    ```
    pip3 install -r requirements.txt
    ```
3. Reggister your application  on [SuperJob API page](https://api.superjob.ru/) and get you personal        secret key wich looks like `v3.r.135656042.7a0563cda8...`. You can specify any web-site during              registration.
   Create .env file in directory with main.py file(use Notepad++) and add the string
   ```
   SJ_TOKEN='your_suberjob_secret_key'
   ```
   to it instead of value in quotes. Here and further quotes must be removed.
4. Add the string like
   ```
   HH_USER_EMAIL=`your_e-mail_address`
   ```
   with your email instead of value in quotes. This is required to access the Headhunter API according to the [documentation](https://github.com/hhru/api/blob/master/docs/general.md).
   
## How to use:
Run `main.py` with console. Use `cd` command if you need to change directory:
```
D:\>cd D:\learning\python\api_services\salary_analysis
D:\learning\python\api_services\salary_analysis>python main.py
```
As result you'll get two tables with statistics of average salaries in vacancies for each of the most popular programming languages on SuperJob
```
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| TypeScript            | 18               | 18                  | 185677           |
| Swift                 | 4                | 4                   | 207250           |
| Scala                 | 1                | 1                   | 240000           |
| Objective-C           | 1                | 1                   | 225000           |
| Shell                 | 6                | 6                   | 215166           |
| Go                    | 17               | 17                  | 205470           |
| C                     | 37               | 37                  | 159621           |
| C#                    | 24               | 24                  | 158083           |
| C++                   | 31               | 31                  | 168887           |
| PHP                   | 54               | 54                  | 157628           |
| Ruby                  | 6                | 6                   | 236000           |
| Python                | 44               | 44                  | 172670           |
| Java                  | 44               | 44                  | 230400           |
| JavaScript            | 85               | 85                  | 152654           |
+-----------------------+------------------+---------------------+------------------+
```
and HeadHunter
```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| TypeScript            | 532              | 433                 | 207421           |
| Swift                 | 213              | 193                 | 244890           |
| Scala                 | 62               | 55                  | 234263           |
| Objective-C           | 72               | 63                  | 239253           |
| Shell                 | 55               | 44                  | 190522           |
| Go                    | 291              | 241                 | 217632           |
| C                     | 1331             | 1258                | 173444           |
| C#                    | 586              | 524                 | 183740           |
| C++                   | 536              | 483                 | 180810           |
| PHP                   | 952              | 886                 | 170441           |
| Ruby                  | 114              | 94                  | 207802           |
| Python                | 909              | 811                 | 199806           |
| Java                  | 899              | 809                 | 225807           |
| JavaScript            | 1754             | 1532                | 180910           |
+-----------------------+------------------+---------------------+------------------+
```
