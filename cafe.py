import mysql.connector
import time
import smtplib
from random import randint
from pathlib import Path
from tkinter import messagebox
from tkinter import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("gui/")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
EMAIL_ADDRESS = 'sangeerthanacafe@gmail.com'  # your email address
EMAIL_PASSWORD = "xnaqtdrqfaahrzlz" # password
x = randint(99, 200)
window = Tk()
window.geometry("1280x700")
window.iconbitmap(relative_to_assets("image.ico"))
window.title("SANGEERTHANA CAFETERRIA")
canvas = Canvas(window,bg = "#545454",height = 700,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
background_img = PhotoImage(file = relative_to_assets("background.png"))
background = canvas.create_image( 640.0, 361.0,image=background_img)
# ==============================Variables=====================
items=['Burger','Pizza','Vanillacake','Doughnut','Strawberrycake','Chocolatecake','Redvelvettcake']
fileref = "Bill-"+str(x)+'.txt'
PaymentRef = StringVar()
emailID = StringVar()
Burger = StringVar()
Pizza = StringVar()
Doughnut = StringVar()
Vanillacake = StringVar()
Strawberrycake = StringVar()
Chocolatecake = StringVar()
Redvelvettcake = StringVar()
costBurger = StringVar()
costPizza = StringVar()
costVanillacake = StringVar()
costDoughnut = StringVar()
costStrawberrycake=StringVar()
costChocolatecake = StringVar()
costRedvelvettcake = StringVar()
dateRef = StringVar()
subTotal = StringVar()
vat = StringVar()
totalPrice = StringVar()
text_Input = StringVar()
dateRef.set(time.strftime("%d/%m/%y"))
operator = ""
vat.set(0)
Burger.set(0)
Pizza.set(0)
Vanillacake.set(0)
Doughnut.set(0)
Strawberrycake.set(0)
Chocolatecake.set(0)
Redvelvettcake.set(0)
subTotal.set(0)
totalPrice.set(0)
costBurger.set(30)
costPizza.set(40)
costDoughnut.set(20)
costVanillacake.set(90)
costStrawberrycake.set(100)
costChocolatecake.set(120)
costRedvelvettcake.set(180)
emailID.set("Enter_EmailID")
# =============================Functions==================
def tPrice():
    cBprice = int(costBurger.get())
    bBprice = int(costPizza.get())
    fFprice = int(costVanillacake.get())
    sDprice = int(costDoughnut.get())
    aAprice=int(costStrawberrycake.get())
    cCprice=int(costChocolatecake.get())
    dDprice=int(costRedvelvettcake.get())
    cBno = int(Burger.get())
    bBno = int(Pizza.get())
    fFno = int(Vanillacake.get())
    sDno = int(Doughnut.get())
    aAno=int(Strawberrycake.get())
    cCno=int(Chocolatecake.get())
    dDno=int(Redvelvettcake.get())
    tempVat = int(vat.get())
    subPrice = (cBprice * cBno + bBprice * bBno + fFprice * fFno + sDprice * sDno +  cCprice*cCno + dDprice*dDno+ aAprice*aAno)
    totalCost = str('%d' % subPrice)
    totalCostwithVat = str('%d' % (subPrice + (subPrice * tempVat) / 100))
    subTotal.set(totalCost)
    totalPrice.set(totalCostwithVat)
    PaymentRef.set("BILL" + str(x))
def iExit():
    qexit = messagebox.askyesno("Billing System", "Do you want to exit?")
    if qexit > 0:
        window.destroy()
        return
def reset():
    global x
    x = x + 1
    PaymentRef.set("")
    Burger.set(0)
    Pizza.set(0)
    Vanillacake.set(0)
    Doughnut.set(0)
    Strawberrycake.set(0)
    Chocolatecake.set(0)
    Redwelvettcake.set(0)
    subTotal.set(0)
    totalPrice.set(0)
    emailID.set("Enter-EmailID")
def show_bill():
    PaymentRef.set("BILL" + str(x))
def create_bill():
    with open(fileref, 'w') as file1:
        global toFile
        toFile=output()
        file1.write(toFile)
    updatedb()
    messagebox.showinfo("Information", "Bill Generated")
def send_bill():
    global x
    msgcontent='This is your total bill\nYour Reference No: is: Bill' + str(x)+"\n\n"+output()
    msg = MIMEMultipart()
    msg['Subject'] = 'Your bill '
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = emailID.get()+'@gmail.com' # receiver email
    msg.attach(MIMEText(msgcontent,'plain'))
    global toFile
    with open(fileref, "w") as f:
        f.write(toFile)
    with open(fileref,'rb') as f:
        file_data = f.read()
        file_name = "RestaurantBill.txt"
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(file_data)
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', "attachment; filename= " + file_name)
        msg.attach(payload)
    qsend = messagebox.askyesno("Billing System", "Do you want to send the bill?")
    if qsend > 0:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS,emailID.get()+'@gmail.com',msg.as_string())
            messagebox.showinfo("Information", "Bill send successfully")
    else:
        messagebox.showinfo("Information", "Bill  will not send")
def output():
    refno = str(x)
    list0 = ("Reference.no :" + refno).center(55)+"\n\n"
    list1 = "Item"+"Quantity".center(45)+"Cost\n"
    list12 = "____".ljust(23)+"________".ljust(26) + "____\n\n"
    list2 = "Burger".ljust(23) + Burger.get().ljust(26)+ str(int(Burger.get()) * int(costBurger.get())) + "\n"
    list3 = "Pizza".ljust(23) + Pizza.get().ljust(26) + str(int(Pizza.get()) * int(costPizza.get())) + "\n"
    list4 = "Vanillacake".ljust(23) + Vanillacake.get().ljust(26) + str(
        int(costVanillacake.get()) * int(Vanillacake.get())) + "\n"
    list5 = "Doughnut".ljust(23) + Doughnut.get().ljust(26) + str(
        int(Doughnut.get()) * int(costDoughnut.get())) + "\n"
    list6= "Chocolatecake".ljust(23) + Chocolatecake.get().ljust(26)  + str(
        int(Chocolatecake.get()) * int(costChocolatecake.get())) + "\n"
    list7= "Strawberrycake".ljust(23) + Strawberrycake.get().ljust(26) + str(
        int(Strawberrycake.get()) * int(costStrawberrycake.get())) + "\n"
    list8= "Redvelvettcake".ljust(23) + Redvelvettcake.get().ljust(26) + str(
        int(Redvelvettcake.get()) * int(costRedvelvettcake.get())) + "\n"
    list9 =  "Total      = Rs ".rjust(49) + subTotal.get() + "/-" + "\n"
    list10 = "Vat        = Rs ".rjust(49) + str(int(totalPrice.get()) - int(subTotal.get())) + "/-" + "\n"
    list11 = "GrandTotal = Rs ".rjust(49) + totalPrice.get()[:] + "/-"
    String = list0 + list1 + list12 + list2 + list3 + list4 + list5 + list6 + list7 + list8 + list9 + list10 + list11
    return String
# ==================================Order Info===========================
#Entries
Redvelvettcake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Redvelvettcake_bg = canvas.create_image(456.0, 475.5, image = Redvelvettcake_img)
Redvelvettcake_txt = Entry(bd = 0 , textvariable=Redvelvettcake,bg = "#e3e3e3",highlightthickness = 0)
Redvelvettcake_txt.place(x = 356.0, y = 458, width = 200.0,height = 33)

Chocolatecake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Chocolatecake_bg = canvas.create_image(456.0, 432.5, image = Chocolatecake_img)
Chocolatecake_txt = Entry(bd = 0 , textvariable=Chocolatecake,bg = "#e3e3e3",highlightthickness = 0)
Chocolatecake_txt.place(x = 356.0, y = 415,width = 200.0,height = 33)

Strawberrycake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Strawberrycake_bg = canvas.create_image(456.0, 389.5,image = Strawberrycake_img)
Strawberrycake_txt = Entry(bd = 0 , textvariable=Strawberrycake,bg = "#e3e3e3",highlightthickness = 0)
Strawberrycake_txt.place(x = 356.0, y = 372,width = 200.0,height = 33)

Doughnut_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Doughnut_bg = canvas.create_image(456.0, 346.5,image = Doughnut_img)
Doughnut_txt = Entry(bd = 0 , textvariable=Doughnut,bg = "#e3e3e3",highlightthickness = 0)
Doughnut_txt.place(x = 356.0, y = 329,width = 200.0,height = 33)

Vanillacake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Vanillacake_bg = canvas.create_image(457.0, 303.5,image = Vanillacake_img)
Vanillacake_txt = Entry(bd = 0 , textvariable=Vanillacake,bg = "#e3e3e3",highlightthickness = 0)
Vanillacake_txt.place(x = 357.0, y = 286,width = 200.0,height = 33)

Pizza_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Pizza_bg = canvas.create_image(456.0, 260.5,image = Pizza_img)
Pizza_txt = Entry(bd = 0 , textvariable=Pizza,bg = "#e3e3e3",highlightthickness = 0)
Pizza_txt.place(x = 356.0, y = 243,width = 200.0,height = 33)

Burger_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
Burger_bg = canvas.create_image(456.0, 217.5,image = Burger_img)
Burger_txt = Entry(bd = 0 , textvariable=Burger,bg = "#e3e3e3",highlightthickness = 0)
Burger_txt.place(x = 356.0, y = 200,width = 200.0,height = 33)

PaymentRef_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
PaymentRef_bg = canvas.create_image(456.0, 174.5,image = PaymentRef_img)
PaymentRef_txt = Entry(bd = 0 , textvariable=PaymentRef,bg = "#e3e3e3",highlightthickness = 0)
PaymentRef_txt.place(x = 356.0, y = 157,width = 200.0,height = 33)

costRedvelvettcake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costRedvelvettcake_bg = canvas.create_image(1052.0, 475.5,image = Redvelvettcake_img)
costRedvelvettcake_txt = Entry(bd = 0 , textvariable=costRedvelvettcake,bg = "#e3e3e3",highlightthickness = 0)
costRedvelvettcake_txt.place(x = 952.0, y = 458,width = 200.0,height = 33)
             
costChocolatecake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costChocolatecake_bg = canvas.create_image(1052.0, 432.5,image = costChocolatecake_img)
costChocolatecake_txt = Entry(bd = 0 , textvariable=costChocolatecake,bg = "#e3e3e3",highlightthickness = 0)
costChocolatecake_txt.place(x = 952.0, y = 415,width = 200.0,height = 33)

costStrawberrycake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costStrawberrycake_bg = canvas.create_image(1052.0, 389.5,image = costStrawberrycake_img)
costStrawberrycake_txt = Entry(bd = 0 , textvariable=costStrawberrycake,bg = "#e3e3e3",highlightthickness = 0)
costStrawberrycake_txt.place(x = 952.0, y = 372,width = 200.0,height = 33)

costDoughnut_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costDoughnut_bg = canvas.create_image(1052.0, 346.5,image = costDoughnut_img)
costDoughnut_txt = Entry(bd = 0 , textvariable=costDoughnut,bg = "#e3e3e3",highlightthickness = 0)
costDoughnut_txt.place(x = 952.0, y = 329,width = 200.0,height = 33)

costVanillacake_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costVanillacake_bg = canvas.create_image(1053.0, 303.5,image = costVanillacake_img)
costVanillacake_txt = Entry(bd = 0 , textvariable=costVanillacake,bg = "#e3e3e3",highlightthickness = 0)
costVanillacake_txt.place(x = 953.0, y = 286,width = 200.0,height = 33)

costPizza_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costPizza_bg = canvas.create_image(1052.0, 260.5,image = costPizza_img)
costPizza_txt = Entry(bd = 0 , textvariable=costPizza,bg = "#e3e3e3",highlightthickness = 0)
costPizza_txt.place(x = 952.0, y = 243,width = 200.0,height = 33)

costBurger_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
costBurger_bg = canvas.create_image(1052.0, 217.5,image = costBurger_img)
costBurger_txt = Entry(bd = 0 , textvariable=costBurger,bg = "#e3e3e3",highlightthickness = 0)
costBurger_txt.place(x = 952.0, y = 200,width = 200.0,height = 33)

dateRef_img = PhotoImage(file = relative_to_assets("img_textBox0.png"))
dateRef_bg = canvas.create_image(1052.0, 174.5,image = dateRef_img)
dateRef_txt = Entry(bd = 0 , textvariable=dateRef,bg = "#e3e3e3",highlightthickness = 0)
dateRef_txt.place(x = 952.0, y = 157,width = 200.0,height = 33)

Vat_img = PhotoImage(file = relative_to_assets("img_textBox1.png"))
Vat_bg = canvas.create_image(459.0, 572.5,image = Vat_img)
Vat_txt = Entry(bd = 0 , textvariable=vat,bg = "#fbc778",highlightthickness = 0)
Vat_txt.place(x = 356.0, y = 555,width = 206.0,height = 33)

Total_img = PhotoImage(file = relative_to_assets("img_textBox1.png"))
Total_bg = canvas.create_image(459.0, 614.5,image = Total_img)
Total_txt = Entry(bd = 0 , textvariable=totalPrice,bg = "#fbc778",highlightthickness = 0)
Total_txt.place(x = 356.0, y = 597,width = 206.0,height = 33)

emailID_img = PhotoImage(file = relative_to_assets("img_textBox2.png"))
emailID_bg = canvas.create_image(853.0, 572.5,image = emailID_img)
emailID_txt = Entry(bd = 0 , textvariable=emailID,bg = "#ffffff",highlightthickness = 0)
emailID_txt.place(x = 783.0, y = 555,width = 140.0,height = 33)
#Buttons
img0 = PhotoImage(file = relative_to_assets("img0.png"))
b0 = Button(image = img0,borderwidth = 0,highlightthickness = 0,command = tPrice,relief = "flat")
b0.place(x = 616, y = 551,width = 153,height = 41)

img1 = PhotoImage(file = relative_to_assets("img1.png"))
b1 = Button(image = img1,borderwidth = 0,highlightthickness = 0,command = create_bill,relief = "flat")
b1.place(x = 615, y = 594,width = 153,height = 41)

img2 = PhotoImage(file = relative_to_assets("img2.png"))
b2 = Button(image = img2,borderwidth = 0,highlightthickness = 0,command = send_bill,relief = "flat")
b2.place(x = 776, y = 592,width = 153,height = 41)

img3 = PhotoImage(file = relative_to_assets("img3.png"))
b3 = Button(image = img3,borderwidth = 0,highlightthickness = 0,command = iExit,relief = "flat")
b3.place(x = 939, y = 594,width = 153,height = 41)

img4 = PhotoImage(file = relative_to_assets("img4.png"))
b4 = Button(image = img4,borderwidth = 0,highlightthickness = 0,command = reset,relief = "flat")
b4.place(x = 937, y = 551,width = 153,height = 41)
# ==================================Database===========================
tablename='Day_'+str(dateRef.get()).replace('/','_')
def Database():
    global connectn, cursor
    connectn = mysql.connector.connect(host="localhost", user="root", passwd="12345678", database="cafe",port=3306)
    cursor = connectn.cursor()
    # creating bill table
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {tablename}(Id int NOT NULL AUTO_INCREMENT PRIMARY KEY,Item VARCHAR(20) NOT NULL UNIQUE,Rate int,Qnty int DEFAULT 0,Total int DEFAULT 0);")
    for item in items:
        exec(f"rate=int(cost{item}.get())",globals())
        cursor.execute(f"INSERT IGNORE INTO {tablename}(Item,Rate) VALUES('{item}',{rate});")
def updatedb():
    Database()
    i=1
    for item in items:
        exec(f"rate=int(cost{item}.get())",globals())
        exec(f"qnty=int({item}.get())",globals())
        price=rate*qnty
        cursor.execute(f"UPDATE {tablename} SET Qnty=Qnty+{qnty} WHERE Id={i}")
        cursor.execute(f"UPDATE {tablename} SET Total=Total+{price} WHERE Id={i}")
        i+=1
    connectn.commit()
    cursor.close()
    connectn.close()
window.resizable(False, False)
window.mainloop()
