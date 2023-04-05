from datetime import datetime, date

form_string = '1978-06-19'
today = date.today()
birthday = datetime.strptime(form_string, '%Y-%m-%d')
print(today.year - birthday.year
       - ((today.month, today.day) < (birthday.month, birthday.day)))
print((today.month, today.day) < (birthday.month,birthday.day))
print((birthday.month,birthday.day))
print(True + True)