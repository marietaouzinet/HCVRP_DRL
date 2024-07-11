import os
from fleet_v5.utils.data_utils import save_dataset
import argparse

def generate_real_data(X_list, Y_list, d_list,N):
    x = X_list
    y = Y_list
    d= d_list
    y_depot=48.5919883
    x_depot=7.7807406

    yA=48.493476 #latitudeA
    xA=7.678295 #longitudeA
    yB=48.647955 #latitudeB
    xB=7.838970 #longitudeB

    x_depot_norm = x_depot - xA
    x_depot_norm= x_depot_norm/(xB-xA)
    y_depot_norm = y_depot - yA
    y_depot_norm= y_depot_norm/(yB-yA)


    depot=[x_depot_norm,y_depot_norm]
    cust = [[x[i],y[i]] for i in range(len(x))]
    
    cap = [20., 25., 30., 40., 45.]
    thedata = [depot,  # Coordonées du dépôt
                    cust,
                    d,
                    cap
                    ]
    
    data_dir = 'real_data'
    problem = 'hcvrp'
    datadir = os.path.join(data_dir, problem)
    os.makedirs(datadir, exist_ok=True)
    filename = os.path.join(datadir, '{}_v{}_{}_seed{}.pkl'.format(problem, 5, N, 24610))
    save_dataset(thedata, filename)
    
    return thedata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--X_list", nargs='+', type=float, required=True)
    parser.add_argument("--Y_list", nargs='+', type=float, required=True)
    parser.add_argument("--d_list", nargs='+', type=int, required=True)
    parser.add_argument("--filename", help="Filename of the dataset to create (ignores datadir)")
    parser.add_argument("--veh_num", type=int, default=5, help="number of the vehicles; 3 or 5")
    parser.add_argument('--graph_size', type=int, default=80,
                        help="Sizes of problem instances: {40, 60, 80, 100, 120} for 3 vehicles, "
                             "{10, 20, 30, 40, 60, 80, 100, 120, 140, 160} for 5 vehicles")

    opts = parser.parse_args()
    data_dir = 'real_data'
    problem = 'hcvrp'
    datadir = os.path.join(data_dir, problem)
    os.makedirs(datadir, exist_ok=True)
    filename = os.path.join(datadir, '{}_v{}_{}_seed{}.pkl'.format(problem, 5, opts.graph_size , 24610))

    dataset = generate_real_data(opts.X_list, opts.Y_list, opts.d_list,opts.graph_size)
    #print(dataset)
    save_dataset(dataset, filename)