
```
1. backend
cd backend 
python -m venv venv
venv\Scripts\activate
pip install requirements.txt
pytest tests\test_normalizer.py -v

run backend: .\venv\Scripts\uvicorn.exe main:app --reload

2. fontend
cd backend
run frontend: .\venv\Scripts\streamlit.exe run ..\frontend\form.py 
```