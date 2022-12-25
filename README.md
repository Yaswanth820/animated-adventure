# animated-adventure

This project extracts text from scanned PDFs and stores it in a database. 

## Features:-

1. User Authentication where users can login and store their pdfs
2. Extracts text from scanned PDFs
3. Stores the extracted text in a database
4. Provides a search interface to filter the pdfs


## Prequisites:-

1. Python3
2. PostgreSQL
3. Tesseract
4. Poppler


## Installation:-

1. Clone the repository
2. Install the requirements using `pip install -r requirements.txt`
3. Configure database settings in `settings.py`
4. Run `python manage.py makemigrations`
5. Run `python manage.py migrate`
6. Run `python manage.py runserver`