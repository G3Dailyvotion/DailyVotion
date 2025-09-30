@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: ============================================================================
:: DailyVotion - Windows Setup Script
:: Creates a venv, installs dependencies, runs migrations, and can start server
:: Usage: Double-click or run in Command Prompt: setup.bat
:: ============================================================================

pushd "%~dp0"

echo.
echo === DailyVotion Windows Setup ===
echo Repo: %cd%

:: 1) Locate Python (prefer the Windows py launcher)
call :find_python
if errorlevel 1 goto :fail

:: 2) Require Python >= 3.10
%PY_CMD% -c "import sys; exit(0 if sys.version_info>=(3,10) else 1)"
if errorlevel 1 (
  echo [ERROR] Python 3.10+ is required. Detected version:
  %PY_CMD% --version
  goto :fail
)

:: 3) Create virtual environment if needed
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment in .venv ...
  %PY_CMD% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    goto :fail
  )
) else (
  echo Reusing existing virtual environment: .venv
)

:: 4) Activate venv
call ".venv\Scripts\activate.bat"
if not defined VIRTUAL_ENV (
  echo [ERROR] Failed to activate the virtual environment.
  goto :fail
)

:: 5) Upgrade pip tooling
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail

:: 6) Install dependencies
if exist "requirements.txt" (
  echo Installing dependencies from requirements.txt ...
  python -m pip install -r requirements.txt
  if errorlevel 1 goto :fail
) else (
  echo [WARN] requirements.txt not found. Installing Django only for development ...
  python -m pip install "Django>=5.0,<6.0"
  if errorlevel 1 goto :fail
)

:: 7) Run Django checks and migrations if manage.py exists
if exist "manage.py" (
  echo Running Django system check ...
  python manage.py check
  if errorlevel 1 (
    echo [WARN] Django check reported issues. Review output above.
  )

  echo Applying database migrations ...
  python manage.py migrate --noinput
  if errorlevel 1 goto :fail

  echo Collecting static files (may be optional for dev) ...
  python manage.py collectstatic --noinput
  if errorlevel 1 (
    echo [WARN] collectstatic failed or is not configured; continuing. This is often safe for local development.
  )
) else (
  echo [WARN] manage.py not found in %cd%. Skipping Django steps.
)

echo.
echo Setup complete.
echo.
echo To activate the virtual environment in a new shell:
echo   .venv\Scripts\activate
echo To start the development server:
echo   python manage.py runserver

:: 8) Offer to start the server now (choice requires Windows Vista+)
choice /C YN /M "Start Django development server now?"
if errorlevel 2 goto :end
if exist "manage.py" (
  python manage.py runserver
) else (
  echo manage.py not found; cannot start server.
)

goto :end

:: ----------------------------------
:: Functions
:: ----------------------------------
:find_python
  :: Prefer the py launcher with explicit versions
  where py >nul 2>&1
  if not errorlevel 1 (
    for %%V in (3.13 3.12 3.11 3.10 3) do (
      py -%%V --version >nul 2>&1
      if not errorlevel 1 (
        set "PY_CMD=py -%%V"
        echo Using Python via: %PY_CMD%
        exit /b 0
      )
    )
  )

  :: Fallback to python/python3 on PATH
  for %%P in (python python3) do (
    where %%P >nul 2>&1
    if not errorlevel 1 (
      set "PY_CMD=%%P"
      echo Using Python via: %PY_CMD%
      exit /b 0
    )
  )

  echo [ERROR] Python was not found. Please install Python 3.10+ from:
  echo         https://www.python.org/downloads/windows/
  exit /b 1

:fail
  echo.
  echo [FAILED] Setup encountered an error. See messages above.
  echo If this persists, ensure you have network access and sufficient permissions.
  goto :end

:end
  echo.
  echo Done. You can close this window.
  pause
  popd
  endlocal
  exit /b 0
