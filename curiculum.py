while  True:
        
    name = input ("как тебя зовут человек?").capitalize()
    
    name = name.capitalize()
                        
    try:
        age = int ( input ("сколько тебе лет ?"))
    except:
        print("Вводите только числовое значение ")
        continue
        
    if age >= 101:
        print ("Столько не жывут")
        continue
        

    if age % 10 == 1 and age != 11:
        ageText = "год"
    elif  2 <= age % 10 <= 4 and not ( 12 <= age % 100 <= 14):
        ageText = "года"
    else:
        ageText = "лет"

    
    print (f"Привет {name}. Приятно познакомиться! Тебе {age} {ageText}.")

    if age >= 18:
        print ("Ты взрослый")
    else:
        print("Ты ещё молодой")
    
    if age < 18:
        print ("Ты еще ребенок")
    elif age < 66:
        print ("Ты совершенелетний")
    else:
        print ("Ты пенсионер")
        
    
    break
