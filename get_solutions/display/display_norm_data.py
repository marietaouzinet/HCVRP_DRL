import matplotlib.pyplot as plt

def display(x_norm, y_norm, d):
    # On ajoute le dépôt
    x_depot_norm=0.6375951454800044
    y_depot_norm=0.6377067433113536
    x=x_norm.copy()
    x.insert(0,x_depot_norm)
    y=y_norm.copy()
    y.insert(0,y_depot_norm)
    d1=d.copy()
    d1.insert(0,0)
    #print("depot_norm : ",x_depot_norm,y_depot_norm)
    #print("x_norm avec dépôt : ",x)
    #print("y_norm avec dépôt : ",y)
    #print("d_norm avec dépôt : ",d1)

    # On trace les points sauf le dépôt
    plt.scatter(x[1:], y[1:])  
    plt.scatter(x[0], y[0], color='black', marker='s')  # Dépôt
    plt.title("Points de livraisons (normalisés) avant traitement")

    # (demande de matériel, ordre d'entrée de l'interface)
    for i in range(len(x)):
        plt.text(x[i], y[i], " d={} (n°{})".format(d1[i],i))

    # Espace normalisé
    plt.xlim([0, 1])
    plt.ylim([0, 1])

    plt.show()
