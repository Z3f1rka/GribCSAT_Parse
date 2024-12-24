@echo off
SET venv=.venv\Scripts
SET source=setup_scripts
cd ..
IF NOT EXIST ".venv" (
    python -m venv .venv
    %venv%\pip.exe install -r requirements/dev.txt
) ELSE (
    ECHO 'Delete python venv for installing correctly'
)

IF NOT EXIST ".env" (
    IF NOT EXIST ".env.template" (
        ECHO ".env.template is not exist"
    ) ELSE (
        COPY .env.template .env
    )
)

IF NOT EXIST ".git" (
    ECHO "git repository does not exist"
) ELSE (
    COPY %source%\pre-commit .git\hooks\pre-commit
)