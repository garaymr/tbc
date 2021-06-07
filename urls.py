from django.urls import path
from .views import *

app_name = 'TBC'
urlpatterns = [
   #Comienzan urls de la primera versión

   path('', homePage, name='homepageTBC'),
   path('consulta-alumnos',consultaAlumnos, name="consultaAlumnos"),
   path('historial-academico',historialAcademico,name='historialAcademico'),
   path('pase-lista', paseLista, name="paseLista"),
   path('consulta-docentes', consultaDocentes, name="consultaDocentes"),
   path('actividades-aprendizaje', actividadesAprendizaje, name="actividadesAprendizaje"),
   path('nueva-actividad', nuevaActividad, name="nuevaActividad"),
   path('actividad-docente/<int:id>', actividadD, name="actividadD"),
   path('listas',ListasAsistencias,name="saveList"),
   path('delete-docente/<int:id>', delete_docente, name='delete_docente'),
   path('delete-alumno/<int:id>', delete_alumno, name='delete_alumno'),
   path('delete-archivo/<idAct>/<tipo>/<name>', delete_archivo, name='delete_archivo'),
   path('delete-actividad/<int:id>', delete_actividad, name='delete_actividad'),
   path('revisar-actividad/<id>/<idAlumno>', revisarActividad, name="revisarActividad"),
   path('actividad-alumno/<int:id>', actividadAlumno, name="actividadAlumno"),
   path('Modulos/nuevo',nuevoModulo, name="nuevoModulo"),
   path('Modulos/nuevo/guardar',nuevoModuloInsertar, name="nuevoModuloInsertar"),
   path('entrega-alumno/<int:id>/<int:idAlumno>', entregaAlumno , name='entregaAlumno'),
   path('Modulos/nuevo/unidad/guardar',nuevaUnidad,name='nuevaUnidad'),
   path('Modulos/nuevo/apes/guardar',nuevoApes,name='nuevoApes'),
   path('Modulos/get/APES/<int:idNombre>',getAPES,name='getAPES'),
   path('Modulos/get/Unidades',getUnidades,name='getUnidades'),
   path('Modulos/delete/unidad/<int:idNombre>',deleteUnidad,name='deleteUnidad'),
   path('Modulos/update/unidad',updateUnidad,name='updateUnidad'),
   path('Modulos/delete/APES',deleteAPES,name='deleteAPES'),
   path('Modulos/update/APES',updateAPES,name='updateAPES'),
   path('Modulos/update/propositoUnidad',updPropUnidad,name='updPropUnidad'),
   path('Modulos/update/archivo',updArchivo,name='updArchivo'),
   path('Modulos/update/getpropositoUnidad',getPropUnidad,name='getPropUnidad'),
   path('relacionar-modulo', relacionarModulo, name="relacionarModulo"),
   path('material-aprendizaje/<slug:id>', catalogo_material_didactico, name="catalogo_material_didactico"),
   #Comienzan urls de prueba TODO: Eliminar al final
   path('material-didactico', materialDidactico, name="materialDidactico"),
   path('estadistica', estadistica, name="estadistica"),
   #Fin de urls de prueba
   #Fin de las urls de la primera versión

   #Comienzan urls de la segunda versión
   path('generar-certificado', generarCertificado, name="generarCertificado"),
   path('alumno/<int:id>', alumno, name="alumno"),
   path('subir-estadistica', subirEstadistica, name="subirEstadistica"),
   #Fin de las urls de la segunda versión
   
]