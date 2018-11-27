import numpy as np
import cv2
import matplotlib.pyplot as plt
import os



def pronadji_rectangle(ivica_slike):
    broj_redova = len(ivica_slike);
    broj_kolona = len(ivica_slike[0]);

    (x1, y1) = (0, 0);
    (x2, y2) = (0, 0);

    brejk = 0;

    firstx = 1;
    firsty = 1;

    for i in range(broj_kolona):
        for j in range(broj_redova):
                if (ivica_slike[j][i] == 255):
                    if (firstx):
                        x1 = i;
                        firstx = 0;
                    else:
                        x2 = i;

    for i in range(broj_redova):
        for j in range(broj_kolona):
                if (ivica_slike[i][j] == 255):
                    if (firsty):
                        y1 = i;
                        firsty = 0;
                    else:
                        y2 = i;
    

    if (x1 > 0):
        x1 -= 1;
    if (x2 < broj_kolona - 1):
        x2 += 1;
    if (y1 > 0):
        y1 -= 1;
    if (y2 < broj_redova - 1):
        y2 += 1;

    return [(x1, y1), (x2, y2)];
#_____________________________________________________________DataPrep1



def obradiDataset(folderOriginal, folderNovi, funkcijaObrade):
    for i in range(10):
        lokacijaOriginalFoldera = folderOriginal + r"\{0}".format(i)
        k = 0
        for slikica in os.listdir(lokacijaOriginalFoldera):
            lokacijaOriginalSlike = folderOriginal + r"\{0}".format(i) +"\\" + slikica
            img1 = cv2.imread(lokacijaOriginalSlike)
            img2 = funkcijaObrade(img1)
            lokacijaNovogFoldera = folderNovi + r"\{0}".format(i)
            if not os.path.exists(lokacijaNovogFoldera):
                os.makedirs(lokacijaNovogFoldera)
            lokacijaNoveSlike = folderNovi + r"\{0}".format(i) + r"\{0:{fill}3}.png".format(k, fill = "0=")
            k+=1
            cv2.imwrite(lokacijaNoveSlike,img2)
#_____________________________________________________DataPrep1

def razdvojiValidacijskePodatke(folderOriginal, folderValidacije):
    for i in range(10):
        lokacijaOriginalFoldera = folderOriginal + r"\{0}".format(i)
        BrojSlika = 0
        for filename in os.listdir(lokacijaOriginalFoldera):
            BrojSlika+=1
        for k in range(BrojSlika- int(0.2*BrojSlika), BrojSlika):
            lokacijaOriginalSlike = folderOriginal + r"\{0}".format(i) + r"\{0:{fill}3}.png".format(k, fill = "0=")
            lokacijaNovogFoldera = folderValidacije + r"\{0}".format(i)
            if not os.path.exists(lokacijaNovogFoldera):
                os.makedirs(lokacijaNovogFoldera)
            lokacijaValidacijskeSlike = folderValidacije + r"\{0}".format(i) + r"\{0:{fill}3}.png".format(k, fill = "0=")
            os.rename(lokacijaOriginalSlike,lokacijaValidacijskeSlike)
#______________________________________________________________________DataPrep4

def filtriranje(img1):
    img2 = np.copy(img1)
    ivica = cv2.Canny(img2, 200, 300)
    tacke = pronadji_rectangle(ivica)
    img2 = img2[tacke[0][1]:tacke[1][1]  ,tacke[0][0]:tacke[1][0]] #umjesto maske za anotacije ovdje croppamo sliku
#_________________________________________________________________DataPrep1
# U biti ovo mogu biti i 2 funkcije koje bismo pozivali naknadno pomocu obradiDataset, ali ovako je brze
    
    img2 = img2*1.35 +3 #(np.power( img2, 0.8)) # brightness and contrast
    img2[np.where(img2>255)] = 255
    img2 = img2.astype('uint8')
    img3 = cv2.Laplacian(img2,cv2.CV_64F)
    img3 = img2.astype("int16") - (img3*0.1).astype("int16") #laplacian
    img3[np.where(img3>255)] = 255
    img3 = img3.astype("uint8")
    #img4 = np.copy(img3)
    # cv2.equalizeHist(img3,img4) #ujednacavanje daje lose rezultate
    return img3
#___________________________________________________________________DataPrep3


def ukloni_sum(slika):
    return cv2.blur(slika, (3, 3));

def izostri_sliku(slika):
    return slika + (slika - cv2.blur(slika, (3, 3)));

#_________________________________________________________DataPrep2

def obradi_i_dodaj_slike(putanja_izvor, putanja_destinacija):
    for broj in range(10):
        putanja_orig = putanja_izvor + str(broj) + '/';
        putanja_cropped = putanja_destinacija + str(broj) + '/';
        lista_naziva_slika = os.listdir(putanja_orig);

        for naziv_slike in lista_naziva_slika:
            slika = cv2.imread(putanja_orig + naziv_slike, cv2.IMREAD_GRAYSCALE);
            slika += slika - cv2.blur(slika, (3, 3));
            cv2.imwrite(putanja_cropped + naziv_slike, slika);        
#__________________________________________________________________________________DataPrep1 
#odvojeno napravila 2 clana tim, moze se koristiti bilo koja



obradiDataset(r"C:\Users\userr\vscodePython\poosProjekat", r"C:\Users\userr\vscodePython\poosProjekat\IzostrenoMesud",izostri_sliku)
#razdvojiValidacijskePodatke(r"C:\Users\userr\vscodePython\poosProjekat\CroppedAndFiltered", r"C:\Users\userr\vscodePython\poosProjekat\CroppedAndFilteredValidacija")
