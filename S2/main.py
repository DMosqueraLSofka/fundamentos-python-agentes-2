#Taller Semana 2 >>> Historial de Chat y Búsqueda
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# Importaciones
import hashlib # Libreria para el manejo de usuarios y contraseñas almacenadas
import getpass # Libería para ocultar los caracteres de la contraseña ingresada por consola
from datetime import date, datetime # Librería para el manejo de fechas y horas


# Funciones
## Función para solicitar  al usuario números para el comando calculadora, controlando el error que si el usuario ingresa letras y/o caracteres especiales, le indique que ingrese un número váldido
def ingresar_numero(num: str) -> float:
    while True:
        try:
            # AUDITORÍA TS1 - Uso de float() vs int():
            # 1. Se usa float() en lugar de int() porque la calculadora requiere soportar números 
            #    con decimales. Al dividir, el resultado suele ser decimal, y limitarlo a int() 
            #    sería un error matemático en muchos cálculos de una calculadora.
            # 2. Se aplica el casting (conversión): Porque la función input() 
            #    automáticamente captura todo como un tipo texto (str) y no realizaría las operaciones
            #    matemáticas con texto y el sistema lanzaría error.
            # 3. El usuario podrá ingresar números con comas (ej: 7,9) indicando que es un número decimal (7.9) y el sistema reemplazará la coma por un punto (método replace)
            return float(input(num).replace(",", "."))
        except ValueError: ## Con la ayuda de IA se implenta el control de errores, cuando el usuario no proporcione un número válido
            print("❌ El número ingresado no es válido. Intenta de nuevo\n")


## Función para ejecutar la calculadora, cuando el comando cmd sea igual a calculador
def calculadora(rol, historial_chat):
    calculadora_activa = True
    mensaje = ""

    while calculadora_activa:
        print("\n\t...::Menú de operaciones::...")
        print("\t\t1. ➕ Suma")
        print("\t\t2. ➖ Resta")
        print("\t\t3. ✖️  Multiplicación")
        print("\t\t4. ➗ División")
        print("\t\t5. 🏁 Salir")

        opcion = input("\nSelecciona una opción (1-5): ")        

        match opcion: ##Se implementa el match/case para las distintas opciones de la calculadora.
            case "1":
                num1 = ingresar_numero(f"\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = float(num1 + num2)
                print("---------------------------------------------------")
                print(f"Resultado: {num1} + {num2} = {resultado} 📌")
                print("---------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una suma"
            case "2":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = num1 - num2
                print("---------------------------------------------------")
                print(f"Resultado: {num1} - {num2} = {resultado} 📌")
                print("---------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una resta"
            case "3":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = num1 * num2
                print("---------------------------------------------------")
                print(f"Resultado: {num1} × {num2} = {resultado} 📌")
                print("---------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una multiplicación"
            case "4":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("---------------------------------------------------")
                if num2 != 0:
                    resultado = num1 / num2
                    print(f"Resultado: {num1} ÷ {num2} = {resultado} 📌")
                    print("---------------------------------------------------")
                    mensaje = f"{rol.capitalize()} hizo una división"
                else:
                    # Control de la división por cero. Es una indeterminanción matemática 
                    # por lo que al presentarse no hay un resultado para dicha operación
                    print("❌ ¡Upppppssss! No está permitida la división por cero.")
                    print("---------------------------------------------------")
                    mensaje = f"{rol.capitalize()} intentó hacer una división por cero."
            case "5":
                print("\n😁  Gracias por usar nuesta calculadora 😁\n")
                mensaje = f"{rol.capitalize()} salió de la calculadora."
                calculadora_activa = False
            case _:
                print("\n⚠️ Opción inválida. Seleccione una opción")
                mensaje = f"{rol.capitalize()} ingresó una opción inválida en la calculadora."
        d_log = {"timestamp": datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                "cmd": "calculadora",
                "rol": rol,
                "descripcion": mensaje}
        historial_chat.append(d_log)


# Usuarios y contraseñas
usuarios = {"admin": "1234", "user": "abcd", "ejecutivo": "4321"}

# Hash de contraseñas --- Con la ayuda de la IA se implementa el hash para hacer más profesional el código
for u in usuarios:
    usuarios[u] = hashlib.sha256(usuarios[u].encode()).hexdigest()

login_exitoso = False
usuario_actual = ""
intento = 0
max_intentos = 3

# Fase 1: Capa de Seguridad (Login)
print("""
      \n..::Bienvenid@ a tu PythonAgente::..\n
      Iniciemos sesión. 😎\n
    ---------------------------------------------------------------------------------------------------------------------------- 
    🚨 Ten presente que sólo cuentas con 3 intentos de inicio de sesión. Superado estos intentos, tu usuario será bloqueado. 🚨
    ----------------------------------------------------------------------------------------------------------------------------
    """)
# AUDITORÍA TS1 - Lógica del contador de 3 intentos:
# 1. Variables base: Iniciamos `intento = 0` y el límite de oportunidades `max_intentos = 3`.
# 2. Condición del ciclo: El bucle `while` se mantendrá activo siempre y cuando 
#    los intentos actuales sean menores que 3 (`intento < max_intentos`) Y 
#    el estado del login aún no sea exitoso (`not login_exitoso`).
# 3. Flujo Verdadero (Éxito): Si las credenciales hacen match, la bandera `login_exitoso` 
#    pasa a True, lo que rompe automáticamente la segunda condición del ciclo.
# 4. Flujo Falso (Falla): Si no coinciden, entra al `else` y aumentamos los intentos (`intento += 1`). 
#    Luego verificamos si aún quedan intentos (`intento < max_intentos`). De ser así, mostramos 
#    las oportunidades restantes (3 - intento).
# 5. Bloqueo (Fin de Intentos): Si `intento` llega a 3, el `while` termina. Como 
#    `login_exitoso` sigue siendo False, el sistema pasa al bloque final (`if not login_exitoso:`) 
#    donde bloquea el acceso.
while intento < max_intentos and not login_exitoso:
    print("\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*")
    usuario = input("\n👤  Usuario: ").lower()
    ## Usando la librería getpass, permite que el usuario mientras escribe la contraseña esta se oculte (no muestra los carácteres de la contraseña en pantalla)
    password = getpass.getpass(" ░  Contraseña: ")
    hash_password_ingresada = hashlib.sha256(password.encode()).hexdigest()
    rol = "admin" if usuario == "admin" else "invitado"

    if usuario in usuarios and hash_password_ingresada == usuarios[usuario]:
        print(f"\n🎉 ¡Acceso Concedido! 🎉 - Bienvenido/a {usuario.capitalize()}")
        login_exitoso = True        
    else:
        intento += 1
        if intento < max_intentos:
            print(
                f"\n❌ Datos incorrectos. Te quedan {max_intentos - intento} intento(s) para iniciar de sesión."
            )
        else:
            print("\n❌ ¡Acceso Denegado!. Superaste la cantidad máxima de intentos.\n")

if not login_exitoso:
    print("🚫 Usuario bloqueado 🚫 Cerrando sistema.\n")
else:
    print("\n=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*\n")
    print(f"🤗  {rol.capitalize()}, ¿Qué deseas hacer hoy?\n")
    usuario_actual = usuario

    # Fase 2: Comandos Base

    cmd = ""
    sistema_activo = True
    historial_chat = []
    mensaje = ""

    while sistema_activo:
        cmd = input("Comando>: ").strip().lower()
        mensaje = ""
        
        ## Salir del sistema
        if cmd == "salir":
            print("\n💖  Gracias por usar nuesto PythonAgente 💖 \n")
            sistema_activo = False
            mensaje = f"{rol.capitalize()} finalizó la sesión."

        ## El sistema responde pong si recibe del usuario el comando ping
        elif cmd == "ping":
            print("\n¡pong!\n")
            mensaje = f" {rol.capitalize()} envió ping, el sistema respondió pong."

        ## Contar la cantidad de vocales, consonantes y letras que contiene una palabra ingresada por el usuario
        elif cmd == "contar":
            palabra = input("\nIngrese una palabra: ").strip().lower()
            ## Usando el método isalpha(), el sistema valida que la palabra ingresada por el usuario corresponde a los carácteres del alfabeto
            validando_palabra = palabra.isalpha()
            tot_letras = len(palabra)

            if (validando_palabra):
                # Conteo
                tot_vocales = 0
                tot_cons = 0
                for p in palabra:
                    if p in "aeiou":
                        tot_vocales += 1
                    else:
                        tot_cons += 1
                # Resultados del conteo
                print(f"\n\t✍️  Palabra ingresada: {palabra}")
                print(f"\n\t✏️  Total de vocales: {tot_vocales}")
                print(f"\t✏️  Total de consonantes: {tot_cons}")
                print(f"\t✏️  Total de letras: {tot_letras}\n")
                mensaje = f"{rol.capitalize()} ingresó la palabra {palabra} y obtuvo como resultado: {tot_vocales} vocales | {tot_cons} consonantes | {tot_letras} letras en total."
            else:
                print("\n🙅 La palabra ingresada no es válida\n")
                mensaje = f"{rol.capitalize()} ingresó una palabra no válida >>> {palabra}"          

        # Fase 3: Nuevas Herramientas

        ## Casting y Lógica Múltiple
        elif cmd == "calculadora":
            calculadora(rol, historial_chat)
            continue

        ## Control de Acceso
        elif cmd == "fecha_hoy":
            if rol == "admin":
                hoy = date.today()
                print(f"\n🗓️  Hoy es: {hoy.strftime('%d %B %Y')}\n")
                mensaje = f"{rol.capitalize()} obtuvo la fecha de hoy: {hoy.strftime('%d %B %Y')}"
            else:
                print(
                    "\n⛔ Acceso Denegado. Este comando requiere privilegios de administrador. ⛔\n"
                )
                mensaje = f"Comando denegado. {rol.capitalize()} no tiene privilegios de administrador."

        ## Manipulación de Strings
        elif cmd == "validar_pass":
            pass_nueva = input("\nIngrese la contraseña nueva validar: ").strip()
            no_permitido = usuario_actual
            no_usar = no_permitido in pass_nueva

            if (len(pass_nueva) < 8):
                print("\n📢 La contraseña debe ser al menos de 8 caracteres.\n")
                mensaje = f"{rol.capitalize()} ingresó una opción de contraseña no válida."
            elif (no_usar or pass_nueva == no_permitido):
                print("\n📢 La contraseña no debe contener o ser igual al usuario con que inicias sesión.\n")
                mensaje = f"{rol.capitalize()} ingresó una opción de contraseña no válida."
            else:
                print("""\n👌 La contraseña que ingresaste cumple las condiciones establecidas:\n
                      ✔️  Tiene al menos 8 carácteres.
                      ✔️  No usa el usuario de inicio de sesión.\n""")
                mensaje = f"{rol.capitalize()} ingresó una opción de contraseña válida."

        # Historial y Búsqueda en el Chat >>> Taller Semana 2
        elif cmd.startswith("historial"):
            # Se divide el comando introducido por el usuario para atrapar las distintas opciones:
            #   - "historial all" 
            #   - "historial clear"
            #   - "historial para buscar por palabra clave"
            partes = cmd.split()
            accion = partes[1] if len(partes) > 1 else ""

            if accion == "all":
                if (len(historial_chat) == 0):
                    print("\nPor el momento no tienes registros en tu historial.\n")
                    mensaje = f"{rol.capitalize()} consultó todo su historial y este no tenía registro"
                else:
                    print(f"\n📋 Historial del Chat Usuario {rol}. \n📊 Total de acciones realizadas en la sesión: {len(historial_chat)} \n🧾 Detalle Historial: \n")
                    for registro in historial_chat:
                        print(f"✅ {registro}")
                    mensaje = f"{rol.capitalize()} consultó todo su historial del chat."
                    print("\n")
            elif accion == "clear":
                respuesta = input(f"\n⚠️  ¿Está seguro {rol.upper()} de eliminar el historial del chat? SI[S] NO[N]: ").strip().upper()
                if (respuesta == "S"):
                    historial_chat.clear()                    
                    print("\n🗑️  Se eliminó todo el historial del chat.\n")
                    mensaje = f"{rol.capitalize()} eliminó todo su historial del chat."
                else:
                    print("\nNo se eliminó el historial del chat.\n")
                    mensaje = f"{rol.capitalize()} no eliminó el historial del chat."
            elif accion == "":
                palabra_clave = input("\nIngresa la palabra clave a buscar: ").strip().lower()
                coincidencias = []
                for registro in historial_chat:
                    # AUDITORÍA TS2:
                    # 1. Para saber si una palabra estaba "dentro" de otra, se usó el operador 'in' propio de Python, 
                    #    el cual revisa si la subcadena (palabra_clave) pertenece a la cadena mayor (descripción).
                    # 2. El reto de las singularidades se resolvió aplicando el método .split() al comando de 
                    #    entrada principal ("cmd"). Así, si el usuario escribe "historial all", se convierte en 
                    #    la lista ["historial", "all"] - ["historial", "clear"] - ["historial"], permitiendo al sistema validar la posición 1 para saber la acción.
                    # 3. La insensibilidad a mayúsculas/minúsculas se logró usando .lower() tanto en el input como en la descripción.
                    # 4. Se agregó el método .get() para obtener el valor de la clave 'descripcion' del diccionario.
                    # 5. Se agregó el casting a string str() para asegurar que el valor de la clave 'descripcion' sea una cadena de texto.
                    if registro.get('descripcion') and palabra_clave in str(registro['descripcion']).lower():
                        coincidencias.append(registro)

                if len(coincidencias) > 0:
                    print(f"\n✅ Total de coincidencias: {len(coincidencias)}\n")
                    for coincidencia in coincidencias:
                            print(f"➤ {coincidencia}")
                    print("\n")
                else:
                    print("\n📋 Total de coincidencias: 0. \n❌ No encontré registros que coincidan con esa palabra.\n")
                
                mensaje = f"{rol.capitalize()} realizó una búsqueda en el historial con la palabra clave: '{palabra_clave}'"
            else:
                print("\n⚠️ Acción de historial desconocida.\n")
                mensaje = f"{rol.capitalize()} intentó una acción desconocida en el historial: {accion}"
        else:
            print("\n🤷 Comando desconocido, intente de nuevo.\n")
            mensaje = f"{rol.capitalize()} ingresó un comando desconocido."
        
        # Formato de cada registro que estará en el historial del chat        
        d_log = {"timestamp": datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol,
            "descripcion": mensaje}
        historial_chat.append(d_log)
