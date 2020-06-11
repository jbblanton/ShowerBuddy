

def test_function():
    
    my_list = ['cat', 'dog', 'fish']
    active = True

    start_action(0)
    print('<h3>started</h3>')
    
    
    while active:

        if 'cat' in my_list:
            first_func(1) 
            print('<h4>cat</h4>')
            my_list.remove('cat')
            continue

        if 'fish' in my_list:
            second_func(2)
            print('<h4>fish</h4>')
            my_list.remove('fish')
            continue

        if 'horse' in my_list:
            fourth_func(4)
            print('horse')
            my_list.remove('<h4>horse</h4>')
            continue

        active = False

    print("<h3>completed test</h3>")

def first_func(n):
    
    return 'complete'

def second_func(n):
    
    return 'complete'

def fourth_func(n):
    
    return 'complete'

def start_action(n):

    return 'complete'

print(test_function)