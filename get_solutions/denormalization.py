
def denormalization(routes,xA, yA, xB, yB):
    real_routes=[]

    #dénomarlisation des coordonnées
    for i,route in enumerate(routes):
        real_route_coords = [[y*(yB-yA) + yA, x*(xB-xA) + xA] for [x, y] in route[0]]
        real_route = [real_route_coords, route[1]]
        real_routes.append(real_route)

    print("veh1_real : ", real_routes[0])
    print("veh2_real : ", real_routes[1])
    print("veh3_real : ", real_routes[2])
    print("veh4_real : ", real_routes[3])
    print("veh5_real : ", real_routes[4])

    return real_routes
