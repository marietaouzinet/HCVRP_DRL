import matplotlib.pyplot as plt

def display_results(routes):
    veh1=routes[0]
    veh2=routes[1]
    veh3=routes[2]
    veh4=routes[3]
    veh5=routes[4]
    x_depotnorm=0.6375951454800044
    y_depotnorm=0.6377067433113536

    x1_coords=[veh1[0][k][0] for k in range(len(veh1[0]))]
    x1_coords.insert(0, x_depotnorm)
    y1_coords=[veh1[0][k][1] for k in range(len(veh1[0]))]
    y1_coords.insert(0, y_depotnorm)
    #print("X1:",x1_coords)
    #print("Y1:",y1_coords)
    print("\n")

    x2_coords=[veh2[0][k][0] for k in range(len(veh2[0]))]
    x2_coords.insert(0, x_depotnorm)
    y2_coords=[veh2[0][k][1] for k in range(len(veh2[0]))]
    y2_coords.insert(0, y_depotnorm)
    #print("X2:",x2_coords)
    #print("Y2:",y2_coords)
    #print("\n")

    x3_coords=[veh3[0][k][0] for k in range(len(veh3[0]))]
    x3_coords.insert(0, x_depotnorm)
    y3_coords=[veh3[0][k][1] for k in range(len(veh3[0]))]
    y3_coords.insert(0, y_depotnorm)
    #print("X3:",x3_coords)
    #print("Y3:",y3_coords)
    #print("\n")

    x4_coords=[veh4[0][k][0] for k in range(len(veh4[0]))]
    x4_coords.insert(0, x_depotnorm)
    y4_coords=[veh4[0][k][1] for k in range(len(veh4[0]))]
    y4_coords.insert(0, y_depotnorm)
    #print("X4:",x4_coords)
    #print("Y4:",y4_coords)
    #print("\n")

    x5_coords=[veh5[0][k][0] for k in range(len(veh5[0]))]
    x5_coords.insert(0, x_depotnorm)
    y5_coords=[veh5[0][k][1] for k in range(len(veh5[0]))]
    y5_coords.insert(0, y_depotnorm)
    #print("X5:",x5_coords)
    #print("Y5:",y5_coords)
    #print("\n")

    x_coords=[x1_coords,x2_coords,x3_coords,x4_coords,x5_coords]
    y_coords=[y1_coords,y2_coords,y3_coords,y4_coords,y5_coords]

    # Liste de couleurs pour les véhicules
    colors = ['r', 'g', 'b', 'c', 'm']
    #Légendes pour les véhicules
    labels = ['Véhicule 1', 'Véhicule 2', 'Véhicule 3', 'Véhicule 4', 'Véhicule 5']

    # Boucle pour chaque véhicule
    for i, vehicle in enumerate(routes):
        # On trace les points
        plt.scatter(x_coords[i], y_coords[i], color=colors[i])
        # On les relie avec des flèches
        plt.plot(x_coords[i], y_coords[i], color=colors[i],label=labels[i])
        for j in range((len(x_coords[i])) - 1):
            start = (x_coords[i][j], y_coords[i][j])
            end = (x_coords[i][j+1], y_coords[i][j+1])
            mid_point = ((start[0]+end[0])/2, (start[1]+end[1])/2)
            plt.annotate('', xy=mid_point, xytext=start, arrowprops=dict(arrowstyle='->', color=colors[i % len(colors)], lw=1.5), va='center', ha='center')
            if j != 0 and routes[i][1][j-1] != 0:
                plt.text(x_coords[i][j], y_coords[i][j], f" {j}",color=colors[i])


    # On trace le dépôt
    plt.scatter(x_depotnorm, y_depotnorm, color='black',marker='s')
    plt.legend()
    plt.text(x_depotnorm, y_depotnorm, "Dépôt")
    plt.title("Points de livraisons (normalisés) et trajets obtenus après traitement")
    # Limites de l'espace normalisé
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.show()
