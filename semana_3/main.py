# Taller Semana 3 >>> Type Aliasing - Try/Except - Refactorización usando Funciones
# Doris Mosquera Lozano - doris.mosquera@sofka.com.co
# DMosqueraLSofka

# Importaciones
import hashlib  # Libreria para el manejo de usuarios y contraseñas almacenadas
import getpass  # Libería para ocultar los caracteres de la contraseña ingresada por consola
from datetime import date, datetime  # Librería para el manejo de fechas y horas

# AUDITORÍA TS3 - Type Aliasing
# El type aliasing permite asignar nombres semánticos a estructuras de datos complejas,
# mejorando la legibilidad y mantenibilidad del código.
# La "MemoriaAgente" permite que el sistema recuerde comandos y contexto,
# mientras que "Recuerdo" es cada huella del usuario.
# "Credenciales" almacena el usuario y la contraseña del usuario.
# En lugar de escribir List[Dict[str, str]] en cada función, usamos los type definidos,
# lo que hace el código más legible, más fácil de mantener y más fácil de escalar.

# Representa un evento individual dentro del historial
type Recuerdo = dict[str, str]
# Representa la memoria completa del agente, una lista de recuerdos
type MemoriaAgente = list[Recuerdo]
# Representa las credenciales del usuario
type Credenciales = dict[str, str]


# Funciones
def ingresar_numero(num: str) -> float:
    # AUDITORÍA TS3 - Docstrings
    """
    Le solicita al usuario un número válido por consola.

    Muestra el mensaje num como prompt y repite la solicitud
    hasta que el usuario ingrese un valor numérico válido.
    Acepta comas como separador decimal (ej: '7,9' → 7.9).

    Args:
        num (str): Mensaje/prompt que se mostrará al usuario.

    Returns:
        float: El número ingresado por el usuario convertido a flotante.

    Raises:
        ValueError: Se captura internamente si el valor no es numérico;
                    se notifica al usuario y se vuelve a solicitar el dato.
    """
    while True:
        try:
            return float(input(num).replace(",", "."))
        except ValueError:
            print("❌ El número ingresado no es válido. Intenta de nuevo\n")


def calculadora(rol: str, historial_chat: MemoriaAgente) -> None:
    # AUDITORÍA TS3 - Docstrings
    """
    Ejecuta la calculadora para el usuario logeado.

    Muestra un menú con las operaciones disponibles (suma, resta,
    multiplicación y división) y le solicita al usuario dos números
    para realizar el cálculo seleccionado. Cada acción queda registrada en el
    historial del chat. El bucle continúa hasta que el usuario
    elija la opción de salir (5).

    La división por cero está controlada: si el divisor es 0,
    se informa al usuario y se registra el intento sin resultado.

    Args:
        rol (str): Rol del usuario autenticado ('admin' o 'invitado').
                   Se usa para personalizar los mensajes del historial.
        historial_chat (MemoriaAgente): Lista de registros donde se añade
                                    un diccionario por cada acción
                                    realizada dentro de la calculadora.

    Returns:
        None: La función no retorna ningún valor; su efecto es mostrar
              resultados por consola y guardar en la MemoriaAgente.
    """
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

        match opcion:
            case "1":
                num1 = ingresar_numero(f"\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = float(num1 + num2)
                print("---------------------------------------------------------")
                print(f"Resultado: {num1} + {num2} = {resultado} 📌")
                print("---------------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una suma"
            case "2":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = num1 - num2
                print("---------------------------------------------------------")
                print(f"Resultado: {num1} - {num2} = {resultado} 📌")
                print("---------------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una resta"
            case "3":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                resultado = num1 * num2
                print("---------------------------------------------------------")
                print(f"Resultado: {num1} × {num2} = {resultado} 📌")
                print("---------------------------------------------------------")
                mensaje = f"{rol.capitalize()} hizo una multiplicación"
            case "4":
                num1 = ingresar_numero("\n🔢  Primer número: ")
                num2 = ingresar_numero("🔢  Segundo número: ")
                print("---------------------------------------------------------")
                # AUDITORÍA TS3 - try/except:
                # Se intenta la operación directamente y se captura el error si ocurre, en lugar de verificar la condición antes.
                try:
                    resultado = num1 / num2
                    print(f"Resultado: {num1} ÷ {num2} = {resultado} 📌")
                    print("---------------------------------------------------------")
                    mensaje = f"{rol.capitalize()} hizo una división"
                except ZeroDivisionError:
                    # Control de la división por cero.
                    print("❌ ¡Upppppssss! No está permitida la división por cero.")
                    print("---------------------------------------------------------")
                    mensaje = f"{rol.capitalize()} intentó hacer una división por cero."
            case "5":
                print("\n😁  Gracias por usar nuesta calculadora 😁\n")
                mensaje = f"{rol.capitalize()} salió de la calculadora."
                calculadora_activa = False
            case _:
                print("\n⚠️ Opción inválida. Seleccione una opción")
                mensaje = (
                    f"{rol.capitalize()} ingresó una opción inválida en la calculadora."
                )
        registrar_accion(historial_chat, "calculadora", rol, mensaje)


# AUDITORÍA TS3 - Refactorización del código => Funciones
def login(usuarios: Credenciales) -> tuple[bool, str, str]:
    # AUDITORÍA TS3 - Docstrings
    """
    Gestiona el proceso de autenticación del usuario.

    Muestra el mensaje de bienvenida y solicita las credenciales al usuario.
    Permite un máximo de 3 intentos antes de bloquear el acceso.
    La contraseña se compara usando su hash SHA-256.

    Args:
        usuarios (Credenciales): Diccionario con usuarios y sus contraseñas
                                 ya hasheadas en SHA-256.

    Returns:
        tuple[bool, str, str]: Una tupla con:
            - bool: True si el login fue exitoso, False si fue bloqueado.
            - str:  El nombre del usuario que inició sesión (vacío si falló).
            - str:  El rol asignado: 'admin' o 'invitado' (vacío si falló).
    """
    login_exitoso = False
    usuario_actual = ""
    rol = ""
    intento = 0
    max_intentos = 3

    print("""
      \n..::Bienvenid@ a tu PythonAgente::..\n
      Iniciemos sesión. 😎\n
    ----------------------------------------------------------------------------------------------------------------------------
    🚨 Ten presente que sólo cuentas con 3 intentos de inicio de sesión. Superado estos intentos, tu usuario será bloqueado. 🚨
    ----------------------------------------------------------------------------------------------------------------------------
    """)

    while intento < max_intentos and not login_exitoso:
        print("\n========================")
        usuario = input("\n👤  Usuario: ").lower()

        password = getpass.getpass(" ░  Contraseña: ")
        hash_password_ingresada = hashlib.sha256(password.encode()).hexdigest()
        rol = "admin" if usuario == "admin" else "invitado"

        if usuario in usuarios and hash_password_ingresada == usuarios[usuario]:
            print(f"\n🎉 ¡Acceso Concedido! 🎉 - Bienvenido/a {usuario.capitalize()}")
            login_exitoso = True
            usuario_actual = usuario
        else:
            intento += 1
            if intento < max_intentos:
                print(
                    f"\n❌ Datos incorrectos. Te quedan {max_intentos - intento} intento(s) para iniciar de sesión."
                )
            else:
                print(
                    "\n❌ ¡Acceso Denegado!. Superaste la cantidad máxima de intentos.\n"
                )

    return login_exitoso, usuario_actual, rol


def contar(palabra: str, rol: str) -> str:
    # AUDITORÍA TS3 - Docstrings
    """
    Gestiona el conteo de vocales, consonantes y letras de una palabra.

    Args:
        palabra (str): La palabra a analizar.
        rol (str): El rol del usuario que realiza la acción.

    Returns:
        str: Mensaje descriptivo del resultado del conteo.
    """

    validando_palabra = palabra.isalpha()

    if validando_palabra:
        vocales = [l for l in palabra if l in "aeiouáéíóú"]
        consonantes = [l for l in palabra if l not in "aeiouáéíóú"]

        tot_vocales = len(vocales)
        tot_cons = len(consonantes)
        tot_letras = len(palabra)

        print(f"\n\t✍️  Palabra ingresada: {palabra}")
        print(f"\n\t✏️  Total de vocales: {tot_vocales}")
        print(f"\t✏️  Total de consonantes: {tot_cons}")
        print(f"\t✏️  Total de letras: {tot_letras}\n")
        mensaje = f"{rol.capitalize()} ingresó la palabra {palabra} y obtuvo como resultado: {tot_vocales} vocales | {tot_cons} consonantes | {tot_letras} letras en total."
    else:
        print("\n🙅 La palabra ingresada no es válida\n")
        mensaje = f"{rol.capitalize()} ingresó una palabra no válida >>> {palabra}"

    return mensaje


def validar_pass(pass_nueva: str, rol: str) -> str:
    # AUDITORÍA TS3 - Docstrings
    """
    Gestiona la validación de una contraseña nueva.

    Args:
        pass_nueva (str): La contraseña nueva a validar.
        rol (str): El rol del usuario que realiza la acción.

    Returns:
        str: Mensaje descriptivo con el resultado de la validación de la contraseña.
    """
    no_permitido = usuario_actual
    no_usar = no_permitido in pass_nueva

    if len(pass_nueva) < 8:
        print("\n📢 La contraseña debe ser al menos de 8 caracteres.\n")
        mensaje = f"{rol.capitalize()} ingresó una opción de contraseña no válida."
    elif no_usar or pass_nueva == no_permitido:
        print(
            "\n📢 La contraseña no debe contener o ser igual al usuario con que inicias sesión.\n"
        )
        mensaje = f"{rol.capitalize()} ingresó una opción de contraseña no válida."
    else:
        print("""\n👌 La contraseña que ingresaste cumple las condiciones establecidas:\n
              ✔️  Tiene al menos 8 carácteres.
              ✔️  No usa el usuario de inicio de sesión.\n""")
        mensaje = f"{rol.capitalize()} ingresó una opción de contraseña válida."

    return mensaje


def registrar_accion(
    historial_chat: MemoriaAgente, cmd: str, rol: str, descripcion: str
) -> None:
    # AUDITORÍA TS3 - Docstrings
    """
    Registra una acción en el historial del chat.

    Args:
        historial_chat (MemoriaAgente): Lista donde se añade el registro.
        cmd (str): Nombre del comando ejecutado.
        rol (str): Rol del usuario que realizó la acción.
        descripcion (str): Descripción detallada de la acción realizada.

    Returns:
        None
    """
    d_log: Recuerdo = {
        "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "cmd": cmd,
        "rol": rol,
        "descripcion": descripcion,
    }
    historial_chat.append(d_log)


def fecha_hoy(rol: str) -> str:
    # AUDITORÍA TS3 - Docstrings
    """
    Obtiene la fecha actual del sistema si el usuario tiene rol de administrador.

    Args:
        rol (str): El rol del usuario autenticado ('admin' o 'invitado').

    Returns:
        str: Mensaje descriptivo de la acción realizada exitosamente.

    Raises:
        PermissionError: Si el usuario no tiene rol de administrador.
    """
    if rol != "admin":
        # AUDITORÍA TS3 - raise:
        # Se lanza explícitamente una excepción usando raise. Al ejecutarse,
        # la función se detiene inmediatamente y el error se propaga hasta encontrar
        # un bloque except que lo maneje.
        # En este caso, la excepción se origina dentro de fecha_hoy y se
        # propaga hasta el try/except del menú principal (while sistema_activo),
        # donde es capturada por un except PermissionError.
        raise PermissionError(
            "Acceso Denegado. Este comando requiere privilegios de administrador."
        )

    hoy = date.today()
    print(f"\n🗓️  Hoy es: {hoy.strftime('%d %B %Y')}\n")
    return f"{rol.capitalize()} obtuvo la fecha de hoy: {hoy.strftime('%d %B %Y')}"


def gestionar_historial(
    accion: str, rol: str, memoria: MemoriaAgente
) -> tuple[str, str]:
    # AUDITORÍA TS3 - Docstrings
    """
    Gestiona las acciones del historial del chat. Función Pura (sin prints).

    Interpreta el subcomando recibido a través de accion y devuelve los strings resultantes:
    - 'all'   → muestra todos los registros de la sesión.
    - 'clear' → asume que la confirmación ya pasó en el Menú y limpia la memoria.
    - <palabra> → busca por palabra clave y filtra coincidencias.

    Args:
        accion (str): Acción a realizar ('all', 'clear', o la palabra clave).
        rol (str): Rol del usuario que ejecuta la acción.
        memoria (MemoriaAgente): Lista de recuerdos del agente.

    Returns:
        tuple[str, str]: Una tupla con (texto_pantalla_a_imprimir, mensaje_para_historial).
    """
    texto_pantalla = ""
    texto_log = ""

    if accion == "all":
        if len(memoria) == 0:
            texto_pantalla = (
                "\n➤  Por el momento no tienes registros en tu historial.\n"
            )
            texto_log = f"{rol.capitalize()} consultó todo su historial y este no tenía registro."
        else:
            lineas = [
                f"\n📋 Historial del Chat Usuario {rol}. \n📊 Total de acciones realizadas en la sesión: {len(memoria)} \n🧾 Detalle Historial: \n"
            ]
            for recuerdo in memoria:
                lineas.append(f"✅ {recuerdo}")
            lineas.append("\n")
            texto_pantalla = "\n".join(lineas)
            texto_log = f"{rol.capitalize()} consultó todo su historial del chat y se cargó en pantalla."

    elif accion == "clear":
        memoria.clear()
        texto_pantalla = "\n🗑️  Se eliminó todo el historial del chat.\n"
        texto_log = f"{rol.capitalize()} eliminó todo su historial del chat."

    else:
        palabra_clave = accion.lower()
        coincidencias = []
        for recuerdo in memoria:
            if (
                recuerdo.get("descripcion")
                and palabra_clave in str(recuerdo["descripcion"]).lower()
            ):
                coincidencias.append(recuerdo)

        if len(coincidencias) > 0:
            lineas = [f"\n✅ Total de coincidencias: {len(coincidencias)}\n"]
            for coincidencia in coincidencias:
                lineas.append(f"➤ {coincidencia}")
            lineas.append("\n")
            texto_pantalla = "\n".join(lineas)
        else:
            texto_pantalla = "\n📋 Total de coincidencias: 0. \n❌ No encontré registros que coincidan con esa palabra.\n"

        texto_log = f"{rol.capitalize()} realizó una búsqueda en el historial con la palabra clave: '{palabra_clave}'"

    return texto_pantalla, texto_log


# Usuarios y contraseñas
usuarios: Credenciales = {"admin": "1234", "user": "abcd", "ejecutivo": "4321"}

for u in usuarios:
    usuarios[u] = hashlib.sha256(usuarios[u].encode()).hexdigest()

# Fase 1: Capa de Seguridad (Login)
login_exitoso, usuario_actual, rol = login(usuarios)

if not login_exitoso:
    print("🚫 Usuario bloqueado 🚫 Cerrando sistema.\n")
else:
    print("\n========================\n")
    print(f"🤗  {rol.capitalize()}, ¿Qué deseas hacer hoy?\n")

    # Fase 2: Comandos Base
    ## PythonAgente
    cmd = ""
    sistema_activo = True
    historial_chat: MemoriaAgente = []
    mensaje = ""

    while sistema_activo:
        cmd = input(f"{usuario_actual.capitalize()}@Comando>: ").strip().lower()
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
            mensaje = contar(palabra, rol)

        # Fase 3: Nuevas Herramientas
        ## Casting y Lógica Múltiple
        elif cmd == "calculadora":
            calculadora(rol, historial_chat)
            continue

        ## Control de Acceso
        elif cmd == "fecha_hoy":
            try:
                mensaje = fecha_hoy(rol)
            except PermissionError as e:
                print(f"\n⛔ {e} ⛔\n")
                mensaje = f"Comando denegado. {rol.capitalize()} no tiene privilegios de administrador."

        ## Manipulación de Strings
        elif cmd == "validar_pass":
            pass_nueva = input("\nIngrese la contraseña nueva validar: ").strip()
            mensaje = validar_pass(pass_nueva, rol)

        # Historial y Búsqueda en el Chat >>> Taller Semana 2
        elif cmd.startswith("historial"):
            partes = cmd.split()
            accion = partes[1] if len(partes) > 1 else ""

            if accion == "clear":
                respuesta = (
                    input(
                        f"\n⚠️  ¿Está seguro {rol.upper()} de querer borrar el historial? SI[S] NO[N]: "
                    )
                    .strip()
                    .upper()
                )
                if respuesta == "S":
                    texto_pantalla, mensaje = gestionar_historial(
                        "clear", rol, historial_chat
                    )
                    print(texto_pantalla)
                else:
                    print("\nNo se eliminó el historial del chat.\n")
                    mensaje = f"{rol.capitalize()} no eliminó el historial del chat."
            elif accion == "all":
                texto_pantalla, mensaje = gestionar_historial(
                    "all", rol, historial_chat
                )
                print(texto_pantalla)
            else:
                palabra_clave = input("\nIngresa la palabra clave a buscar: ").strip()
                texto_pantalla, mensaje = gestionar_historial(
                    palabra_clave, rol, historial_chat
                )
                print(texto_pantalla)
        else:
            print("\n🤷 Comando desconocido, intente de nuevo.\n")
            mensaje = f"{rol.capitalize()} ingresó un comando desconocido."

        # El bucle principal se encarga de registrar en el historial del chat. A excepción de calculadora y gestionar_historial que lo realizan internamente
        registrar_accion(historial_chat, cmd, rol, mensaje)
