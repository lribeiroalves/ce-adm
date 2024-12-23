with open('teste_pat_TX.txt', 'r') as file:
    content = file.read()
    new_content = content.replace(',', '\n').replace('/', ',')
    with open('texto.csv', 'w') as f:
        for c in new_content:
            f.write(c)