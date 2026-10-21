ANDROMEDA 7.0 · GALAXY — APK GRATIS DESDE WINDOWS
=================================================

IMPORTANTE Y HONESTO
- La APK no se crea cambiando .py por .apk.
- El proyecto original de Windows usa tkinter/ttkbootstrap, que Android no soporta directamente.
- Este paquete es una primera adaptación móvil con Kivy. Conserva el estilo negro/azul, consultas a fuentes abiertas, chats e historial local.
- No es una conversión exacta de toda la lógica de escritorio: OCR de imágenes/documentos, configuración avanzada y algunas funciones del motor original aún deben portarse y probarse.
- La compilación corre en un servidor Ubuntu de GitHub Actions; NO necesitas instalar Linux en tu PC. Es gratuito dentro de los límites de GitHub Actions.

PASO 1 — Crear repositorio
1. Abre https://github.com y entra en tu cuenta.
2. Pulsa + (arriba) > New repository.
3. Nombre: andromeda-android
4. Elige Public (recomendado para que el flujo sea sencillo) y pulsa Create repository.
5. No agregues README, .gitignore ni licencia desde GitHub.

PASO 2 — Subir los archivos desde Windows
1. Extrae ANDROMEDA_ANDROID.zip.
2. Dentro verás main.py, buildozer.spec, requirements.txt y la carpeta .github.
3. En la página vacía de tu repositorio pulsa "uploading an existing file".
4. Arrastra TODOS los archivos y carpetas extraídos. IMPORTANTE: debe subirse la carpeta .github/workflows/build-android.yml; no la omitas.
5. Espera a que terminen de subir; escribe el mensaje "Primera compilación Android" y pulsa Commit changes.

PASO 3 — Iniciar/ver la compilación
1. Abre la pestaña Actions del repositorio.
2. Si aparece "I understand my workflows, go ahead and enable them", pulsa para habilitar workflows.
3. Selecciona "Build ANDROMEDA APK".
4. Pulsa "Run workflow" > botón verde "Run workflow".
5. Espera. La primera compilación puede tardar varios minutos. Abre el trabajo que esté ejecutándose para ver los registros.
6. Si falla, abre el paso rojo "Build APK", copia el final del registro (unas 30-50 líneas) y compártelo para corregirlo.

PASO 4 — Descargar la APK
1. Cuando el trabajo aparezca verde, abre la ejecución.
2. Baja a "Artifacts".
3. Descarga "ANDROMEDA-APK" (ZIP).
4. Extrae ese ZIP en Windows y encontrarás un archivo .apk.
5. Pásalo a tu teléfono Android. Abre el archivo y autoriza "Instalar apps desconocidas" si Android lo solicita. Instala.

SI NO APARECE "Run workflow"
- Confirma que el archivo está en .github/workflows/build-android.yml.
- Comprueba que el commit terminó y que estás en la pestaña Actions.
- También puedes hacer un cambio mínimo en README_PASO_A_PASO.txt y hacer Commit changes para activar la compilación por push.

SI LA COMPILACIÓN FALLA
No cambies versiones al azar. Copia el error completo del paso rojo. Las versiones de Android/SDK pueden cambiar y se ajustarán según el registro.

DATOS Y PRIVACIDAD
- La app usa conexión a Internet para consultar fuentes abiertas.
- Los chats/historial se guardan localmente en los datos privados de la app.
- Desinstalar la app normalmente elimina esos datos privados. Guarda una copia si necesitas conservarlos.
- Las fuentes abiertas no garantizan que todas las preguntas tengan respuesta. No hay un modelo generativo grande integrado ni API de IA de pago.
