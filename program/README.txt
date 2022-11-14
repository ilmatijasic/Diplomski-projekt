"gui.py" sadrži grafičko sučelje
"recommend.py" sadrži sustav preporuka
Skup podataka je u "Attribute DataSet.xlsx" u direktoriju "Dresses dataset"
"REST_API.py" sadrži API


Koristi se Python3.
Skidanje potrebnih biblioteka:
	pip install -r requirements.txt

Testiranje programa:

1. Otvoriti dvije konzole i pozicionirati se u radni direktorij.
2. U prvoj pokrenuti naredbu:
	python -m uvicorn REST_API:app --reload
3. U drugoj pokrenuti naredbu:
   API verzija:
	python main_api.py
   GUI i API verzija:
	python main_gui.py

Za GUI verziju korisnik može izabrati vrijednosti različitih značajki i nakon pritiska na gumb "Submit"
Program vraća 4 najsličnije predmete.

