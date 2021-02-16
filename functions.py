
import csv
import smtplib

#Esta es una lista auxiliar que nos permitirá almacenar los contactos del csv
list_of_rows = list

#Este contador sirve para listar los ejemplos y realizar los reemplazos de palabras
c = 0

contactList = []

#Función de LogIn
def login(address, password):

    # Nos conectamos con el SMTP de gmail y nos logeamos
    global s
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(address, password)
    return True


#Función para crear una lista de contactos de un CSV UTF-8
def createContactsList(name):

    #Abrimos el archivo
    with open("static/files/" + name, encoding="utf-8-sig") as csvfile:
        #Determinamos que el delimitante es la ,
        csvreader = csv.reader(csvfile, delimiter=",")

        name = name[:-4]

        #Con la ayuda de nuestra lista auxiliar almacenamos la lista que obtenemos del CSV
        global list_of_rows
        list_of_rows = list(csvreader)

        exe = name + "= ["

        for count, row in enumerate(list_of_rows[1:]):
            c = 0
            exe += " { \"id\" : " + str(count) + ", "
            for col in row:
                exe += "\"" + list_of_rows[0][c] + "\" : \"" + col + "\", "
                c += 1
            exe = exe[:-2]
            exe += "},"
        exe = exe[:-1]
        exe += "]"

        exec(exe, globals())

        exec("contactList.append((name," + name + " ))")



#Función para mostrar los contactos registrados
def printContacts():
    #Solicitamos el nombre de la lista que se desea imprimir
    name = input("Ingrese el nombre de la lista de contactos que desea imprimir: ")
    #Mostramos la lista en base al nombre ingresado
    exec("for row in " + name +": print(\" \".join(row))")

#Función para enviar el email
def sendMail():
    #Solicitamos el nombre de la lista de contactos a la que queremos enviar
    name = input("Ingrese el nombre de la lista de contactos a la que desea enviar: ")

    print("Ahora procederemos a escribir el mensaje")

    #Solicitamos el asunto que se colocará en el correo
    asunto = input("Ingresa el asunto(Subject) del correo: ")

    global c
    c = 0

    #En base a la lista de contactos mostramos un ejemplo de qué columnas tiene que podrían colocarse en el mail
    exec("for element in " + name + """[0]:
        print(str(c) + ": " + element + " - Ejemplo: " +""" + name + """[1][c])
        c = c + 1""", globals())

    print("""
    Si deseas usar alguno de los parámetros mostrados anteriormente en el correo, 
    debes ingresarlo de la siguiente manera en el cuerpo del mensaje""")

    print("Ejemplo: Hola {0} {1} ")

    exec("print(f'En el ejemplo el mensaje para el primer contacto sería: Hola {" +
         name + "[1][0]} {" + name + "[1][1]}')", globals())

    print("Por favor, redacte su mensaje: ")

    #Ahora procedemos a leer el mensaje
    message = input("Mensaje: ")

    #Este auxiliar almacena el mensaje original escrito por el usuario
    aux = message

    #Ahora agregamos los parametros importantes del mensaje, lo personalizamos para cada usuario y lo enviamos.
    exec("for row in " + name + """[1:]:
        
        message = aux
        
        msg = MIMEMultipart()  # create a message
        # setup the parameters of the message
        msg['From'] = "EdCiTec"
        msg['To'] = row[2]
        msg['Subject'] = asunto
        
        c = 0
        for element in row:
            h = "{" + str(c) + "}"
            message = message.replace(h, element)
            c = c + 1
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg""")