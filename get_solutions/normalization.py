import math

y_depot=48.5919883 #latitude dépôt
x_depot=7.7807406 #longitutde dépôt

yA=48.493476 #latitudeA (minimale)
xA=7.678295 #longitudeA (minimale)
yB=48.647955 #latitudeB (maximale)
xB=7.838970 #longitudeB (maximale)

def normalization(X_list,Y_list,d_list,x_depot,y_depot,xA,yA,xB,yB):
    x = X_list
    y = Y_list
    d=d_list

    # Normalisation des coordonnées du dépôt
    x_depot_norm = x_depot - xA
    x_depot_norm= x_depot_norm/(xB-xA)
    y_depot_norm = y_depot - yA
    y_depot_norm= y_depot_norm/(yB-yA)
    depot_norm=[x_depot_norm,y_depot_norm]

    # Normalisation des coordonnées des clients
    x_norm=[(x[i]-xA)/(xB-xA) for i in range(len(x))] #longitudes normalisées
    y_norm=[(y[i]-yA)/(yB-yA) for i in range(len(y))] #latitudes normalisées

    # Arrondi supérieur des demandes
    d_norm = [math.ceil(d[i]) for i in range(len(d))]
   
    return x_norm,y_norm,d_norm,depot_norm
