# Активация виртуального окружения
. .\.venv\Scripts\Activate.ps1

# Создание папки для результатов теста, если её ещё нет
if (!(Test-Path -Path "allure-results")) {
    New-Item -ItemType Directory -Path "allure-results" | Out-Null
}

# Запуск тестов
pytest -s -v tests --alluredir=allure-results

# Показ отчета Allure (если установлен Allure CLI)
if (Get-Command allure -ErrorAction SilentlyContinue) {
    allure serve allure-results
} else {
    Write-Host "`nAllure CLI не найден. Установи его с https://docs.qameta.io/allure/#_get_started"
}
