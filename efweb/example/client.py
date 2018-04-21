import requests


# r = requests.post("http://127.0.0.1:8000", data={'a': 123, 'b': 456})

r = requests.delete("http://127.0.0.1:8000", data={'a': 123, 'b': 456})

print(r.json())