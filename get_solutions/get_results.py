import pickle
import datetime
import os

N=5
x_depotnorm=0.6375951454800044
y_depotnorm=0.6377067433113536

#COORDONNEES POUR NORMALISATION 
y_depot=48.5919883 #latitude dépôt
x_depot=7.7807406 #longitutde dépôt

yA=48.493476 #latitudeA (minimale)
xA=7.678295 #longitudeA (minimale)
yB=48.647955 #latitudeB (maximale)
xB=7.838970 #longitudeB (maximale)


def get_results(N):
    with open(f'results/hcvrp/hcvrp_v5_{N}_seed24610/hcvrp_v5_{N}_seed24610-hcvrp_40_epoch-20-greedy-t1-0-4.pkl', 'rb') as f1:
        results = pickle.load(f1)
        results=results[0]
        #print(results)
    return results


def get_best_route(results):
    min_cost=results[0][0]
    ind_min=0
    for i in range(len(results)):
     if results[i][0]<min_cost :
        min_cost=results[i][0]
        ind_min=i
    #print("ind_min :", ind_min)
    #print(results[0][ind_min])

    return results[ind_min],ind_min,min_cost


def get_routes(best_route,X_list,Y_list,d_list):
    
    # Génération du nom du fichier texte de sortie
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    directory = f'Tournees_optimisees/{current_date}/{N}_clients'
    filename_out = f'{directory}/{timestamp}.txt'
    # Création du répertoire s'il n'existe pas
    os.makedirs(directory, exist_ok=True)

    #On ajoute les coordonnées du dépot aux listes
    X_list.insert(0, x_depotnorm)
    Y_list.insert(0, y_depotnorm)
    #print(X_list, "\n", Y_list)

    #On rajoute la demande du dépot à d (0)
    d_list.insert(0,0)
    #print(d_list)
    #print ("\n")

    trajets=best_route[1]
    vehicules=best_route[2]
    vehicules=vehicules.tolist()
    #print("trajets:",trajets)
    #print("vehicules:",vehicules)
    while trajets[-1] == 0 and trajets.count(0) > 1:
        trajets.pop()
        vehicules.pop()
    #print("trajets:",trajets)
    #print("vehicules:",vehicules)
    veh1=[[],[]]
    veh2=[[],[]]
    veh3=[[],[]]
    veh4=[[],[]]
    veh5=[[],[]]
    for i, v in enumerate(vehicules):
        if v==0:
            veh1[0].append([X_list[trajets[i]],Y_list[trajets[i]]])
            veh1[1].append(d_list[trajets[i]])
        elif v==1:
            veh2[0].append([X_list[trajets[i]],Y_list[trajets[i]]])
            veh2[1].append(d_list[trajets[i]])
        elif v==2:
            veh3[0].append([X_list[trajets[i]],Y_list[trajets[i]]])
            veh3[1].append(d_list[trajets[i]])
        elif v==3:
            veh4[0].append([X_list[trajets[i]],Y_list[trajets[i]]])
            veh4[1].append(d_list[trajets[i]])
        else:
            veh5[0].append([X_list[trajets[i]],Y_list[trajets[i]]])
            veh5[1].append(d_list[trajets[i]])
    
    routes = [veh1, veh2, veh3, veh4, veh5]
    #real_routes=denormalization(routes,xA, yA, xB, yB)

    with open(filename_out, 'w') as f2:
        for k in range(5):
            f2.write(f"Véhicule {k+1} :\n")
            for i in range(len(real_routes[k][0])):
                f2.write(f"Client {i+1} : {real_routes[k][0][i]} \t")
                if real_routes[k][1][i] == 0:
                    f2.write("Retour au dépôt\n")
                    break
                f2.write(f"Demande : {real_routes[k][1][i]}\n")
            f2.write("\n")

    return routes,real_routes,filename_out

#routes,real_routes,filename_out=get_routes(best_route,X_list,Y_list,d_list)
#display_results(routes)   
