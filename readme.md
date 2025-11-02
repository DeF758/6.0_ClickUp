

Копировать репозиторий на локальную машину:
```
git clone https://github.com/DeF758/5.2_Playwright.git
```
Установить `uv`, если ещё не установлен:
```
pip install uv
```
Создать виртуальное окружение:
```
uv venv
```
Активировать виртуальное окружение:
```
.\.venv\Scripts\activate
```
Установить зависимости проекта: 
```
uv pip install -r requirements.txt
```
Установить chromium:
```
uv run playwright install chromium
```
Запустить тесты командой:
```
pytest
```
или командой `.\run_tests.ps1` для просмотра отчётов Allure:
```
.\run_tests.ps1
```
Если Allure не установлен - следуй инструкции ниже ↓

#### Для просмотра web-отчётов:
1. Открой PowerShell
2. Установи Scoop выполнив команды:  
    ```  
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  
    ```
    ```  
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression  
    ```
3. Установи Java. Для этого посети сайт [Oracle](https://www.oracle.com/java/technologies/downloads/?er=221886#java17-windows) и скачай installer подходящий твоей операционной системе. Затем просто установи Java, как обычную программу
4. Чтобы проверить, что Java был установлен, выполни команду:  
    ```  
    java -version  
    ```
5. Установи Allure, выполнив команду в PowerShell:   
    ``` 
    scoop install allure  
    ```
6. Чтобы проверить, что Allure был установлен, выполни команду в PowerShell:  
    ```  
    allure --version  
    ```
7. Открой терминал в той среде разработки, куда клонировал репозиторий
8. Запусти тесты, выполнив команду в терминале среды разработки:  
    ```  
    pytest -s -v tests --alluredir=allure-results  
    ```
9. Сгенерируй отчёт на web-странице, выполнив команду в терминале среды разработки:  
    ```  
    allure serve allure-results
    ```
10. Нажми на полученную ссылку, она будет примерно `Server started at <`ЗДЕСЬ`>. Press <Ctrl+C> to exit`
