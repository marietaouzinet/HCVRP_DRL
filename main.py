import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from opencage.geocoder import OpenCageGeocode
import webbrowser
import customtkinter as ctk
import folium
from CTkListbox import *
import tkinter.messagebox as messagebox
#import polyline
import os
import folium
#import requests
import json
import subprocess
from get_solutions import normalization
import datetime
from get_solutions.display.display_norm_data import display
from get_solutions.display.display_results import display_results
#from generate_real_data import generate_real_data
from get_solutions.get_results import get_results
from get_solutions.get_results import get_best_route
from get_solutions.denormalization import denormalization

#COORDONNEES POUR NORMALISATION 
y_depot=48.5919883 #latitude dépôt
x_depot=7.7807406 #longitutde dépôt

yA=48.493476 #latitudeA (minimale)
xA=7.678295 #longitudeA (minimale)
yB=48.647955 #latitudeB (maximale)
xB=7.838970 #longitudeB (maximale)

def trajets_finaux(best_route,X_list,Y_list,d_list,depotnorm,N):
        # Génération du nom du fichier texte de sortie
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        directory = f'Tournees_optimisees/{current_date}/{N}_clients'
        filename_out = f'{directory}/{timestamp}.txt'
        # Création du répertoire s'il n'existe pas
        os.makedirs(directory, exist_ok=True)

        #On ajoute les coordonnées du dépot aux listes
        X_list.insert(0, depotnorm[0])
        Y_list.insert(0, depotnorm[1])

        print(X_list, "\n", Y_list)
        #On rajoute la demande du dépot à d (0)
        d_list.insert(0,0)
        print(d_list)
        print ("\n")

        trajets=best_route[1]
        vehicules=best_route[2]
        vehicules=vehicules.tolist()
        print("trajets:",trajets)
        print("vehicules:",vehicules)
        while trajets[-1] == 0 and trajets.count(0) > 1:
            trajets.pop()
            vehicules.pop()
        print("trajets:",trajets)
        print("vehicules:",vehicules)
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
        
        routes = [veh1, veh2, veh3, veh4, veh5] #liste des trajets normalisés pour chaque véhicule
        real_routes=denormalization(routes,xA, yA, xB, yB) # liste des trajets dénormalisés pour chaque véhicule

        with open(filename_out, 'w') as f2:
            for k in range(5):
                f2.write(f"Véhicule {k+1} :\n")
                for i in range(len(real_routes[k][0])):
                    f2.write(f"Client {i+1} : {real_routes[k][0][i]} \t")
                    if real_routes[k][1][i] == 0:
                        f2.write("Retour au dépôt\n")
                        continue
                    f2.write(f"Demande : {real_routes[k][1][i]}\n")
                f2.write("\n")

        return routes,real_routes,filename_out


class Application(ctk.CTk):
    def __init__(self):

        ctk.CTk.__init__(self)
        self.title("Projet Ingénieur Equipe n°3")

        self.equipments_by_address_index = {}

        # Créer les trois pages
        self.page1 = Page(self, "PI03", "StrasTruck")
        self.page2 = Page(self, "Information adresse", "Adresses en mémoire:")
        self.page3 = Page(self, "Matériels", "Contenu de chaque adresse ")

        # Charger l'image
        self.image_path = "ST.jpg"


        self.image = Image.open(self.image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        # Ajouter un Canvas pour afficher l'image sur la page1
        self.canvas = ctk.CTkCanvas(self.page1, width=200, height=200)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.pack()

        # Créer les boutons pour naviguer entre les pages
        self.button1 = ctk.CTkButton(self.page1, text="Entrez vos adresses de livraison", fg_color='#F51010', command=self.show_page2)
        self.button2 = ctk.CTkButton(self.page2, text="Nouvelle adresse", fg_color='#68CC5E', command=self.new_adresse)
        self.button3 = ctk.CTkButton(self.page2, text="Sauvegarder", fg_color='#4078EE', command=self.save)
        self.button4 = ctk.CTkButton(self.page2, text="Supprimer", fg_color='#E84949',  command=self.delete_address)
        self.button5 = ctk.CTkButton(self.page2, text="Suivant", fg_color='#A7A7A7', command=self.show_page3)
        self.button6 = ctk.CTkButton(self.page3, text="Retour", fg_color='#A7A7A7', command=self.show_page2)
        self.button7 = ctk.CTkButton(self.page3, text="Supprimer equipement", fg_color='#E84949', command=self.delete_equipement)
        #self.button8 = tk.Button(self.page3, text="Lancer", bg='#4078EE', fg='white', command=self.open_map)
        #self.button8 = ctk.CTkButton(self.page3, text="Lancer", fg_color='#4078EE', command=self.recap_equipement)
        self.button9 = ctk.CTkButton(self.page3, text="Ajouter matériels a livrer", fg_color='#68CC5E', command=self.create_dropdown_menu)
        #self.button10 = ctk.CTkButton(self.page3, text="Voir", fg_color='#4078EE', command=self.display_addresses_and_weights)
        self.button11 = ctk.CTkButton(self.page3, text="Lancer", fg_color='#4078EE', command=self.alerte)

        # Création d'un Label pour afficher les phrases enregistrées
        self.label_phrases = tk.Label(self.page2, text="")
        self.label_phrases.pack(pady=10)

        # Ajouter une Listbox pour afficher les adresses enregistrées
        self.address_listbox = tk.Listbox(self.page2)
        self.address_listbox.pack(pady=10)

        self.address_listbox1 = tk.Listbox(self.page3)
        self.address_listbox1.pack(pady=15)

        self.address_listbox2 = tk.Listbox(self.page3)
        self.address_listbox2.pack(pady=122)

        # Placer les boutons dans la fenêtre
        self.button1.pack(side=tk.LEFT)
        self.button2.pack(side=tk.LEFT)
        self.button3.pack(side=tk.RIGHT)
        self.button4.pack(side=tk.RIGHT)
        self.button5.pack(side=tk.BOTTOM)
        self.button6.pack(side=tk.BOTTOM)
        self.button7.pack(side=tk.RIGHT)
        #self.button8.pack(side=tk.RIGHT)
        self.button9.pack(side=tk.LEFT)
        #self.button10.pack(side=tk.LEFT)
        self.button11.pack(side=tk.LEFT)


        # Afficher la première page par défaut
        self.show_page1()

        # Instance variable pour stocker les coordonnées
        self.coordinates = []

    def show_page1(self):
        self.page2.pack_forget()
        self.page3.pack_forget()
        self.page1.pack()

    def show_page2(self):
        self.page1.pack_forget()
        self.page3.pack_forget()
        self.page2.pack()

    def show_page3(self):
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack()

    def new_adresse(self):
        # Ajouter un widget Entry pour la saisie de l'utilisateur
        self.user_input = tk.Entry(self.page2)
        self.user_input.pack(pady=10)

    def save(self):
        phrase_enregistree = self.user_input.get()
        ancien_texte = self.label_phrases.cget("text")
        nouveau_texte = f"{ancien_texte}\n{phrase_enregistree}"
        self.label_phrases.configure(text=nouveau_texte)
        self.user_input.destroy()
        print(nouveau_texte)

        # Récupérer et imprimer les coordonnées
        coordinates = self.transfgeo(phrase_enregistree)
        print(coordinates)

        # Créer une nouvelle liste pour l'adresse enregistrée
        current_address_index = len(self.coordinates) - 1
        self.equipments_by_address_index[current_address_index] = []

        # Ajouter l'adresse à la Listbox
        self.address_listbox.insert(ctk.END, phrase_enregistree)
        self.address_listbox1.insert(ctk.END, phrase_enregistree)


    def delete_address(self):
        selected_index = self.address_listbox.curselection()
        if selected_index:
            deleted_address = self.coordinates.pop(selected_index[0])
            print(f"Adresse supprimée : {deleted_address}")

            # Mettre à jour le texte du label pour retirer la dernière adresse
            current_text = self.label_phrases.cget("text")
            if current_text:
                lines = current_text.split('\n')
                updated_text = '\n'.join(lines[:-1])  # Retirer la dernière ligne
                self.label_phrases.config(text=updated_text)

            # Supprimer l'adresse de la Listbox
            self.address_listbox.delete(selected_index)
            self.address_listbox1.delete(selected_index)

        else:
            print("Aucune adresse sélectionnée.")


    def create_dropdown_menu(self):
        # Créer un sous-menu pour le menu principal
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Chaise", command=self.option1)
        file_menu.add_command(label="Banc", command=self.option2)
        file_menu.add_command(label="Table", command=self.option3)
        file_menu.add_command(label="Barrière Heras", command=self.option4)
        file_menu.add_command(label="Barrière Vauban", command=self.option5)
        file_menu.add_command(label="Béton", command=self.option6)

        file_menu.post(self.button9.winfo_rootx(), self.button9.winfo_rooty() + self.button9.winfo_height())

    def close_spinbox(spinbox_window):
        spinbox_window.destroy()

    def option1(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 1 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} chaises")
            self.equipement(poid1)

    def option2(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 2 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} bancs")
            self.equipement(poid1)


    def option3(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 0.4 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} tables")
            self.equipement(poid1)


    def option4(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 1 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} barrières Heras")
            self.equipement(poid1)


    def option5(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 0.3 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} barrières Vauban")
            self.equipement(poid1)



    def option6(self):
        selected_index = self.address_listbox1.curselection()
        current_address_index = selected_index[0]

        # Créer une nouvelle fenêtre pour le Spinbox
        self.spinbox_window = tk.Toplevel(self)

        # Créer une variable de contrôle pour le Spinbox
        self.spinbox_value = tk.StringVar()

        # Créer le Spinbox dans la nouvelle fenêtre et le lier à la variable de contrôle
        self.spinbox = tk.Spinbox(self.spinbox_window, from_=0, to=10000, textvariable=self.spinbox_value)
        self.spinbox.pack()

        def close_spinbox():
            self.spinbox_window.destroy()

        # Créer un bouton "Valider" pour fermer la fenêtre de la Spinbox
        close_button = tk.Button(self.spinbox_window, text="Valider", command=close_spinbox)
        close_button.pack()

        self.spinbox_window.wait_window(self.spinbox_window)  # Attendre que l'utilisateur ferme la fenêtre de la Spinbox

        # Récupérer la valeur du Spinbox à partir de la variable de contrôle
        nb = int(self.spinbox_value.get())

        if selected_index and nb > 0:
            poid1 = 6 * nb
            self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",f"{nb} bétons")
            self.equipement(poid1)


    def equipement(self, poid1):
        #bancs
        selected_index = self.address_listbox1.curselection()
        if selected_index:
            current_address_index = selected_index[0]
            self.equipments_by_address_index[current_address_index].append(poid1)
            #Liste avec le poids
            #self.address_listbox2.insert(tk.END,f"adresse numéro{current_address_index+1}",self.equipments_by_address_index[current_address_index])
            print(current_address_index)
            print(self.equipments_by_address_index[current_address_index])


    def recap_equipement(self):
        recap_list = []  # Liste pour stocker le récapitulatif des équipements par adresse
        for address_index, equipments in self.equipments_by_address_index.items():
            total_weight = 0  # Poids total pour cette adresse
            for equipment in equipments:
                total_weight += equipment  # Ajouter le poids de l'équipement au poids total
            address = self.address_listbox1.get(address_index)  # Obtenir l'adresse correspondante
            recap_list.append((address, total_weight))  # Ajouter l'adresse et le poids total à la liste
        self.address_listbox2.insert(tk.END,f"poids total{recap_list}")
        return recap_list


    def delete_equipement(self):
        selected_index = self.address_listbox1.curselection()
        print(selected_index)

        if selected_index:
            current_address_index = selected_index[0]
            self.equipments_by_address_index[current_address_index].pop()
            self.address_listbox2.insert(tk.END,"adresse numéro dernier equipement supprimé")


    def open_map(self, coordinates_list):

         # Créer une carte Folium
        m = folium.Map(location=[48.576995, 7.766849], zoom_start=12)
        # Ajouter un marqueur à l'adresse spécifiée
        for i, coord in enumerate(self.coordinates, start=1):
            popup_text = f"Adresse {i}"

            folium.Marker(coord, popup=popup_text).add_to(m)

        m.save("map.html")
        webbrowser.open("map.html")
        # Ajouter le dépôt à la liste des coordonnées (début et fin de la tournée)
        coordinates_list.insert(0, [48.5919883, 7.7807406])
        coordinates_list.append([48.5919883, 7.7807406])
  
        # Pour chaque paire de points, ouvrez GoogleMaps avec la destination
        for i in range(len(coordinates_list) - 1):
            start = coordinates_list[i]
            end = coordinates_list[i + 1]

            # Créez le lien deeplink pour Google Maps
            google_maps_link = f"https://www.google.com/maps/dir/{start[0]},{start[1]}/{end[0]},{end[1]}"

            # Ouvrez Google Maps avec le point de départ et la destination
            webbrowser.open(google_maps_link)

    def transfgeo(self, adresse):
        query = f'{adresse}, Strasbourg, France'
        results = geocoder.geocode(query)

        if results and len(results) > 0:
            coordinates = [results[0]['geometry']['lat'], results[0]['geometry']['lng']]
            self.coordinates.append(coordinates)
            return coordinates
        else:
            print(f"Aucun résultat trouvé pour l'adresse : {adresse}")
            return None


    def display_addresses_and_weights(self):
        # Effacer les éléments précédents dans les listes de la listbox
        self.address_listbox1.delete(0, tk.END)
        self.address_listbox2.delete(0, tk.END)

        # Parcourir les adresses et les équipements associés
        for coord, equipments in zip(self.coordinates, self.equipments_by_address_index.values()):
            # Ajouter les coordonnées à la listebox
            self.address_listbox1.insert(tk.END, f"Coordonnées : {coord}")

            # Calculer le poids total des équipements pour cette adresse
            total_weight = sum(equipments)

            # Ajouter le poids total des équipements à la listebox
            self.address_listbox2.insert(tk.END, f"Poids total des équipements : {total_weight} ")


    def alerte(self):
        response=messagebox.askquestion("Confirmation", "Voulez-vous ouvrir la carte?")
        if response == 'yes':
            data={
                "coordonnees": app.get_coordinates_list(),
                "demandes": app.get_total_weights_list()
            }
            with open('temp.json', 'w') as f:
                json.dump(data, f)
            routes,real_routes,filename_out=self.opti()
            coord=real_routes[0][0]
            self.open_map(coord)

    def opti(self):
        with open('temp.json', 'r') as f:
            data = json.load(f)
        # Afficher les données
        print("data :", data)

        # Extraire les listes de coordonnées et de demandes
        coordinates = data['coordonnees']
        demands = data['demandes']

        # Créer des listes de longitudes (X_list) et de latitudes (Y_list)
        X_list = [coord[1] for coord in coordinates]  # longitudes
        Y_list = [coord[0] for coord in coordinates]  # latitudes

        print("X : ",X_list)
        print("Y : ",Y_list)
        # La liste des demandes est déjà dans 'demands'
        d_list = demands
        print("d : ",d_list)

        # Normaliser les données avec normalization.py
        x_norm,y_norm,d_norm,depot_norm = normalization.normalization(X_list,Y_list,d_list,x_depot,y_depot,xA,yA,xB,yB)

        print("depot_norm : ",depot_norm)
        print("x_norm : ",x_norm)
        print("y_norm : ",y_norm)
        print("d_norm : ",d_norm)
        print("\n")

        N=len(x_norm) #nombre de clients

        # Afficher les données normalisées
        display(x_norm,y_norm,d_norm)

        #Génération des données sous le bon format (commande bash)
        args1 = ["python", "generate_real_data.py", "--X_list", *map(str, x_norm), "--Y_list", *map(str, y_norm), "--d_list", *map(str, d_norm), "--graph_size", str(N)]

        # Exécuter le script et capturer la sortie et les erreurs
        result1 = subprocess.run(args1, capture_output=True, text=True)

        # Imprimer la sortie standard
        print("Output1:", result1.stdout)

        # Imprimer les erreurs
        print("Errors1:", result1.stderr)

        args2 = ["python", "fleet_v5/eval.py", f"real_data/hcvrp/hcvrp_v5_{N}_seed24610.pkl", "-f", "--model", "fleet_v5/outputs/hcvrp_40/epoch-20.pt", "--decode_strategy", "greedy", "--obj", "min-sum"]
        result2 = subprocess.run(args2, capture_output=True, text=True)

        print("Output2:", result2.stdout)
        print("Errors2:", result2.stderr)

        resultats=get_results(N)
        #print(resultats)
        best_route,ind_min,min_cost=get_best_route(resultats)
        cout,trajets,vehicules,duree=best_route
        vehicules=vehicules.tolist()
        print("coût :", cout)
        print("trajets :", trajets)
        print("véhicules utilisés :", vehicules) # de 0 à 4 pour les 5 véhicules
        print("durée de calcul :", duree)

        routes,real_routes,filename_out=trajets_finaux(best_route,x_norm,y_norm,d_list,depot_norm,N)
        display_results(routes)
        return routes,real_routes,filename_out

    def get_coordinates_list(self):
        coordinates_list = []
        for coord in self.coordinates:
            coordinates_list.append(coord)
        print(coordinates_list)
        return coordinates_list


    def get_total_weights_list(self):
        total_weights_list = []
        for address_index, equipments in self.equipments_by_address_index.items():
            total_weight = sum(equipments)
            total_weights_list.append(total_weight)
        print(total_weights_list)
        return total_weights_list
    


class Page(ctk.CTkFrame):
    def __init__(self, master, title, content, bg_color=None):
        super().__init__(master)
        self.title_label = ctk.CTkLabel(self, text=title, font=("Helvetica", 16))
        self.title_label.pack(pady=10)
        self.content_label = ctk.CTkLabel(self, text=content)
        self.content_label.pack(pady=20)
        self.configure(fg_color="#FFFFFF")
        #self.title_label.configure(bg='#F51010', fg='white')
        #self.content_label.configure( fg_color='#F51010')#bg='#F51010',
        if bg_color:
            self.config(bg=bg_color)


if __name__ == "__main__":
    geocoder = OpenCageGeocode('2e598f1bc13e48cda885fd64b1e49c53')
    app = Application()
    app.geometry("1000x950")
    app.iconbitmap("ST.jpg") # Ajouter une icône à la fenêtre
    app.config(background='white')
    app.mainloop()
