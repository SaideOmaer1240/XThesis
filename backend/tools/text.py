from learnfetch import Pesquisador

pesquisar = Pesquisador()
env = 'molecula'
def get_image(qury : str, engine):
    images = []
    p = engine.get_response(qury)
    for i in p:
        img = i.get('img', '')
        images.append(img)
    
    return images

f = get_image(env, pesquisar)
print(f)