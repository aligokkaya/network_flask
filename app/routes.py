import cv2
import mysql.connector
import smtplib
from flask import flash, request, redirect, url_for, current_app,send_from_directory,render_template, session
from datetime import  date, datetime
from functools import wraps
import pandas as pd
from email.mime.text import MIMEText
import smtplib
from pandas import json_normalize
from app import app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return decorated_function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["yetki"]==1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("index"))

    return decorated_function

try:
    mydb = mysql.connector.connect(
        host="hypegenai.com",
        user="hypegena",
        password="aZ5xjXf133",
        database="hypegena_chain"
    )
    
    mycursor2 = mydb.cursor(buffered=True)
    mycursor3 = mydb.cursor(buffered=True)
except Exception as e:
    print(e)

with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)
app.secret_key = 'super secret key'

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# mail=session["username"]
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


def eslesme():
    sol_ayak_toplam_para=0
    sag_ayak_toplam_para=0
    mycursor = mydb.cursor(buffered=True, dictionary=True)
    mycursor2 = mydb.cursor(buffered=True, dictionary=True)
    sol_ayak=mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(session['atanan_ref'])+'1'+"%"+ "'")
    sag_ayak=mycursor2.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(session['atanan_ref'])+'2'+"%"+ "'")
    mycursor.execute(sol_ayak)
    mycursor2.execute(sag_ayak)
   
    try:
        session['ekipsayisi'] = int(len(sol_ayak))+int(len(sag_ayak))
        myresult1 = mycursor.fetchall()
        myresult2 = mycursor2.fetchall()
        # print(session['atanan_ref'])
        print('sol_ayak+++++++++++++++++++++++++++++++++++++++++++++')
        print((myresult1))
        for i in range(len(myresult1)):
                sol_ayak_toplam_para=sol_ayak_toplam_para+myresult1[i]['yatirilan_para']
                print("---------")
        for i in range(len(myresult2)):
                sag_ayak_toplam_para=sag_ayak_toplam_para+myresult2[i]['yatirilan_para']
                print("---------")
        
        
        esle=min(sol_ayak_toplam_para,sag_ayak_toplam_para)
        print((esle))
        session['puan']=session['puan']+(esle/10)
    except:
        session['ekipsayisi']=session['atanan_ref']
        session['puan']=session['puan']
   


    return True

@app.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    print("-----------")
    print(session['puan'])
    toplam_para=float(session['puan'])*2.342

    alinan_paket = "Alınan Paket Numarasi" +str("1") +"& 3.Sunucu Sistemi Barındırıyor."

    return render_template("update.html",toplam_para=toplam_para,alinan_paket=alinan_paket)

@app.route('/uploads/<name>')
@login_required
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_file", methods=['GET', 'POST'])
@login_required
def upload_file():
    
    dataframe=[]
    username =[]
    mail_array = []
    tel_array = []
    ust_referans = []
    atanan_referans = []
    if request.method == 'POST':
        if request.form.get("button") == "value":
            # print("girdi")
            mycursor = mydb.cursor(dictionary=True)
            # print(str(session['atanan_ref']))
            mycursor.execute("SELECT * FROM users2 WHERE ust_referans LIKE '"+str(session['atanan_ref'])+"%"+ "'")
            
            myresult = mycursor.fetchall()
            # print(myresult)
            mycursor.close()
            dataframe = pd.DataFrame.from_dict(myresult)
            print("--------------")
           
            try:    
                # dataframe=(dataframe.iloc[1::])
                for i in range(len(dataframe)):
                    
                    username.append(str(dataframe['name_surname'].iloc[i]))
                    mail_array.append(str(dataframe['mail'].iloc[i]))
                    tel_array.append(str(dataframe['tel'].iloc[i]))
                    atanan_referans.append(str(dataframe['atanan_ref'].iloc[i]))
                    ust_referans.append(str(dataframe['ust_referans'].iloc[i]))
            except:
                pass
        if request.form.get("button") == "value2":
            ref = request.form.get("ref")
            print(ref)

            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(ref)+"%"+ "'   ORDER BY id ASC     LIMIT 3   ")
            ilk_ref = []
            mail_array = []
            myresult = mycursor.fetchall()
            for i in myresult:
                print(i)
                
                ilk_ref.append(str(i[7]))
                mail_array.append(str(i[3]))
            mycursor.close()

            img=cv2.imread("./app/static/img/beyaz1.jpg")
            cv2.rectangle(img, (310,40), (380,110), (0,255,0), 2)

            ###RECTANGLE
            cv2.rectangle(img, (125,320), (195,390), (0,255,0), 2)
            cv2.rectangle(img, (490,320), (560,390), (0,255,0), 2)

            start_point= (222,193)


            end_point = (176,253)

            image = cv2.line(img, start_point, end_point, (0,255,0), 2)

            #######################################
            start_point2= (471,193)


            end_point2 = (523,253)

            image = cv2.line(img, start_point2, end_point2, (0,255,0), 2)


##PUTTEXT

            try:
                    
                cv2.putText(img=img, text='Referans No : '+str(ref), org=(225, 140), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)

                cv2.putText(img=img, text='Mail No : '+str(mail_array[0]), org=(225, 175), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)

            except Exception as e:
                print(e)

            try:
                cv2.putText(img=img, text='Referans No : '+str(ilk_ref[1]), org=(55, 275), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)
                cv2.putText(img=img, text='Mail No : '+str(mail_array[1]), org=(55, 305), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)

            except Exception as e:
                print(e)

            try:
                cv2.putText(img=img, text='Referans No : '+str(ilk_ref[2]), org=(415, 275), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)
                cv2.putText(img=img, text='Mail No : '+str(mail_array[2]), org=(415, 305), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 0),thickness=1)

            except Exception as e:
                print(e)
            
            dosya_path = "./app/static/agac/"+str(session['referans'])+".jpg"
            cv2.imwrite(str(dosya_path),img)
            dosya_path = "./static/agac/"+str(session['referans'])+".jpg"
            

            return render_template("upload_file.html",dosya_path=dosya_path,atanan_referans=atanan_referans,ust_referans=ust_referans,username=username,mail_array=mail_array,tel_array=tel_array)


    return render_template("upload_file.html",atanan_referans=atanan_referans,ust_referans=ust_referans,username=username,mail_array=mail_array,tel_array=tel_array)
@app.route("/", methods=['GET', 'POST'])
def anasayfa():
    return render_template("anasayfa.html")


@app.route("/anasayfa", methods=['GET', 'POST'])
def anasayfa1():
    return render_template("anasayfa.html")

    
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    try:
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute("select*from money where mail='" +
                            str(session['mail'])+"' ORDER BY ıd DESC")
            myresult = mycursor.fetchall()
            mycursor.close()
            aktif_para=str(myresult[0]['para'])
            session["aktif_para"]=aktif_para

    except Exception as e:
        print(e)
    return render_template("index.html")

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
  
    twitter_kullanici_adi = session["username"]

    try:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            "select*from users WHERE name_surname = '"+str(twitter_kullanici_adi)+"' ")
        myresult = mycursor.fetchall()
        mycursor.close()
        for i in myresult:
            twitter_kullanici_adi = i[3]
            name_surname = i[4]
    except:
        pass

    if request.method == 'POST':
        mail = session["username"]

        old_pass = request.form.get("password_current")
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select*from users where mail='" +
                         str(mail)+"' and pass='"+str(old_pass)+"'")
        myresult = mycursor.fetchall()
        mycursor.close()
        if myresult:
            newpass1 = request.form.get("password")
            newpass2 = request.form.get("password_confirmation")
            if newpass1 == newpass2:
                mycursor2 = mydb.cursor(buffered=True)
                mycursor2.execute("update users SET pass='" +
                                  newpass1+"' where mail='"+mail+"'")
                mydb.commit()
                mycursor2.close()
                flash("Şifre Değiştirildi",'info')
            else:
                flash("Şifre Değiştirelemedi",'info')

    new_name = request.form.get("name")
    mail = request.form.get("email")

    if request.method == 'POST':
        if request.form.get("button") == "value":

            try:
                sql = "UPDATE users SET mail = '" + \
                    str(mail)+"' WHERE name_surname = '" + \
                    str(twitter_kullanici_adi)+"' "
                mycursor = mydb.cursor(buffered=True)
                mycursor.execute(sql)
                session["username"] = mail
                twitter_kullanici_adi = session["username"]
                mydb.commit()
                mycursor.close()

            except Exception as e:
                pass
    return render_template("profile.html", mail=mail, twitter_kullanici_adi=twitter_kullanici_adi)

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route("/yonetim", methods=['GET', 'POST'])
@admin_required
def yonetim():
    input_mail=""
    aktif_para=""
    paket_no_str=""
    tutar_array = []
    mail_array = []
    cuzdan_array = []
    date_array= []
    if request.method == 'POST':
        if request.form.get("button2") == "value_g":
            print("--")
            input_mail = request.form.get("mail_adresi_g")

            print(input_mail)
            try:
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute("select*from cekme_istegi where mail='" +
                                str(input_mail)+"' ORDER BY id DESC")
                myresult = mycursor.fetchall()
                mycursor.close()
                aktif_para=str(myresult[0]['tutar'])



                
            except Exception as e:
                print(e)

            try:
                mycursor = mydb.cursor(dictionary=True)
                mycursor.execute("select*from paket where mail='" +
                                str(session['mail'])+"' ORDER BY id DESC")
                myresult = mycursor.fetchall()
                mycursor.close()
                print(myresult)
                paket_no_str=str(myresult[0]['packet_no'])
                # print(packet_no)
                # session['packet_no']=packet_no
                # aktif_para=str(myresult[0]['para'])
                # session["aktif_para"]=aktif_para


            except Exception as e:
                print(e)


        elif request.form.get("button") == "value":
            print("EKLEME")
            mail = request.form.get("mail")
            eklenecek_para = request.form.get("eklenecek_para")
            print(mail,eklenecek_para)
            try:
                    
                mycursor = mydb.cursor()
                session["aktif_para"]=eklenecek_para
                sql = "INSERT INTO money (mail,para,durum) VALUES (%s, %s,%s)"
                val = (str(mail),str(eklenecek_para),str("ekleme"))
                mycursor.execute(sql, val)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
            except Exception as e:
                print(e)



            try:

                mycursor = mydb.cursor()
                sql = "UPDATE users2 SET yatirilan_para = '"+str(eklenecek_para)+"' WHERE mail = '"+str(mail)+"'"

                # sql = "INSERT INTO money (mail,para,durum) VALUES (%s, %s,%s)"
                # val = (str(mail_cikarma),str(cikarilan_para),str("cikarma"))
                mycursor.execute(sql)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
               
            except Exception as e:
                print(e)

            flash("Para Ekeleme İşlemi Başarılı",'info')






        elif request.form.get("button1") == "value_cikar":
            print("ÇIKARMA")
            mail_cikarma = request.form.get("mail_cikarma")
            cikarilan_para = request.form.get("cikarilan_para")
            session["aktif_para"]=cikarilan_para
            try:

                mycursor = mydb.cursor()
                sql = "UPDATE cekme_istegi SET value = '1' WHERE tutar='"+str(cikarilan_para)+"' and  mail = '"+str(mail_cikarma)+"'"

                # sql = "INSERT INTO money (mail,para,durum) VALUES (%s, %s,%s)"
                # val = (str(mail_cikarma),str(cikarilan_para),str("cikarma"))
                mycursor.execute(sql)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
                print(mail_cikarma,cikarilan_para)
                session['puan']-=int(cikarilan_para)
            except Exception as e:
                print(e)

            try:

                mycursor = mydb.cursor()
                sql = "UPDATE users2 SET yatirilan_para = '"+str(cikarilan_para)+"' WHERE mail = '"+str(mail_cikarma)+"'"

                # sql = "INSERT INTO money (mail,para,durum) VALUES (%s, %s,%s)"
                # val = (str(mail_cikarma),str(cikarilan_para),str("cikarma"))
                mycursor.execute(sql)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
               
            except Exception as e:
                print(e)

        elif request.form.get("button") == "cekim_istek":

            date1=request.form.get("date1")
            print(date1)

            try:
                mycursor = mydb.cursor(dictionary=True)

                # mycursor.execute("select* from user_sinir where date BETWEEN '23.10.2021 00:00' and '23.10.2021 23:59'   ")
                # mycursor.execute('SELECT * FROM user_sinir WHERE date BETWEEN "2021-10-23" AND "2021-10-23" AND mail='+session['username']+'      ')
                mycursor.execute('SELECT * FROM `cekme_istegi` WHERE  date BETWEEN "'+str(date1)+' 00:00:00" AND "'+str(date1)+' 23:59:59"')
                # mycursor.execute("SELECT * FROM user_sinir WHERE eklenme_tarihi BETWEEN '01.01.2018 00:00' and '01.05.2018 23:59'")
                myresult=mycursor.fetchall()
                mycursor.close()
                
              
                print(myresult)
                dataframe = pd.DataFrame.from_dict(myresult)
                for i in range(len(dataframe)):
                    tutar_array.append(str(dataframe['tutar'].iloc[i]))
                    
                    
                    
                    mail_array.append(str(dataframe['mail'].iloc[i]))
                    cuzdan_array.append(str(dataframe['soguk_cuzdan'].iloc[i]))
                    date_array.append(str(dataframe['date'].iloc[i]))

                    
            except Exception as e:
                print(e)
        elif request.form.get("button_p") == "paket":
            mail=request.form.get("mail")
            print(mail)
            paket_no=request.form.get("paket_no")
            print(paket_no)
            try:
                tarih=datetime.now()
                
                mycursor = mydb.cursor()

                sql = "INSERT INTO paket (mail,packet_no) VALUES (%s, %s)"
                val = (str(mail),str(paket_no))
                mycursor.execute(sql, val)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
               
                flash("Paket İsteği Gönderimi Başarılı",'info')
            except Exception as e:
                print(e)
                flash("Paket İsteği Gönderimi Başarısız",'info')

    return render_template("yonetim.html",paket_no_str=paket_no_str,date_array=date_array,tutar_array=tutar_array,mail_array=mail_array,cuzdan_array=cuzdan_array,input_mail=input_mail,aktif_para=aktif_para)

@app.route("/sosyalmedya", methods=['GET', 'POST'])
@login_required
def sosyalmedya():

    link_array = []
    date_array = []
    if request.method == 'POST':
        if request.form.get("button3") == "value_2":
            print("burda")
            try:

                file_on = request.files['file_on']
                if file_on and allowed_file(file_on.filename):
                    now_save=datetime.now()
                    file_on.save("./app/static/social_image/"+str(now_save)+"-"+str(session['mail'])+".jpg")
                    flash("Resim Gönderimi Başarılı",'info')

                    print("aldik")
            except Exception as e:
                flash("Resim Gönderimi Başarısız!!",'info')
                print(e)

        if request.form.get("button1") == "value_g":

            if session['atanan_para']>0:







            
                link = request.form.get("link")
                print(link)
                print(session['mail'])
                
                link_date=(datetime.now())
                link_date=str(link_date)

                try:
                    link_date=(datetime.now())
                    print(link_date)
                    link_date=str(link_date)
                    link_date=(link_date[0:10])
                    baslangic=link_date+" 00:00:00"
                    bitis=link_date+" 23:59:00"
                    mycursor = mydb.cursor()
                    mycursor.execute("select*from social where mail='"+str(session['mail'])+"' and  link_date>='"+baslangic+"' and link_date<='"+bitis+"'       ")
                    myresult = mycursor.fetchall()
                    # print(myresult)

                    print(len(myresult))

                    if len(myresult)<2:
                        try:

                            mycursor = mydb.cursor()
                            sql = "INSERT INTO social (mail,link,link_date,value) VALUES (%s, %s,%s, %s)"

                            val = (str(session['mail']),str(link),str(link_date),0)
                            mycursor.execute(sql, val)

                            mydb.commit()
                            print(mycursor.rowcount, "record inserted.")
                            mycursor.close()
                            flash("Link Ekleme Başarılı",'info')

                        except Exception as e:
                            print(e)
                    else:
                        flash("Günlük Limit Doldu 24 Saat Sonra Tekrar Deneyin",'info')

                except Exception as e:
                    flash("Link Ekleme Başarısız Oldu Daha Sonra Tekrar Deneyin",'info')
                    print(e)
            else:
                # flash("Link Ekleme Başarısız Ödeme Yapmadınız",'info')
                flash("Link Ekleme Başarısız Link Eklemek İçin Lütfen Paket Ödemesi Yapınız !",'info')
                
     
        if request.form.get("button2") == "goruntule":
            link_date=(datetime.now())
            print(link_date)
            link_date=str(link_date)
            link_date=(link_date[0:10])
            baslangic=link_date+" 00:00:00"
            bitis=link_date+" 23:59:00"
          
            try:
                mycursor = mydb.cursor()
                mycursor.execute("select*from social where link_date>='"+baslangic+"' and link_date<='"+bitis+"'    ORDER BY RAND() LIMIT 8  ")
                myresult = mycursor.fetchall()
                print(myresult)

                for i in myresult:
                    print(i)
                    link_array.append(i[2])

                    date_array.append(i[3])
                mycursor.close()
             
            except Exception as e:
                print(e)
        return render_template("sosyalmedya.html",link_array=link_array,date_array=date_array)

    # except Exception as e:
    #     print(e)

    return render_template("sosyalmedya.html")

@app.route("/fileupload", methods=['GET', 'POST'])
@login_required
def fileupload():

    if request.method == 'POST':
        if request.form.get("button1") == "value_g":
            try:

                file_on = request.files['file_on']
                if file_on and allowed_file(file_on.filename):
                    now_save=datetime.now()
                    file_on.save("./app/static/social_image/"+str(now_save)+"-"+str(session['mail'])+".jpg")
                    flash("Resim Gönderimi Başarılı",'info')

                    print("aldik")
            except Exception as e:
                flash("Resim Gönderimi Başarısız!!",'info')
                print(e)

    
    return render_template("fileupload.html")

@app.route("/raporlar", methods=['GET', 'POST'])
@login_required
def raporlar():
    len_dataframe=""
    aylık_tahmin=""
    try:
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(session['atanan_ref'])+"%"+ "'")
                

        myresult = mycursor.fetchall()
        print(myresult)
        mycursor.close()
        dataframe = pd.DataFrame.from_dict(myresult)
        len_dataframe=len(dataframe)
        session['ekip_sayisi']=int(len_dataframe)+1

        aylık_tahmin=int(len_dataframe)*180*1.13*int(session['puan'])
    except Exception as e:
        print(e)
    return render_template("raporlar.html",len_dataframe=len_dataframe,aylık_tahmin=aylık_tahmin)




@app.route("/parayatir", methods=['GET', 'POST'])
@login_required
def paraupload():
    if request.method == 'POST':
        if request.form.get("button1") == "goruntule":
            try:
                file_on = request.files['file_on']
                hash = request.form.get("hash")
                print(hash)
                if file_on and allowed_file(file_on.filename):
                    now_save=datetime.now()
                    print("buradaaa")
                    file_on.save("./app/static/para/"+str(hash)+"-"+str(now_save)+"-"+str(session['mail'])+".jpg")
                    flash("Resim Gönderimi Başarılı",'info')

                    print("aldik")
            except Exception as e:
                flash("Resim Gönderimi Başarısız!!",'info')
                print(e)

    
    return render_template("parayatir.html")

@app.route("/cekme", methods=['GET', 'POST'])
@login_required
def cekme():
    tutar_array = []
    cuzdanNO = []
    date_array = []
    value=[]
    if request.method == 'POST':
        if request.form.get("button") == "goruntule":
            print("girdi")
            mycursor = mydb.cursor(buffered=True)
           
        
            sql = "SELECT * FROM cekme_istegi WHERE mail= '"+str(session['mail'])+"'"
            # sql = "SELECT * FROM users2 WHERE ust_referans= '"+str(session['atanan_ref']) + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            print(myresult)

            for i in myresult:
                print(i[4])
                print(type(i[4]))
                tutar_array.append(str(i[2]))
                cuzdanNO.append(str(i[3]))
                date_array.append(str(i[4]))
                if i[5]==1:
                    value.append("Onaylandı")
                if i[5]==0:
                    value.append("Beklemede")



        if request.form.get("button") == "value":
            tutar = request.form.get("tutar")
            cuzdan = request.form.get("cuzdan")
            print(tutar,cuzdan)

            #

            #çekme isteklerini görebilceek yer yap

            #
            try:
                tarih=datetime.now()
                
                mycursor = mydb.cursor()

                sql = "INSERT INTO cekme_istegi (mail,tutar,soguk_cuzdan,date,value) VALUES (%s, %s,%s, %s,%s)"
                val = (str(session['mail']),str(tutar),str(cuzdan),str(tarih),0)
                mycursor.execute(sql, val)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
                flash("Çekme İsteği Gönderimi Başarılı",'info')
            except Exception as e:
                print(e)
                flash("Çekme İsteği Gönderimi Başarısız",'info')

    

    return render_template("cekme.html",date_array=date_array,tutar_array=tutar_array,cuzdanNO=cuzdanNO,value=value)

@app.route("/forms", methods=['GET', 'POST'])
@login_required
def forms():
    twitter_kullanici_adi = session["username"]
    result_mail = ""
    if request.method == 'POST':

        if request.form.get("button") == "value":
            name_suname = request.form.get("isim_soyisim")
            telefon = request.form.get("telefon")
            konu = request.form.get("konu")
            baslik = request.form.get("baslik")
            mesaj = request.form.get("mesaj")
            to = ['yildizemre2@hotmail.com', 'yildizemre2@gmail.com']
            subject = baslik
            body = name_suname+"n"+telefon+" "+konu+"\n"+mesaj

            account = 'ali.gkky196@gmail.com'
            password = 'Ali19671570'

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.ehlo()

            server.starttls()

            server.login(account, password)
            mail = MIMEText(body, 'html', 'utf-8')
            mail['From'] = account
            mail['Subject'] = subject
            mail['To'] = ','.join(to)
            mail = mail.as_string()

            try:
                server.sendmail(account, to, mail)
                result_mail = ('Mail gönderimi başarılı')
                flash("Mail gönderimi başarılı",'info')

            except:
                result_mail = ('Mail gönderimi başarısız')
                flash("Mail gönderimi başarısız",'info')

    return render_template("forms.html", result_mail=result_mail, twitter_kullanici_adi=twitter_kullanici_adi)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        toplam_para=0
        email = request.form.get("email")
        password = request.form.get("pass")
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("select*from users2 where mail='" +
                         email+"' and password='"+password+"'")
        myresult = mycursor.fetchall()
        mycursor.close()

        # print(myresult)
        if myresult:
            
            for i in myresult:
                session["username"]=i[1]
                session["yetki"]=i[9]
                session['atanan_ref']=i[7]
                session['referans']=i[6]
                session['atanan_para']=i[10]
                session['mail']=i[3]
                session['ustreferans']=i[11]
                session['puan']=0
            session["logged_in"] = True


            #############################################################################
            mycursor = mydb.cursor(buffered=True, dictionary=True)
            print(str(session['atanan_ref']))
            print("---------------")
            sql = "SELECT * FROM users2 WHERE ust_referans= '"+str(session['atanan_ref'])+"'"
            # sql = "SELECT * FROM users2 WHERE ust_referans= '"+str(session['atanan_ref']) + "'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            # print("---------")
            print(len(myresult))
            # print("---------")
            print(myresult)
            for i in range(len(myresult)):
                
                if str(myresult[i]['yatirilan_para'])[0]=="-":
                    pass
                else:

                    toplam_para=toplam_para+myresult[i]['yatirilan_para']
                    print("---------")


            print("---------")
            print(toplam_para)
            session['puan']=toplam_para*30/100
            if len(myresult)>=14:
                session['puan']=session['puan']+50
            eslesme()

            try:
                mycursor = mydb.cursor(buffered=True)
                # "SELECT * FROM users2 WHERE ust_referans= '"+str(session['atanan_ref'])+"'"
                sql = "SELECT sum(tutar) FROM `cekme_istegi` WHERE mail='"+session['mail']+"' and value=1 "
                # sql = "SELECT * FROM users2 WHERE ust_referans= '"+str(session['atanan_ref']) + "'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                print(int(myresult[0][0]),"------------")
                session['puan']-=int(myresult[0][0])
            except Exception as e:
                print(e)
            try:
             
                mycursor = mydb.cursor()

                sql = "INSERT INTO session_money (mail,date,puan,ref) VALUES (%s, %s,%s, %s)"
                val = (str(session['mail']),str(datetime.now()),str(session['puan']),str(session['atanan_ref']))
                
                mycursor.execute(sql, val)

                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                mycursor.close()
            except Exception as e:
                print(e)

            return redirect(url_for("index"))

        else:
            return render_template("login.html")
    return render_template("login.html")



@app.route("/singup", methods=['GET', 'POST'])
@login_required
def singup():
    kayit_durumu = ""
    new_ref=""
    if request.method == 'POST':
        if request.form.get("button") == "value":
            name_surname = request.form.get("name_surname")
            tc=0
            email = request.form.get("email")
            password = request.form.get("pass")
            tel = request.form.get("tel")
            ref_number = request.form.get("ref")
            ust_ref_number = request.form.get("ustref")

            sehir =request.form.get("sehir")
            print("sehir",sehir)
            # print(email,password,name_surname)
            
            
            



            if  session['atanan_para']>0:


                try:
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM users2 WHERE atanan_ref LIKE '"+str(ref_number)+"%"+ "'"
                    mycursor.execute(sql)

                    myresult = mycursor.fetchall()
                    print(myresult)
                    print(len(myresult))
                    if (len(myresult)) ==1:
                        print(myresult)
                        new_ref=str(ref_number)+"1"
                    elif len(myresult) == 2:
                        new_ref=str(ref_number)+"2"
                    else:
                        kayit_durumu="Referans Numarası Hatalı oluşturulamadi"
                        return render_template("kayit_ol.html",kayit_durumu=kayit_durumu)
                except Exception as e:
                    print(e)
                    kayit_durumu="Kayit oluşturulamadi"
                    return render_template("kayit_ol.html",kayit_durumu=kayit_durumu)
                # if not len(ref_number)==9:
                #     new_Ref=(str(random.random())[2:11])
                #     # print("burada")
                #     print("if ref",new_Ref)
                ##aynı mail olmamalı dikkat 

                mycursor = mydb.cursor()

                sql = "SELECT * FROM users2 WHERE mail ='"+str(email)+"'"

                mycursor.execute(sql)

                myresult = mycursor.fetchall()
                if (len(myresult))==1:
                    print("Bundan var")
                    kayit_durumu = "Böyle bir mail adresi mevcut !!"
                
                else:
                    print("yok kayit yapilabilir")

                    mycursor = mydb.cursor()

                    sql = "INSERT INTO users2 (name_surname,tc,mail,password,tel,referans,atanan_ref,kayit_tarihi,yetki,yatirilan_para,ust_referans,sehir) VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (str(name_surname),str(tc),str(email),str(password),str(tel),str(ref_number),str(new_ref),str(datetime.now()),str(0),str(0),str(ust_ref_number),str(sehir))
                    mycursor.execute(sql, val)

                    mydb.commit()
                    print(mycursor.rowcount, "record inserted.")
                    mycursor.close()
                    kayit_durumu = "Kayit oluşturuldu"
                    flash("Kayit oluşturuldu",'info')
                    return redirect(url_for("index"))    
            else:
                flash("Kayit Oluşturmak İçin Lütfen Paket Ödemesi Yapınız !",'info')
                return redirect(url_for("index"))    
    return render_template("kayit_ol.html",kayit_durumu=kayit_durumu)





@app.route("/logout")
def logout():
    print("çıkis")
    session.clear()
    print(session)

    return redirect(url_for("login"))


@app.route("/delete/<id>")
def delete(id):
    try:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("delete from kayit_formu where kayitID ="+id+" ")
        mydb.commit()
        mycursor.close()

    except Exception as e:
        pass

    return redirect(url_for("raporlar"))
