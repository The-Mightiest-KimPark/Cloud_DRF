# 프로젝트 세팅

1. 가상환경 폴더 생성
```bash
python -m venv venv
```

2. 프로젝트가 가상환경을 바라보도록 설정
```bash
source venv/Scripts/activate     # bash
source venv/Scripts/activate.bat # cmd

```

3. 가상폴더를 바라보도록 한 뒤 모듈 설치
```bash
pip install -r requirements.txt
```


4. 프로젝트 로컬 서버에 띄우기
```bash
python manage.py runserver
```
