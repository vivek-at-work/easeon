find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
