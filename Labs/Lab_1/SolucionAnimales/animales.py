def animales(input):
    '''
    Como hace el animalito?
    '''
    if input.lower() == 'gato':
        print('miau')
    elif input.lower() == 'perro': #Se modificó, cambiando if por elif
        print('guau')
    elif input.lower() == 'fox': #Se modificó, cambiando if por elif
        print('https://www.youtube.com/watch?v=jofNR_WkoCE')
    else:
        raise ValueError('animal no reconocido :(')
