from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import  Subquery
import json
from .models import * 
import sweetify
import xlwt
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.utils import formats
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from login.models import CustomUser, UsuarioInstitucion
import gspread
from oauth2client.service_account import ServiceAccountCredentials

global idDocente
global idAlumnoI

#Comienza sección de vistas de la primer versión

#Función para el control de material didáctico

def catalogo_material_didactico(request,id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))
	else:
		if request.user.tipo_usuario == '7':
			alumno_institucion = Alumno.objects.get(email=request.user.email)
			if alumno_institucion.cct != id:
				return redirect ('/TBC')
			else:
				return render(request, 'material_didactico.html')
		else:
			if request.user.tipo_usuario == '6':
				docente_institucion = Docente.objects.get(email=request.user.email)
				if docente_institucion.cct != id:
					return redirect('/TBC')
				else:
					return render(request, 'material_didactico.html')
			else:
				if request.user.tipo_usuario == '1':
					institucion = UsuarioInstitucion.objects.get(id_usuariobase=request.user.id)
					if 	institucion.cct != id:
						return redirect('/TBC')
					else:
						return render(request, 'material_didactico.html')

#Función para devolver la homePage

def homePage(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	try:
		Docentes = Docente.objects.filter(cct = usuarioLogueado.last_name)#TODO:Cambiar last_name 
		NotificacionesDocente = Notificacion_mod.objects.all()
		NotificacionesDocenteModulo = Notificacion_mod_docente.objects.filter(id_docente = idDocente)
	except:
		NotificacionesDocente = None
		NotificacionesDocenteModulo = None
		cctDocente = None
	Cursos = Curso.objects.all()
	Alumnos = Alumno.objects.all()
	AlumnosI = Alumno.objects.filter(cct = request.user.last_name)#TODO:Cambiar last_name 
	#TODO: Sacar con el request.user.email (o sea del docente), enlazarlo con Docente y sacar su cct para hacer la consulta de abajo
	try:
		field_name = 'cct'
		obj = Docente.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
		field_value = getattr(obj, field_name)
		cctDocente = field_value
	except:
		print('')
	AlumnosD = Alumno.objects.filter(cct = cctDocente)
	
	if request.user.tipo_usuario == "7":
		return redirect('/TBC/alumno/'+str(idAlumnoI))

	return render(request, 'homePage.html', {'usuario':usuarioLogueado, 'notificaciones': NotificacionesDocente, 'notificacion':NotificacionesDocenteModulo, 'docente':Docentes, 'curso':Cursos, 'alumno':Alumnos, 'alumnoI':AlumnosI, 'alumnoD':AlumnosD })

#Función para consultar los alumnos y hacer actualización de estos

def consultaAlumnos(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	Alumnos = Alumno.objects.filter(cct = request.user.last_name) #TODO:Cambiar cuando se actualice los campos a cct
	Usuarios = CustomUser.objects.all()
	Archivos = Archivo.objects.all()
	Modulos = Modulo.objects.all()
	Asignaturas = Asignatura.objects.all()
	indicesDocente = []
	Estadistica = Estadistica_modulo.objects.filter(cct = request.user.last_name).order_by('id_estadistica_modulo')
	#Se filtra la tabla de estadística para encontrar los registros correspondientes a la institución (request.user.last_name)
	try:
		if usuarioLogueado.tipo_usuario == '6':
			#Se saca el areaDocente del usuario conectado
			field_name = 'areadisciplinar_docente_id'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			areaDocente = field_value
			Estadistica_modulos = Estadistica_modulo.objects.filter(nombre_escuela = request.user.municipio).order_by('id_estadistica_modulo')
			ModulosDocente = Modulo.objects.filter(areadisciplinar_modulo_id = areaDocente)
			for m in ModulosDocente:
				indicesDocente.append(m.id_modulo)
		if usuarioLogueado.tipo_usuario == '1':
			ModulosDocente = None
			Estadistica_modulos = Estadistica_modulo.objects.filter(cct = request.user.last_name).order_by('id_estadistica_modulo')
	except:
		Estadistica_modulos = None

	#Se llama la función para generar los reportes declarando antes las variables a usar
	totalAlumnos = 0
	labels, data, labels2, data2, auxData3, auxLabels3, indices3 = [], [], [], [], [], [], []
	labels, data, labels2, data2, auxData3, auxLabels3, totalAlumnos, indices3, indicesDocente = generar_reporte(labels, data, labels2, data2, auxData3, auxLabels3, Estadistica_modulos, Modulos, totalAlumnos, indices3, indicesDocente)

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		idAlumno = request.POST['idAlumno']
		nombreAlumno = request.POST['nombreAlumno']
		email = request.POST['email']
		telFijo = request.POST['telFijo']
		telCelular = request.POST['telCelular']
		curp = request.POST['curp']
		numMatricula = request.POST['numMatricula']
		nombreEscuela = request.POST['nombreEscuela']
		cct = request.POST['cct']
		semestre = request.POST['semestre']
		contrasena = make_password(request.POST['contrasena'])
		tipo_secundaria = request.POST['tipo_secundaria']
		beca = request.POST['beca']
		subsistema = request.POST['subsistema_nombre']
		#Compara si el id está vacio para insertar nuevo reigstro
		if idAlumno == '':
			try:
				field_name = 'id_alumno'
				obj = Alumno.objects.last()
				field_value = getattr(obj, field_name)
				idAlumno = field_value + 1
			except:
				idAlumno = 1
			try:
				nuevoAlumno = Alumno(id_alumno = idAlumno, nombre_alumno = nombreAlumno, email = email, tel_fijo = telFijo, tel_celular = telCelular, curp_alumno = curp,
				num_matricula = numMatricula, nombre_escuela = nombreEscuela, cct = cct, semestre = semestre, tipo_secundaria = tipo_secundaria, beca = beca, subsistema_nombre = subsistema)
				nuevoAlumno.save()
				nuevoAlumnoUser = CustomUser(password = contrasena, username = email, last_name = nombreAlumno, email = email, curp_rfc = curp,
				municipio = nombreEscuela, celular = telCelular, tipo_usuario = 7, tipo_persona = 1, first_name = numMatricula)
				#Código para guardar los archivos [acta, curp, y certificado] en la carpeta TODO: Guardar en la tabla archivo tambien
				try:
					acta = request.FILES['acta']
					#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+acta.name #'/media/TBC/Datos/Alumnos/'+acta.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = acta.name, tipo_archivo = 'Acta nacimiento', url = url, id_alumno = idAlumno)
					nuevoArchivo.archivo = acta
					nuevoArchivo.save()
				except:
					print('')
				try:
					curp = request.FILES['curpArchivo']
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					url =  'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+curp.name #'/media/TBC/Datos/Alumnos/'+curp.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = curp.name, tipo_archivo = 'Curp', url = url, id_alumno = idAlumno)
					nuevoArchivo.archivo = curp
					nuevoArchivo.save()
				except:
					print('')
				try:
					certificado = request.FILES['certificado']
					#aqui guardar el registro en la tabla de archivos
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+certificado.name #'/media/TBC/Datos/Alumnos/'+certificado.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = certificado.name, tipo_archivo = 'Certificado secundaria', url = url, id_alumno = idAlumno)
					nuevoArchivo.archivo = certificado
					nuevoArchivo.save()
				except:
					print('')
				try:
					subsistema_archivo = request.FILES['subsistema']
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+subsistema_archivo.name #'/media/TBC/Datos/Alumnos/'+subsistema_archivo.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = subsistema_archivo.name, tipo_archivo = 'Subsistema', url = url, id_alumno = idAlumno)
					nuevoArchivo.archivo = subsistema_archivo
					nuevoArchivo.save()
				except:
					print('')
				nuevoAlumnoUser.save()
				sweetify.success(request, 'Se insertó', text='El alumno fue registrado exitosamente', persistent='Ok', icon="success")
			except:
				sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		else:
			#Se pretende actualizar un registro existente
			Alumno.objects.filter(id_alumno = idAlumno).update(nombre_alumno = nombreAlumno, email = email, tel_fijo = telFijo, tel_celular = telCelular, curp_alumno = curp,
				num_matricula = numMatricula, nombre_escuela = nombreEscuela, cct = cct, semestre = semestre, tipo_secundaria = tipo_secundaria, beca = beca, subsistema_nombre = subsistema)
			#CustomUser.objects.filter(email = email).update(password = contrasena)
			sweetify.success(request, 'Se actualizó', text='El alumno fue actualizado exitosamente', persistent='Ok', icon="success")
	return render(request, 'consultaAlumnos.html', {'usuario':usuarioLogueado, "alumno":Alumnos, 'archivo':Archivos, 'modulo':Modulos, 'labels':labels, 'data':data, 'labels2':labels2, 'data2':data2, 'data3':auxData3, 'labels3':auxLabels3, 'totalAlumnos':totalAlumnos, 'modulosDocente':ModulosDocente, 'indices3':indices3, 'indicesDocente':indicesDocente, 'estadistica':Estadistica })

#Función para generar los reportes
def generar_reporte(labels, data, labels2, data2, auxData3, auxLabels3, Estadistica_modulos, Modulos, totalAlumnos, indices3, indicesDocente):	
	#Para generar un reporte por módulos de manera general
	labels = []
	data = []
	try:
		size = len(Estadistica_modulos)
		if size == 0:
			size = 1
	except:
		size = 1
	#Para generar los promedios por modulos, se declaran variables para la suma y promedio de cada asignatura (32)
	#TODO:Analizar cambiarlos por arreglos y/o del modelo traido de la bd de los modelos (añadir clave de campo) no c pudo
	sum_mat1 = sum_fis1 = sum_ev1 = sum_met_inv = sum_tlr1 = sum_ing1 = sum_mat2 = sum_fis2 = sum_ev2 = sum_ics = sum_tlr2 = sum_ing2 = sum_mat3 = sum_q1 = sum_bio1 = sum_hm1 = sum_lit1 = sum_ing3 = sum_sft1 = sum_mat4 = sum_q2 = sum_bio2 = sum_hm2 = sum_lit2 = sum_ing4 = sum_sft2 = sum_geog = sum_huc = sum_cdemyce = sum_cdecsyh = sum_cdec = sum_sft3 = sum_filos = sum_ema = sum_met_invx = sum_derech2 = sum_cc2 = sum_cs2 = sum_proyes2 =  0
	prom_mat1 = prom_fis1 = prom_ev1 = prom_met_inv = prom_tlr1 = prom_ing1 = prom_mat2 = prom_fis2 = prom_ev2 = prom_ics = prom_tlr2 = prom_ing2 = prom_mat3 = prom_q1 = prom_bio1 = prom_hm1 = prom_lit1 = prom_ing3 = prom_sft1 = prom_mat4 = prom_q2 = prom_bio2 = prom_hm2 = prom_lit2 = prom_ing4 = prom_sft2 = prom_geog = prom_huc = prom_cdemyce = prom_cdecsyh = prom_cdec = prom_sft3 = prom_filos = prom_ema = prom_met_invx = prom_derech2 = prom_cc2 = prom_cs2 = prom_proyes2 =  0
	#Se acumulan los promedios por cada asignatura
	for e in Estadistica_modulos:
		if e.prom_mat1 == None: e.prom_mat1 = 0  
		sum_mat1 += float(e.prom_mat1)
		if e.prom_fis1 == None: e.prom_fis1 = 0
		sum_fis1 += float(e.prom_fis1)
		if e.prom_ev1 == None: e.prom_ev1 = 0
		sum_ev1 += float(e.prom_ev1)
		if e.prom_met_inv == None: e.prom_met_inv = 0
		sum_met_inv += float(e.prom_met_inv)
		if e.prom_tlr1 == None: e.prom_tlr1 = 0
		sum_tlr1 += float(e.prom_tlr1)
		if e.prom_ing1 == None: e.prom_ing1 = 0
		sum_ing1 += float(e.prom_ing1)
		if e.prom_mat2 == None: e.prom_mat2 = 0
		sum_mat2 += float(e.prom_mat2)
		if e.prom_fis2 == None: e.prom_fis2 = 0 
		sum_fis2 += float(e.prom_fis2)
		if e.prom_ev2 == None: e.prom_ev2 = 0 
		sum_ev2 += float(e.prom_ev2)
		if e.prom_ics == None: e.prom_ics = 0 
		sum_ics += float(e.prom_ics)
		if e.prom_tlr2 == None: e.prom_tlr2 = 0 
		sum_tlr2 += float(e.prom_tlr2)
		if e.prom_ing2 == None: e.prom_ing2 = 0 
		sum_ing2 += float(e.prom_ing2)
		if e.prom_mat3 == None: e.prom_mat3 = 0
		sum_mat3 += float(e.prom_mat3)
		if e.prom_q1 == None: e.prom_q1 = 0
		sum_q1 += float(e.prom_q1)
		if e.prom_bio1 == None: e.prom_bio1 = 0
		sum_bio1 += float(e.prom_bio1)
		if e.prom_hm1 == None: e.prom_hm1 = 0
		sum_hm1 += float(e.prom_hm1)
		if e.prom_lit1 == None: e.prom_lit1 = 0
		sum_lit1 += float(e.prom_lit1)
		if e.prom_ing3 == None: e.prom_ing3 = 0
		sum_ing3 += float(e.prom_ing3)
		if e.prom_sft1 == None: e.prom_sft1 = 0
		sum_sft1 += float(e.prom_sft1)
		if e.prom_mat4 == None: e.prom_mat4 = 0
		sum_mat4 += float(e.prom_mat4)
		if e.prom_q2 == None: e.prom_q2 = 0
		sum_q2 += float(e.prom_q2)
		if e.prom_bio2 == None: e.prom_bio2 = 0
		sum_bio2 += float(e.prom_bio2)
		if e.prom_hm2 == None: e.prom_hm2 = 0
		sum_hm2 += float(e.prom_hm2)
		if e.prom_lit2 == None: e.prom_lit2 = 0
		sum_lit2 += float(e.prom_lit2)
		if e.prom_ing4 == None: e.prom_ing4 = 0
		sum_ing4 += float(e.prom_ing4)
		if e.prom_sft2 == None: e.prom_sft2 = 0
		sum_sft2 += float(e.prom_sft2)
		if e.prom_geog == None: e.prom_geog = 0
		sum_geog += float(e.prom_geog)
		if e.prom_huc == None: e.prom_huc = 0
		sum_huc += float(e.prom_huc)
		if e.prom_cdemyce == None: e.prom_cdemyce = 0
		sum_cdemyce += float(e.prom_cdemyce)
		if e.prom_cdecsyh == None: e.prom_cdecsyh = 0
		sum_cdecsyh += float(e.prom_cdecsyh)
		if e.prom_cdec == None: e.prom_cdec = 0
		sum_cdec += float(e.prom_cdec)
		if e.prom_sft3 == None: e.prom_sft3 = 0
		sum_sft3 += float(e.prom_sft3)
		if e.prom_filos == None: e.prom_filos = 0
		sum_filos += float(e.prom_filos)
		if e.prom_ema == None: e.prom_ema = 0
		sum_ema += float(e.prom_ema)
		if e.prom_met_invx == None: e.prom_met_invx = 0
		sum_met_invx += float(e.prom_met_invx)
		if e.prom_derech2 == None: e.prom_derech2 = 0
		sum_derech2 += float(e.prom_derech2)
		if e.prom_cc2 == None: e.prom_cc2 = 0
		sum_cc2 += float(e.prom_cc2)
		if e.prom_cs2 == None: e.prom_cs2 = 0 
		sum_cs2 += float(e.prom_cs2)
		if e.prom_proyes2 == None: e.prom_proyes2 = 0
		sum_proyes2 += float(e.prom_proyes2)
	#Calcular los promedios de las sumas de cada asignatura entre los registros
	prom_mat1 = sum_mat1 / size
	prom_fis1 = sum_fis1 / size
	prom_ev1 = sum_ev1 / size
	prom_met_inv = sum_met_inv / size
	prom_tlr1 = sum_tlr1 / size
	prom_ing1 = sum_ing1 / size
	prom_mat2 = sum_mat2 / size
	prom_fis2 = sum_fis2 / size
	prom_ev2 = sum_ev2 / size
	prom_ics = sum_ics / size
	prom_tlr2 = sum_tlr2 / size
	prom_ing2 = sum_ing2 / size
	prom_mat3 = sum_mat3 / size
	prom_q1 = sum_q1 / size
	prom_bio1 = sum_bio1 / size
	prom_hm1 = sum_hm1 / size
	prom_lit1 = sum_lit1 / size
	prom_ing3 = sum_ing3 / size
	prom_sft1 = sum_sft1 / size
	prom_mat4 = sum_mat4 / size
	prom_q2 = sum_q2 / size
	prom_bio2 = sum_bio2 / size
	prom_hm2 = sum_hm2 / size
	prom_lit2 = sum_lit2 / size
	prom_ing4 = sum_ing4 / size
	prom_sft2 = sum_sft2 / size
	prom_geog = sum_geog / size
	prom_huc = sum_huc / size
	prom_cdemyce = sum_cdemyce / size
	prom_cdecsyh = sum_cdecsyh / size
	prom_cdec = sum_cdec / size
	prom_sft3 = sum_sft3 / size
	prom_filos = sum_filos / size
	prom_ema = sum_ema / size
	prom_met_invx = sum_met_invx / size
	prom_derech2 = sum_derech2 / size
	prom_cc2 = sum_cc2 / size
	prom_cs2 = sum_cs2 / size
	prom_proyes2 = sum_proyes2 / size
	#data contiene todos los promedios de todas las asignaturas
	data = [prom_mat1,  prom_fis1,  prom_ev1,  prom_met_inv,  prom_tlr1,  prom_ing1,  prom_mat2,  prom_fis2,  prom_ev2, prom_ics, prom_tlr2,  prom_ing2,  prom_mat3,  prom_q1,  prom_bio1,  prom_hm1,  prom_lit1,  prom_ing3,  prom_sft1,  prom_mat4,  prom_q2,  prom_bio2,  prom_hm2,  prom_lit2,  prom_ing4,  prom_sft2,  prom_geog,  prom_huc,  prom_cdemyce,  prom_cdecsyh,  prom_cdec,  prom_sft3,  prom_filos,  prom_ema,  prom_met_invx,  prom_derech2,  prom_cc2,  prom_cs2,  prom_proyes2]
	#Para acomodar las asignaturas x modulo
	mod1 = (prom_mat1 + prom_fis1)/2
	mod2 = (prom_ev1 + prom_met_inv)/2
	mod3 = (prom_tlr1 + prom_ing1)/2
	mod4 = (prom_mat2 + prom_fis2)/2
	mod5 = (prom_ev2 + prom_ics)/2
	mod6 = (prom_tlr2 + prom_ing2)/2
	mod7 = (prom_mat3 + prom_q1 + prom_bio1)/3
	mod8 = prom_hm1
	mod9 = (prom_lit1 + prom_ing3)/2
	mod10 = prom_sft1
	mod11 = (prom_mat4 + prom_q2 + prom_bio2)/3
	mod12 = prom_hm2
	mod13 = (prom_lit2 + prom_ing4)/2
	mod14 = prom_sft2
	mod15 = prom_geog
	mod16 = prom_huc
	mod17 = prom_cdemyce
	mod18 = prom_cdecsyh
	mod19 = prom_cdec
	mod20 = prom_sft3
	#data ahora contiene todos los promedios de todos los modulos
	data = [mod1, mod2, mod3, mod4, mod5, mod6, mod7, mod8, mod9, mod10, mod11, mod12, mod13, mod14, mod15, mod16, mod17, mod18, mod19, mod20]
	for mod in Modulos:
		labels.append(mod.nombre_modulo)
	#Para generar reporte por módulos, almacenar las calificaciones de cada modulo y sacar datos correspondientes a ponderación de [0-5, 6, 7, 8, 9, 10] (estos serán los labels)
	labels2 = ['Promedio: 0-5', 'Promedio: 6', 'Promedio: 7', 'Promedio: 8', 'Promedio: 9', 'Promedio: 10']
	mat1, fis1, ev1, met_inv, tlr1, ing1, mat2, fis2, ev2, ics ,tlr2, ing2, mat3, q1, bio1, hm1, lit1, ing3, sft1, mat4, q2, bio2, hm2, lit2, ing4, sft2, geog, huc, cdemyce, cdecsyh, cdec, sft3, filos, ema, met_invx, derech2, cc2, cs2, proyes2 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
	#Se almacenan todas los promedios
	for e in Estadistica_modulos:
		if e.prom_mat1 == None: e.prom_mat1 = 0  
		mat1.append(float(e.prom_mat1))
		if e.prom_fis1 == None: e.prom_fis1 = 0  
		fis1.append(float(e.prom_fis1))
		if e.prom_ev1 == None: e.prom_ev1 = 0  
		ev1.append(float(e.prom_ev1))
		if e.prom_met_inv == None: e.prom_met_inv = 0  
		met_inv.append(float(e.prom_met_inv))
		if e.prom_tlr1 == None: e.prom_tlr1 = 0  
		tlr1.append(float(e.prom_tlr1))
		if e.prom_ing1 == None: e.prom_ing1 = 0  
		ing1.append(float(e.prom_ing1))
		if e.prom_mat2 == None: e.prom_mat2 = 0  
		mat2.append(float(e.prom_mat2))
		if e.prom_fis2 == None: e.prom_fis2 = 0  
		fis2.append(float(e.prom_fis2))
		if e.prom_ev2 == None: e.prom_ev2 = 0  
		ev2.append(float(e.prom_ev2))
		if e.prom_ics == None: e.prom_ics = 0  
		ics.append(float(e.prom_ics))
		if e.prom_tlr2 == None: e.prom_tlr2 = 0  
		tlr2.append(float(e.prom_tlr2))
		if e.prom_ing2 == None: e.prom_ing2 = 0  
		ing2.append(float(e.prom_ing2))
		if e.prom_mat3 == None: e.prom_mat3 = 0  
		mat3.append(float(e.prom_mat3))
		if e.prom_q1 == None: e.prom_q1 = 0  
		q1.append(float(e.prom_q1))
		if e.prom_bio1 == None: e.prom_bio1 = 0  
		bio1.append(float(e.prom_bio1))
		if e.prom_hm1 == None: e.prom_hm1 = 0  
		hm1.append(float(e.prom_hm1))
		if e.prom_lit1 == None: e.prom_lit1 = 0  
		lit1.append(float(e.prom_lit1))
		if e.prom_ing3 == None: e.prom_ing3 = 0  
		ing3.append(float(e.prom_ing3))
		if e.prom_sft1 == None: e.prom_sft1 = 0  
		sft1.append(float(e.prom_sft1))
		if e.prom_mat4 == None: e.prom_mat4 = 0  
		mat4.append(float(e.prom_mat4))
		if e.prom_q2 == None: e.prom_q2 = 0  
		q2.append(float(e.prom_q2))
		if e.prom_bio2 == None: e.prom_bio2 = 0  
		bio2.append(float(e.prom_bio2))
		if e.prom_hm2 == None: e.prom_hm2 = 0  
		hm2.append(float(e.prom_hm2))
		if e.prom_lit2 == None: e.prom_lit2 = 0  
		lit2.append(float(e.prom_lit2))
		if e.prom_ing4 == None: e.prom_ing4 = 0  
		ing4.append(float(e.prom_ing4))
		if e.prom_sft2 == None: e.prom_sft2 = 0  
		sft2.append(float(e.prom_sft2))
		if e.prom_geog == None: e.prom_geog = 0  
		geog.append(float(e.prom_geog))
		if e.prom_huc == None: e.prom_huc = 0  
		huc.append(float(e.prom_huc))
		if e.prom_cdemyce == None: e.prom_cdemyce = 0  
		cdemyce.append(float(e.prom_cdemyce))
		if e.prom_cdecsyh == None: e.prom_cdecsyh = 0  
		cdecsyh.append(float(e.prom_cdecsyh))
		if e.prom_cdecsyh == None: e.prom_cdecsyh = 0 
		cdec.append(float(e.prom_cdec))
		if e.prom_sft3 == None: e.prom_sft3 = 0  
		sft3.append(float(e.prom_sft3))
		if e.prom_filos == None: e.prom_filos = 0  
		filos.append(float(e.prom_filos))
		if e.prom_ema == None: e.prom_ema = 0  
		ema.append(float(e.prom_ema))
		if e.prom_met_invx == None: e.prom_met_invx = 0  
		met_invx.append(float(e.prom_met_invx))
		if e.prom_derech2 == None: e.prom_derech2 = 0  
		derech2.append(float(e.prom_derech2))
		if e.prom_cc2 == None: e.prom_cc2 = 0  
		cc2.append(float(e.prom_cc2))
		if e.prom_cs2 == None: e.prom_cs2 = 0  
		cs2.append(float(e.prom_cs2))
		if e.prom_cs2 == None: e.prom_cs2 = 0   
		proyes2.append(float(e.prom_proyes2))
	#Se procede a buscar en el arreglo y llevar conteo de cuantos pertenecen a la ponderación [0-5, 6, 7, 8, 9, 10]
	f = s = sv = e = n = t = 0 #[0-5, 6, 7, 8, 9, 10]
	#Se genera el total de alumnos por institución
	totalAlumnos = len(ev1)
	#Se acomodan los modulos respecto a sus asignaturas
	mod1 = mat1 + fis1
	mod2 = ev1 + met_inv
	mod3 = tlr1 + ing1
	mod4 = mat2 + fis2
	mod5 = ev2 + ics
	mod6 = tlr2 + ing2
	mod7 = mat3 + q1 + bio1
	mod8 = hm1
	mod9 = lit1 + ing3
	mod10 = sft1
	mod11 = mat4 + q2 + bio2
	mod12 = hm2
	mod13 = lit2 + ing4
	mod14 = sft2
	mod15 = geog
	mod16 = huc
	mod17 = cdemyce
	mod18 = cdecsyh
	mod19 = cdec
	mod20 = sft3
	#arr contendrá los arreglos de todos los prmedios por modulo i.e -> mod1[6,7,8.2,9,5,1,2,3]
	arr = [mod1, mod2, mod3, mod4, mod5, mod6, mod7, mod8, mod9, mod10, mod11, mod12, mod13, mod14, mod15, mod16, mod17, mod18, mod19, mod20]
	data2 = []
	#Ciclo para recorrer cada elemento de arr y evaluar a que ponderacion pertenece
	for row in arr:
		for elem in row:
			if elem >= 0 and elem < 6:
				f += 1
			if elem >= 6 and elem < 7:
				s += 1
			if elem >= 7 and elem < 8:
				sv += 1
			if elem >= 8 and elem < 9:
				e += 1
			if elem >= 9 and elem < 10:
				n += 1
			if elem == 10:
				t += 1
		p2 = [f, s, sv, e, n, t]
		data2.append(p2)
		f = s = sv = e = n = t = 0
	#data2 contiene los arreglos con los conteos de cada modulo mat1=[16,11,10,10,5,0]
	#Para generar el indice de reprobacion
	ir = 0
	idMod = 1
	labels3 = []
	data3 = []
	for row in arr:
		for elem in row:
			if elem < 6:
				ir += 1
		data3.append(ir)
		labels3.append(idMod)
		idMod += 1
		ir = 0
	#labels3 tiene el id del modulo
	#data3 tiene los indices de reprobacion por modulo (en el orden de los id de los modulos)
	#Se debe de filtrar los arreglos de data3 y labels3 dejando solo los que tengan indice de reprobacion real -> no sea 0 ni sea igual al total de alumnos (modulo no evaluado)
	#Para obtener y generar los indices de los modulos con mayor reprobacion
	#Se hará uso de arr, que contiene todos los promedios de todos los modulos de la institución
	auxData3 = []
	auxLabels3 = []
	indices3 = []
	for idx, i in enumerate(data3):
		if i != 0 and i != totalAlumnos and i != (totalAlumnos * 2) and i != (totalAlumnos * 3) and i!= (totalAlumnos * 4):
			auxPorcentaje = (i * 100) / totalAlumnos
			auxData3.append(data3[idx])
			auxLabels3.append(labels[idx])
			indices3.append(idx+1)
	#auxLabels3 contiene los nombres de los modulos con indice de reprobacion ya filtrado
	#auxData3 contiene los indices de reprobacion de los modulos correspondientes
	return labels, data, labels2, data2, auxData3, auxLabels3, totalAlumnos, indices3, indicesDocente

#Función para eliminar un alumnos, dado un id (id como parámetro)

def delete_alumno(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	AlumnoD = Alumno.objects.get(id_alumno = id)
	#AlumnoDU = CustomUser.objects.get()
	try:
		AlumnoD.delete()
		sweetify.success(request, 'Se eliminó', text='El alumno fue eliminado exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='Ocurrió un error', persistent='Ok', icon="error")
	return redirect('TBC:consultaAlumnos')

#Función para consultar el historial académico de un alumno o de un grupo

def historialAcademico(request):
	Alumnos = Alumno.objects.all()
	AlumnoSel = Alumno.objects.all()
	AlumnosGrupo = None
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		nombreAlumno = request.POST['nombreAlumno']
		try:
			AlumnoSel = Alumno.objects.get(nombre_alumno = nombreAlumno)
		except:
			grupoSel = request.POST['grupo']
			AlumnosGrupo = Alumno.objects.filter(semestre = grupoSel)
	return render(request, 'historialAcademico.html', {'usuario':usuarioLogueado, "alumno":Alumnos, "alumnoSel":AlumnoSel, 'alumnoGrupo':AlumnosGrupo }) #, "prueba":list_of_hashes})

#Función para realizar el pase de lista

def paseLista(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Alumnos = Alumno.objects.all()
	AlumnoSel = None
	alumnoCurso = Alumno_curso.objects.all()
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	AsistenciasG = None
	materia = None
	AlumnoSelM = None
	try:
		Docentes = Docente.objects.filter(id_docente = idDocente)
		DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	except:
		Docentes = Docente.objects.all()
		DocenteCursos = Docente_curso.objects.all()

	if request.method == 'POST':
		bandera = request.POST['bandera']
		if bandera == 'False':
			try:
				#Entra para buscar un historial como docente
				print('huevos')
				materiaH = request.POST['materiaH']
				grupoH = request.POST['grupoH']
				semestreH = request.POST['semestreH']
				fechaH = ' ' + request.POST['fechaH'] + ' '
				print(grupoH, fechaH, semestreH, materiaH)
				#Aqui la materia debe ser el id_dc que cursa el alumno
				AsistenciasG = Asistencia.objects.filter(cct = grupoH, semestre = semestreH, id_dc = materiaH, fecha = fechaH)
				print('ya buscó')
			except:
				#Entra para sólo buscar algun grupo en especifico para después tomar lista
				materia = request.POST['materia']
				grupo = request.POST['grupo']
				semestre = request.POST['semestre']
				#En el template se filtra que pertenezcan a la materia
				AlumnoSel = Alumno.objects.filter(cct = grupo, semestre = semestre)
				#Se debe de sacar el id_dc de quien imparta el id_curso = materia
				field_name = 'id_dc'
				obj = Docente_curso.objects.get(id_curso = materia)
				field_value = getattr(obj, field_name)
				idDc = field_value
				AlumnoSelM = Alumno_curso.objects.filter( id_dc = idDc)
		elif bandera == 'True':
			#Entra aquí para guardar la lista
			#TODO: Jalar la lista de los campos: nombre, matricula, asistencia, retardo, justificacion
			alumnosL = request.POST.getlist('nombreAlumnoTabla') or None
			matriculasL = request.POST.getlist('matriculaAlumnoTabla') or None
			cctL = request.POST.getlist('cctL') or None
			fechaL = request.POST.getlist('fechaL') or None
			semestreL = request.POST.getlist('semestreL') or None
			id_dcL = request.POST.getlist('id_dcL') or None  
			id_alumnoL = request.POST.getlist('id_alumnoL') or None
			falta = False
			idx = 0
			#Se comprueba si ya se tomó lista ese día en ese grupo* (semestre y módulo)
			existe = Asistencia.objects.filter(fecha = fechaL[0], id_dc = id_dcL[0], cct = cctL[0], semestre = semestreL[0]).count()
			if existe > 0:
				sweetify.error(request, 'Pase de lista ya realizado', text='El pase de lista ya fue realizado previamente!', persistent='Ok', icon="info")
			else:
				for al in alumnosL:
					if not request.POST.get('Asistencia'+str(idx)):
						asistencia = False
					else:
						asistencia = True
					
					if not request.POST.get('Retardo'+str(idx)):
						retardo = False
					else:
						retardo = True
					if not request.POST.get('Justificacion'+str(idx)):
						justificacion = False
					else:
						justificacion = True
					if asistencia == False and retardo == False and justificacion == False:
						falta = True
					#Se procede a guardar los registros en la tabla de asistencia
					paseLista = Asistencia(cct = cctL[0], fecha = fechaL[0], semestre = semestreL[0], id_alumno = id_alumnoL[idx], id_dc = id_dcL[0], asistencia = asistencia, retardo = retardo, justificacion = justificacion, falta = falta)
					paseLista.save()
					#print(id_alumnoL[idx] ,al,cctL[0], fechaL[0], semestreL[0], matriculasL[idx], id_dcL[0], 'Asistencia:', asistencia, 'Retardo:', retardo, 'Justificacion:', justificacion, 'Falta:', falta)
					idx += 1
					sweetify.success(request, 'Pase de lista exitoso', text='¡El pase de lista se guardó correctamente', persistent='Ok', icon="success")

	return render(request, 'paseLista.html', {'usuario':usuarioLogueado, "alumno":Alumnos, "alumnoSel":AlumnoSel, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'modulo':Modulos, 'asistencia':AsistenciasG, 'alumnoSelM':AlumnoSelM, 'alumnoCurso':alumnoCurso}) #, "prueba":list_of_hashes})


#Función para consultar y actualizar docentes

def consultaDocentes(request):
	Docentes = Docente.objects.filter(cct = request.user.last_name) #Docente.objects.all()
	Archivos = Archivo.objects.all()
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		idDocente = request.POST['idDocente']
		nombresDocente = request.POST['nombresDocente']
		apellidosDocente = request.POST['apellidosDocente']
		edad = request.POST['edad']
		email = request.POST['email']
		cct = request.POST['cct']
		curp_docente = request.POST['curp']
		rfc = request.POST['rfc']
		telFijo = request.POST['telFijo']
		telCelular = request.POST['telCelular']
		nombreEscuela = request.POST['nombreEscuela']
		area = request.POST['areaDocente']

		domicilio = request.POST['domicilio']
		num_empleado = request.POST['num_empleado']
		perfil_profesional = request.POST['perfil_profesional']
		maximo_grado = request.POST['maximo_grado']
		#curriculum = request.POST['curriculum']

		contrasena = make_password(request.POST['contrasena'])
		#Compara si el id está vacio para insertar nuevo reigstro
		if idDocente == '':
			try:
				field_name = 'id_docente'
				obj = Docente.objects.last()
				field_value = getattr(obj, field_name)
				idDocente = field_value + 1
			except:
				idDocente = 1
			try:
				nuevoDocente = Docente(id_docente = idDocente, nombres_docente = nombresDocente, apellidos_docente = apellidosDocente, edad_docente = edad, email = email, 
				cct = cct, curp_docente = curp_docente, rfc_docente = rfc, tel_fijo = telFijo, tel_cel = telCelular, nombre_escuela = nombreEscuela,
				domicilio = domicilio, num_empleado = num_empleado, perfil_profesional = perfil_profesional, maximo_grado = maximo_grado, areadisciplinar_docente_id = area)
				nuevoDocente.save()
				nuevoDocenteU = CustomUser(password = contrasena, username = email, first_name = nombresDocente, last_name = cct, email = email, curp_rfc = rfc, 
				municipio = nombreEscuela, tipo_usuario = 6, tipo_persona = 1)
				nuevoDocenteU.save()

				#Código para guardar los archivos [acta, curp, y certificado] en la carpeta TODO: Guardar en la tabla archivo tambien
				try:
					curriculum = request.FILES['curriculum']
					#fsCurriculum = FileSystemStorage("media/TBC/Datos/Docentes")
					#nameCurriculum = fsCurriculum.save(curriculum.name, curriculum)
					#urlCurriculum = fsCurriculum.url(nameCurriculum)
					#aqui guardar el registro en la tabla de archivos
					#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
					try:
						field_name = 'id_archivo'
						obj = Archivo.objects.last()
						field_value = getattr(obj, field_name)
						idArchivo = field_value + 1
					except:
						idArchivo = 1
					
					url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+curriculum.name #'/media/TBC/Datos/Docentes/'+curriculum.name
					nuevoArchivo = Archivo(id_archivo = idArchivo, nombre_archivo = curriculum.name, tipo_archivo = 'Curriculum', url = url, id_docente = idDocente)
					nuevoArchivo.archivo = curriculum
					nuevoArchivo.save()
				except:
					print('')

				sweetify.success(request, 'Se insertó', text='El docente fue registrado exitosamente', persistent='Ok', icon="success")
			except Exception as e:
				print(e)
				sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		else:
			#Se pretende actualizar un registro existente
			Docente.objects.filter(id_docente = idDocente).update(id_docente = idDocente, nombres_docente = nombresDocente, apellidos_docente = apellidosDocente, edad_docente = edad, email = email, 
			 	cct = cct, curp_docente = curp_docente, rfc_docente = rfc, tel_fijo = telFijo, tel_cel = telCelular, nombre_escuela = nombreEscuela,
				domicilio = domicilio, num_empleado = num_empleado, perfil_profesional = perfil_profesional, maximo_grado = maximo_grado, areadisciplinar_docente_id = area)
			#CustomUser.objects.filter(email = email).update(password = contrasena)
			sweetify.success(request, 'Se actualizó', text='El docente fue actualizado exitosamente', persistent='Ok', icon="success")
	return render(request, 'consultaDocentes.html', {'usuario':usuarioLogueado, "docente":Docentes, 'archivo':Archivos, })

#Función para eliminar un docente dado su id (id como parámetro)

def delete_docente(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	DocentesL = Docente.objects.all()
	DocenteD = Docente.objects.get(id_docente = id)
	try:
		DocenteD.delete()
		sweetify.success(request, 'Se eliminó', text='El docente fue eliminado exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='El docente aun tiene cursos relacionados', persistent='Ok', icon="error")
	return redirect('TBC:consultaDocentes')

#Función para mostrar las actividades relacionadas al docente logeado

def actividadesAprendizaje(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Docentes = Docente.objects.filter(id_docente = idDocente)
	DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	Cursos = Modulo.objects.all()
	Modulos = Modulo.objects.all()
	ActividadDocente = Actividad_docente.objects.filter(id_docente = idDocente)
	NotificacionAct = Notificacion_act.objects.all()
	NotificacionActDocente = Notificacion_act_docente.objects.filter(id_docente = idDocente)
	Entregas = Entrega_actividad.objects.all()
	#Cursos = Curso.objects.filter(DocenteCurso.id_curso)

	return render(request, 'actividadesAprendizaje.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'curso':Cursos, 'modulo':Modulos,'actividad_docente': ActividadDocente, 
		'notificaciones':NotificacionAct, 'notificacion': NotificacionActDocente, 'entregas':Entregas }) 

#Función para insertar una actividad, datos y archivos

def nuevaActividad(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	c = 0
	cRub = 0
	DocenteCursos = Docente_curso.objects.filter(id_docente = idDocente)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	Docentes = Docente.objects.filter(id_docente = idDocente)
	ActividadDocente = Actividad_docente.objects.filter(id_docente = idDocente)
	if request.method == 'POST':
		nombreArchivos = ''
		nombreRubrica = ''
		try:
			field_name = 'id_actividad'
			obj = Actividad_docente.objects.last()
			field_value = getattr(obj, field_name)
			idActividad = field_value + 1
		except:
			idActividad = 1
		nombreActividad = request.POST['nombreActividad']
		unidad = request.POST['unidad']
		tipoActividad = request.POST['tipoActividad']
		tema = request.POST['tema']
		subtema = request.POST['subtema']
		objetivoActividad = request.POST['objetivoActividad']
		#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
		for afile in request.FILES.getlist('recurso'):
			#myfile = afile
			#fs = FileSystemStorage("media/TBC/Docente/Recursos")
			#filename = fs.save(myfile.name, myfile)
			#uploaded_file_url = fs.url(filename)
			nombreArchivos += afile.name + '\n'
			#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
			try:
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
			except:
				idArchivo = 1
			descripcion = request.POST.getlist('descRecurso')
			url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+afile.name #'/media/TBC/Docente/Recursos/'+afile.name
			ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Recurso', id_actividad = idActividad, url= url)
			ArchivoNuevo.archivo = afile
			ArchivoNuevo.save()
			c += 1

		#Ciclo para recorrer los archivos seleccionados y guardarlos (rubrica)
		for afile in request.FILES.getlist('rubrica'):
			#myfile = afile
			#fs = FileSystemStorage("media/TBC/Docente/Rubricas")
			#filename = fs.save(myfile.name, myfile)
			#uploaded_file_url = fs.url(filename)
			nombreRubrica += afile.name + '\n'
			#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
			try:
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
			except:
				idArchivo = 1
			descripcionRubrica = request.POST.getlist('descRubrica')
			url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+afile.name #'/media/TBC/Docente/Rubricas/'+afile.name
			ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcionRubrica[cRub], tipo_archivo = 'Rubrica', id_actividad = idActividad, url= url)
			ArchivoNuevo.archivo = afile
			ArchivoNuevo.save()
			cRub += 1
		date_joined = datetime.now()
		formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")	
		fecha = formatted_datetime
		valorActividad = request.POST['valorActividad']
		fechaHoraLimite = request.POST['fechaHoraLimite']
		modulo = request.POST['moduloActividad']
		nuevaActividad = Actividad_docente(id_actividad = idActividad, nombre_actividad = nombreActividad, unidad = unidad, tipo_actividad = tipoActividad, tema = tema,
		subtema = subtema, objetivo = objetivoActividad, valor_parcial = valorActividad, fecha_hora_limite = fechaHoraLimite,
		fechaAct = fecha, id_docente = idDocente, id_curso = modulo)
		nuevaActividad.save()
		#Se obtiene el campo id_dc de la tabla de Docente_curso
		field_name = 'id_dc'
		obj = Docente_curso.objects.get(id_docente = idDocente, id_curso = modulo)
		field_value = getattr(obj, field_name)
		idDc = field_value
		notifAct = Notificacion_act(id_dc = idDc, id_actividad = idActividad, mensaje = 'Nueva actividad', tipo = 1)
		notifAct.save()

		field_name = 'id_notificacion'
		obj = Notificacion_act.objects.last()    #.get(id_dc = idDc).last()
		field_value = getattr(obj, field_name)
		idNotif = field_value


		#TODO: Con el campo id_dc (y id_alumno resultante de consultar la tabla alumno_curso) obtener todos los id_alumno
		field_name = 'id_alumno'
		obj = Alumno_curso.objects.filter(id_dc = idDc)
		for o in obj:
			field_value = getattr(o, field_name)
			idAl = field_value
			print(idNotif)
			notifActAl = Notificacion_act_alumno(id_alumno = idAl, status = 0, id_notificacion = idNotif, id_dc = idDc)
			notifActAl.save()
		sweetify.success(request, 'Se insertó', text='La actividad fue registrado exitosamente', persistent='Ok', icon="success")
		#except:
		#	sweetify.error(request, 'No se insertó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('TBC:actividadesAprendizaje')

	return render(request, 'nuevaActividad.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'docenteCurso':DocenteCursos, 'curso':Cursos, 'modulo':Modulos }) 

'''
Función para mostrar lo relacionado a la actividad seleccionada por su id
(id como parámetro) y para actualizar los datos de la actividad
'''
def actividadD(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	c = 0
	cRub = 0
	Alumnos = Alumno.objects.all()
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Docentes = Docente.objects.filter(id_docente = idDocente)
	Entregas = Entrega_actividad.objects.filter(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)

	if request.method == 'POST':
		nombreArchivos = ''
		nombreRubrica = ''
		try:
			idActividad = id
			nombreActividad = request.POST['nombreActividad']
			unidad = request.POST['unidad']
			tipoActividad = request.POST['tipoActividad']
			tema = request.POST['tema']
			subtema = request.POST['subtema']
			objetivoActividad = request.POST['objetivoActividad']
			#TODO: Realizar la actualización de archivos ya subidos
			#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
			for afile in request.FILES.getlist('recurso'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Docente/Recursos")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreArchivos += afile.name + '\n'
				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
				descripcion = request.POST.getlist('descRecurso')
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+afile.name #'/media/TBC/Docente/Recursos/'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Recurso', id_actividad = idActividad, url= url)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				c += 1

			#Ciclo para recorrer los archivos seleccionados y guardarlos (rubrica)
			for afile in request.FILES.getlist('rubrica'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Docente/Rubricas")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreRubrica += afile.name + '\n'
				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
				descripcionRubrica = request.POST.getlist('descRubrica')
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+afile.name #'/media/TBC/Docente/Rubricas/'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcionRubrica[cRub], tipo_archivo = 'Rubrica', id_actividad = idActividad, url= url)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				cRub += 1
				
			valorActividad = request.POST['valorActividad']
			fechaHoraLimite = request.POST['fechaHoraLimite']
			Actividad_docente.objects.filter(id_actividad = id).update( nombre_actividad = nombreActividad, unidad = unidad, tipo_actividad = tipoActividad, tema = tema,
			subtema = subtema, objetivo = objetivoActividad, valor_parcial = valorActividad, fecha_hora_limite = fechaHoraLimite,
			id_docente = idDocente)
			sweetify.success(request, 'Se actualizó', text='La actividad fue actualizada exitosamente', persistent='Ok', icon="success")
		except:
			sweetify.error(request, 'No se actualizó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('TBC:actividadesAprendizaje')

	return render(request, 'actividadDocente.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos,}) 

#Función para eliminar un archivo dado su id (id como parámetro)

def delete_archivo(request, idAct, tipo, name):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	ArchivosL = Archivo.objects.all()
	ArchivoD = Archivo.objects.get(nombre_archivo = name)
	ArchivoD.delete()
	#TODO: Para eliminar el archivo de /media
	if tipo == 'Recurso':
		fs = FileSystemStorage("media/TBC/Docente/Recursos")
		filename = fs.delete(name)
	elif tipo == 'Rubrica':
		fs = FileSystemStorage("media/TBC/Docente/Rubricas")
		filename = fs.delete(name)

	return redirect('/TBC/actividad-docente/'+idAct)

#Función para eliminar una actividad dada su id (id como parámetro)

def delete_actividad(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	ActividadDocenteD = Actividad_docente.objects.get(id_actividad = id)
	Notificacion_actD = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
	#Se obitne idNotif
	field_name = 'id_notificacion'
	obj = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
	field_value = getattr(obj, field_name)
	idNotif = field_value
	Notificacion_act_alumnoD = Notificacion_act_alumno.objects.filter(id_notificacion = idNotif)
	try:
		ActividadDocenteD.delete()
		Notificacion_actD.delete()
		for n in Notificacion_act_alumnoD:
			n.delete()
		sweetify.success(request, 'Se eliminó', text='La actividad fue eliminada exitosamente', persistent='Ok', icon="success")
	except:
		sweetify.error(request, 'No se eliminó', text='Ocurrió un error', persistent='Ok', icon="error")
	ActividadDocentes = Actividad_docente.objects.all()

	return redirect('TBC:actividadesAprendizaje')

#Función para retroalimentar la actividad entregada por el alumno

def revisarActividad(request, id, idAlumno):
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)
	AlumnoS = Alumno.objects.get(id_alumno = idAlumno)
	Entrega = Entrega_actividad.objects.get(id_actividad = id, id_alumno = idAlumno)
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	if request.method == 'POST':
		try:
			#Sólo se actualizará el registro de la Entrega (actualizando los campos de calificación, retroalimentación y calificada)
			calificacion = request.POST['calificacion']
			retroalimentacion = request.POST['retroalimentacion']
			totalOb = request.POST['totalObtenido2']
			print('entra 0')
			#calificada = True
			Entrega_actividad.objects.filter(id_actividad = id, id_alumno = idAlumno).update(calificacion = calificacion, retroalimentacion = retroalimentacion, calificada = True, totalO = totalOb)
			#Se saca el id de la notificacion (tabla notif_act_alumno) correspondiente a actualizar con el id_dc y el id_actividad (tabla notifi_act)
			print('entra 1')
			field_name = 'id_notificacion'
			obj = Notificacion_act.objects.filter(id_actividad = id, tipo = 2).last()
			field_value = getattr(obj, field_name)
			idNotificacion = field_value
			print('entra 2')
			NotifStatus = Notificacion_act_docente.objects.filter(id_notificacion = idNotificacion, id_alumno = idAlumno).update(status = 1)
			sweetify.success(request, 'Se calificó', text='La actividad fue calificada exitosamente', persistent='Ok', icon="success")
		except:
			sweetify.error(request, 'No se calificó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('/TBC/actividad-docente/'+id)
	return render(request, 'revisarActividad.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'archivo':Archivos, 'alumno':AlumnoS, 'entrega':Entrega, }) 

#Función para consultar los cursos y actividades del alumno logeado

def actividadAlumno (request, id):
	AlumnoI = Alumno.objects.get(id_alumno = id)
	AlumnoCursos = Alumno_curso.objects.filter(id_alumno = id)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	ActividadAlumno = Actividad_docente.objects.all()
	NotificacionAct = Notificacion_act.objects.all()
	NotificacionActAalumno = Notificacion_act_alumno.objects.filter(id_alumno = id)
	DocenteCurso = Docente_curso.objects.all()
	#ActividadAlumno = Actividad_docente.objects.filter(id_curso = idDocente)
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	try:
		Entregas = Entrega_actividad.objects.filter(id_alumno = id)
		return render(request, 'actividadAlumno.html', {'docenteCurso':DocenteCurso, 'usuario':usuarioLogueado, 'alumno':AlumnoI, 'alumnoCurso':AlumnoCursos, 'curso':Cursos, 'modulo':Modulos ,'actividad_docente': ActividadAlumno, 'entrega': Entregas, 'notificaciones':NotificacionAct, 'notificacion':NotificacionActAalumno, })
	except:
		print('kaka')
	return render(request, 'actividadAlumno.html', {'docenteCurso':DocenteCurso,'usuario':usuarioLogueado, 'alumno':AlumnoI, 'alumnoCurso':AlumnoCursos, 'curso':Cursos,'modulo':Modulos ,'actividad_docente': ActividadAlumno, 'notificaciones':NotificacionAct, 'notificacion':NotificacionActAalumno,})

#Función para la funcionalidad de toma de lista

def ListasAsistencias(request):
	#La action del form en paseLista.html ejecuta un POST a la URL ligada a esta view
	if request.method == 'POST':
		#Creamos un workbook a traves de la libreria xlwt
		wb = xlwt.Workbook(encoding='utf-8')
		#A ese workbook le agregamos una sheet con las asistencias del módulo
		ws = wb.add_sheet('Lista Matematicas1')

		#Definimos las variables con las que navegaremos e imprimiremos en el archivo de excel
		row_num = 2
		font_style1 = xlwt.XFStyle()
		font_style1.font.bold = True
		#Creamos una lista con los encabezados del primer renglon
		columnasLista = ['Nombre Alumno','Matricula','Asistencia','Retardo','Justificacion']

		# A traves de un for imprimimos la lista pasada en la hoja de excel, indicando en que fila y en que columna se imprime cada cosa y con que fuente.
		for col_num in range(len(columnasLista)):
			ws.write(row_num, col_num, columnasLista[col_num], font_style1)
		
		#Repetimos proceso de encabezados
		infoGrupo = ['Módulo','Docente','Semestre','Periodo','Fecha']
		row_num=0
		for col_num in range(len(infoGrupo)):
			ws.write(row_num, col_num, infoGrupo[col_num], font_style1)
		font_style = xlwt.XFStyle()
		font_style.font.bold = False

		infoGrupoRes = ['Matematicas 1',request.user.first_name+" "+request.user.last_name,'4to Semestre','Enero - Junio 2020','04 Mayo 2020']
		row_num=1
		for col_num in range(len(infoGrupoRes)):
			ws.write(row_num,col_num,infoGrupoRes[col_num], font_style)

		#Obtenemos los alumnos (Por el momento son todos, despues se filtrará por grupoS)
		alumnos = Alumno.objects.all()
		row_num=3
		counter= 0
		asistenciaFinal = ""
		retardoFinal = ""
		justificacionFinal =""

		#Por cada alumno encontrado se evaluarán las checkboxes de la vista y dependiendo del valor se cambiarán los valores 
		for row in alumnos:
				if not request.POST.get('Asistencia'+str(counter)):
					asistenciaFinal = ""
				else:
					asistenciaFinal = "•"
				if not request.POST.get('Retardo'+str(counter)):
					retardoFinal = ""
				else:
					retardoFinal="•"
				if not request.POST.get('Justificacion'+str(counter)):
					justificacionFinal = ""
				else:
					justificacionFinal="•"
				#Imprimimos los valores finales de cada alumno
				ws.write(row_num,0,row.nombre_alumno, font_style)
				ws.write(row_num,1,row.num_matricula, font_style)
				ws.write(row_num,2,asistenciaFinal,font_style)
				ws.write(row_num,3,retardoFinal,font_style)
				ws.write(row_num,4,justificacionFinal,font_style)
				row_num+=1
				counter+=1
		#Guardamos nuestrow workbook y retornamos
		response = HttpResponse(content_type='application/ms-excel')
		response['Content_Disposition'] = 'attachment; filename="test.xls"'
		wb.save(response)
		return response


'''
Inicio de la sección de vistas para el control de módulos
'''
def nuevoModulo(request):
	semestres = Semestre.objects.all()
	areas_disc = Area_disciplinar.objects.all()
	Modulos = Modulo.objects.all()
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	return render(request, 'nuevoModulo.html',{'semestres': semestres,'areas_disc':areas_disc,'modulos':Modulos,'usuario':usuarioLogueado})

def nuevoModuloInsertar(request):
	if request.is_ajax:
		moduloNuevo = Modulo(nombre_modulo = request.GET.get('nombre'), semestre_modulo = Semestre.objects.get(id_semestre=request.GET.get('semestre')), areadisciplinar_modulo = Area_disciplinar.objects.get(id_areadisciplinar=request.GET.get('AD')), creditos_modulo = request.GET.get('creditos'))
		moduloNuevo.save()
		data = serializers.serialize("json",Modulo.objects.filter(nombre_modulo=request.GET.get('nombre')))
		return JsonResponse(data,safe=False)

def nuevaUnidad(request):
	if request.is_ajax:
		print('============='+request.GET.get('moduloDeLaUnidad')+'    lol=========')
		unidadNueva = Unidad_modulo(nombre_unidad = request.GET.get('nombreUnidad'), id_modulo_unidad = Modulo.objects.get(id_modulo=request.GET.get('moduloDeLaUnidad')), proposito_unidad = "")
		unidadNueva.save()
		data = serializers.serialize("json",Unidad_modulo.objects.filter(nombre_unidad=request.GET.get('nombreUnidad')))
		return JsonResponse(data,safe=False)

def nuevoApes(request):
	if request.is_ajax:
		apesNuevo = Aprendizaje_esperado_modulo(aprendizaje_esperado = request.GET.get('apesDeLaUnidad'), unidad_aprendizaje_esperado = Unidad_modulo.objects.get(id_unidad=request.GET.get('nombreUnidad')), modulo_aprendizaje_esperado = Modulo.objects.get(nombre_modulo=request.GET.get('modulo')))
		apesNuevo.save()
		data = serializers.serialize("json",Aprendizaje_esperado_modulo.objects.filter(aprendizaje_esperado=request.GET.get('apesDeLaUnidad')))
		return JsonResponse(data,safe=False)

def getAPES(request,idNombre):
	if request.is_ajax:
		data = serializers.serialize("json",Aprendizaje_esperado_modulo.objects.filter(unidad_aprendizaje_esperado = idNombre))
		return JsonResponse(data,safe=False)

def deleteUnidad(request,idNombre):
	if request.is_ajax:
		deleteAPES = Aprendizaje_esperado_modulo.objects.filter(unidad_aprendizaje_esperado = idNombre).delete()
		deletetionUnidad = Unidad_modulo.objects.filter(id_unidad=idNombre).delete()
		return JsonResponse("deleted",safe=False)

def getUnidades(request):
	if request.is_ajax:
		data = serializers.serialize("json",Unidad_modulo.objects.filter(id_modulo_unidad__in=Subquery(Modulo.objects.filter(nombre_modulo=request.GET.get('idNombre')).values('id_modulo'))))
		return JsonResponse(data,safe=False)

def updateUnidad(request):
	if request.is_ajax:
		updatedUnidad = Unidad_modulo.objects.filter(id_unidad = request.GET.get('idNombre')).update(nombre_unidad = request.GET.get('nombreUnidad'))
		return JsonResponse("Updated",safe=False)

def deleteAPES(request):
	if request.is_ajax:
		print(request.GET.get('aprendizajeActual'))
		deleteAPES = Aprendizaje_esperado_modulo.objects.filter(id = request.GET.get('aprendizajeEsperado').split('-')[1]).delete()
		return JsonResponse("deleted",safe=False)

def updateAPES(request):
	if request.is_ajax:
		updatedUnidad = Aprendizaje_esperado_modulo.objects.filter(id = request.GET.get('aprendizajeActual').split('-')[1]).update(aprendizaje_esperado = request.GET.get('aprendizajeNuevo'))
		return JsonResponse("Updated",safe=False)

def updPropUnidad(request):
	if request.is_ajax:
		updatedUnidad = Unidad_modulo.objects.filter(Q(id_unidad = request.GET.get('unidad')) & Q(id_modulo_unidad=request.GET.get('modulo'))).update(proposito_unidad = request.GET.get('proposito'))
		return JsonResponse("Updated proposito de la unidad",safe=False)

def updArchivo(request):
	if request.is_ajax:
		if request.method == 'POST':
			doc = request.FILES 
			updatedModulo = Modulo.objects.filter(id_modulo=request.POST.get('modulo')).update(pdf_modulo = request.FILES['archivo'])
			return JsonResponse("Updated pdf de la unidad",safe=False)

def getPropUnidad(request):
	if request.is_ajax:
		propUnidad = serializers.serialize("json",Unidad_modulo.objects.filter(Q(id_unidad = request.GET.get('unidad')) & Q(id_modulo_unidad=request.GET.get('modulo'))))
		return JsonResponse(propUnidad,safe=False)
		
'''
Fin de la sección de vistas para el control de módulos
''' 

#Función para realizar la entrega por parte del alumno

def entregaAlumno(request, id, idAlumno):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')

	c = 0
	Alumnos = Alumno.objects.all()
	ActividadDocente = Actividad_docente.objects.get(id_actividad = id)
	Entregas = Entrega_actividad.objects.filter(id_actividad = id)
	Archivos = Archivo.objects.filter(id_actividad = id)
	Cursos = Curso.objects.all()
	Modulos = Modulo.objects.all()
	try:
		Docentes = Docente.objects.filter(id_docente = idDocente)
	except:
		#Se debe de sacar el id_docente para hacer las inserciones
		#Se quiere obtener el id_docente haciendo la relacion con la actividad
		field_name = 'id_docente'
		obj = Actividad_docente.objects.get(id_actividad = id)
		field_value = getattr(obj, field_name)
		idDocente = field_value
		Docentes = Docente.objects.filter(id_docente = idDocente)
	
	try:
		Entrega = Entrega_actividad.objects.get(id_actividad = id, id_alumno = idAlumno)
		return render(request, 'entregaAlumno.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos, 'curso':Cursos, 'entregaA': Entrega })
	except:
		print('')
	if request.method == 'POST':
		nombreArchivos = ''
		try:
			idActividad = id
			#TODO: Realizar la actualización de archivos ya subidos
			#Ciclo para recorrer los archivos seleccionados y guardarlos (recursos)
			for afile in request.FILES.getlist('recursoAlumno'):
				#myfile = afile
				#fs = FileSystemStorage("media/TBC/Alumno")
				#filename = fs.save(myfile.name, myfile)
				#uploaded_file_url = fs.url(filename)
				nombreArchivos += afile.name + '\n'

				#Se obtiene el id del archivo actual para incrementar en 1 e insertarlo
				field_name = 'id_archivo'
				obj = Archivo.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1

				descripcion = request.POST.getlist('descRecurso')
				url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+afile.name
				ArchivoNuevo = Archivo(id_archivo = idArchivo, nombre_archivo = afile.name, descripcion = descripcion[c], tipo_archivo = 'Entrega', id_actividad = idActividad, url= url, id_alumno = idAlumno)
				ArchivoNuevo.archivo = afile
				ArchivoNuevo.save()
				c += 1
			comentario = request.POST['comentario']
			curso = request.POST['curso']
			date_joined = datetime.now()
			formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")	
			fechaHoraSubida = formatted_datetime
			nombreActividad = request.POST['nombreAct']
			#Para sacar el ultimo id registrado y sumarle 1
			# field_name = 'id_entrega'
			# obj = Entrega_actividad.objects.last()
			# field_value = getattr(obj, field_name)
			# idEntrega = field_value + 1
			EntregaNueva = Entrega_actividad(nombre_actividad = nombreActividad, fecha_hora_subida = fechaHoraSubida, id_alumno = idAlumno, id_actividad = id ,comentario = comentario, calificada = False, entregada = True)
			
			#TODO: Sólo insertar 1 registro al entregar una actividad, si ya existe no se inserta y solo se relaciona el alumno
			#Se obtiene el campo id_dc de la tabla de Docente_curso
			field_name = 'id_dc'
			obj = Docente_curso.objects.get(id_docente = idDocente, id_curso = curso)
			field_value = getattr(obj, field_name)
			idDc = field_value
			#Aqui ya se tienen los datos a insertar, se procede a comprobar si ya existe uno insertado
			notifI = Notificacion_act.objects.filter(id_dc = idDc, id_actividad = id, mensaje = 'Nueva entrega', tipo = 2).count()
			if notifI > 0:
				print('ya hay uno')
				field_name = 'id_notificacion'
				obj = Notificacion_act.objects.get(id_dc = idDc, id_actividad = id, tipo = 2)
				field_value = getattr(obj, field_name)
				idNotif = field_value
				print(idNotif)
				nuevaNotifD = Notificacion_act_docente(id_docente = idDocente, status = 0, id_notificacion = idNotif, id_alumno = idAlumno, id_dc = idDc, tipo = 2)
				
			else:
				notifAct = Notificacion_act(id_dc = idDc, id_actividad = id, mensaje = 'Nueva entrega', tipo = 2)
				notifAct.save()
				#Se inserta la notificación relacionandola al id de la notificacion
				#Se insertan los campos id_docente, id_notif y el id_alumno
				field_name = 'id_notificacion'
				obj = Notificacion_act.objects.last()
				field_value = getattr(obj, field_name)
				idNotif = field_value
				print(idNotif)
				nuevaNotifD = Notificacion_act_docente(id_docente = idDocente, status = 0, id_notificacion = idNotif, id_alumno = idAlumno, id_dc = idDc, tipo = 2)
			
			#Se actualiza la notificación de actividadNueva y ponerla en leída
			#Se saca el id de la notificacion (tabla notif_act_alumno) correspondiente a actualizar con el id_dc y el id_actividad (tabla notifi_act)
			field_name = 'id_notificacion'
			obj = Notificacion_act.objects.get(id_actividad = id, tipo = 1)
			field_value = getattr(obj, field_name)
			idNotificacion = field_value
			NotifStatus = Notificacion_act_alumno.objects.filter(id_alumno = idAlumno, id_notificacion = idNotificacion).update(status = 1)
			
			#No existen errores, se proceden a guardar
			EntregaNueva.save()
			nuevaNotifD.save()
			sweetify.success(request, 'Se entregó', text='La actividad fue entregada exitosamente', persistent='Ok', icon="success")
		except Exception as e:
			print(e)
			sweetify.error(request, 'No se entregó', text='Ocurrió un error', persistent='Ok', icon="error")
		return redirect('/TBC/actividad-alumno/'+str(idAlumno))

	return render(request, 'entregaAlumno.html', {'usuario':usuarioLogueado, 'actividad':ActividadDocente, 'docente':Docentes, 'alumno':Alumnos, 'entrega':Entregas , 'archivo':Archivos, 'curso':Cursos, 'modulo':Modulos })#'entregaA':Entrega}) 

#Función para relacionar un módulo con un docente y ese módulo-docente con un grupo de alumnos (por semestres)

def relacionarModulo(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	Docentes = Docente.objects.filter(cct = usuarioLogueado.last_name)
	Alumnos = Alumno.objects.filter(cct = usuarioLogueado.last_name)
	Modulos = Modulo.objects.all()
	DocenteModulo = Docente_curso.objects.all()
	# cct del logincustomuser = last_name print(usuarioLogueado.last_name) TODO: Cambiar a la relación que tenga Diana al dar de alta la institución
	#Para relacionar un módulo con un docente
	if request.method == 'POST':
		bandera = request.POST['bandera']
		#False para relacionar módulo con un docente
		if bandera == 'False':
			try:
				idDocente = request.POST['docente']
				idModulo = request.POST['modulo']
				print('x', idModulo, idDocente)
				try:
					field_name = 'id_dc'
					obj = Docente_curso.objects.last()
					field_value = getattr(obj, field_name)
					id_Dc = field_value + 1
				except:
					id_Dc = 1
				nuevoDocenteMod = Docente_curso(id_dc = id_Dc, id_curso = idModulo, id_docente = idDocente)
				nuevoDocenteMod.save()
				sweetify.success(request, 'Relación realizada', text='El docente fue relacionado al módulo seleccionado', persistent='Ok', icon="success")
			except Exception as e:
				print(e)
		elif bandera == 'True':
			#True para relacionar alumnos con un modulo-docente
			alumnosL = request.POST.getlist('nombreAlumnoTabla') or None
			id_alumnoL = request.POST.getlist('id_alumnoL') or None
			idDocMod = request.POST['docenteModulo']
			idx = 0
			for al in alumnosL:
				if not request.POST.get('alumnoModulo'+str(idx)):
					cursando = False
				else:
					cursando = True
				#Se recorren los alumnos que están en la tabla ya obteniendo si está checkeado el checkbox o no
				#print('id del curso: ', idDocMod)
				#print(id_alumnoL[idx], ' - ', cursando)
				#Se guarda en la tabla alumnoCurso
				try:
					field_name = 'id_ac'
					obj = Alumno_curso.objects.last()
					field_value = getattr(obj, field_name)
					id_Ac = field_value + 1
				except:
					id_Ac = 1
				#Insertar solo los que sean cursando = True
				if cursando == True:
					try:
						nuevoAlCurso = Alumno_curso(id_ac = id_Ac, id_dc = idDocMod, id_alumno = id_alumnoL[idx] )
						nuevoAlCurso.save()
						print('insertao segun', id_alumnoL[idx])
						sweetify.success(request, 'Relación realizada', text='Los alumnos fueron relacionado al módulo seleccionado', persistent='Ok', icon="success")
					except:
						sweetify.error(request, 'No se realizó la operación', text='Ocurrió un error', persistent='Ok', icon="error")
				else:
					print('')
				idx += 1

	return render(request, 'relacionarModulo.html', {'usuario':usuarioLogueado, 'docente':Docentes, 'modulo':Modulos, 'alumno':Alumnos, 'docenteModulo':DocenteModulo }) 

'''
Incicia sección de vistas de prueba TODO: Eliminarlas al final
'''
def generarCertificado(request):
	alumno = Alumno.objects.all()
	alumnoS = Alumno.objects.filter(id_alumno=1)
	return render(request, 'generarCertificado.html', {'alumno':alumno, 'alumnoS':alumnoS})

def materialDidactico(request):
	return render(request, 'materialDidactico.html', {})

def estadistica(request):
	return render(request, 'estadistica.html', {})

'''
Fin de la ección de vistas de prueba TODO: Eliminarlas al final
'''

#Fin de Vistas de sección de vistas de la primer versión

#Comienza sección de vistas de la segunda versión

#Función para que el docente suba el archivo de la información estadística con formato ya establecido
def subirEstadistica(request):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user

	#Si el usuario logeado es un docente tipo_usuario = 6, entonces se procede a asignar el idDocente correspondiente
	if usuarioLogueado.tipo_usuario == '6':
		try:
			#Para sacar el idDocente de la tabla de tbc con base en el registro CustomUser
			field_name = 'id_docente'
			obj = Docente.objects.get(email = request.user.email) #TODO: Cambiar last_name ya que se la haya dado más espacio
			field_value = getattr(obj, field_name)
			idDocente = field_value
		except:
			print('')
	
	#Si el usuario logeado es un alumno tipo_usuario = 7, entonces se procede a asignar el idAlumno correspondiente
	if usuarioLogueado.tipo_usuario == '7':
		try:
			#Para sacar el idAlumno de la tabla de tbc con base en el registro de CustomUser
			field_name = 'id_alumno'
			obj = Alumno.objects.get(email = request.user.email) #TODO:Cambiar last_name ya que se le haya dado más espacio
			field_value = getattr(obj, field_name)
			idAlumnoI = field_value
		except:
			print('')
	Modulos = Modulo.objects.all()
	Docentes = Docente.objects.all()
	Archivo_e = Archivo_estadistica.objects.filter(tipo_archivo='estadistica').order_by('id_archivo_estadistica')
	if request.method == 'POST':
		fecha = request.POST['fecha']
		nombre_archivo = request.POST['nombreArchivo']
		try:
			archivo = request.FILES['archivo']
			try:
				field_name = 'id_archivo_estadistica'
				obj = Archivo_estadistica.objects.last()
				field_value = getattr(obj, field_name)
				idArchivo = field_value + 1
			except:
				idArchivo = 1
			url = 'https://storage.googleapis.com/plataformase.appspot.com/TBC/archivos/'+archivo.name #'/media/TBC/Datos/Alumnos/'+archivo.name
			nuevoArchivo = Archivo_estadistica(id_archivo_estadistica = idArchivo, nombre_archivo = nombre_archivo, nombre_archivoL = archivo.name, tipo_archivo = 'estadistica', url = url, id_docente = idDocente, fecha = fecha)
			nuevoArchivo.archivo = archivo
			nuevoArchivo.save()
		except:
			print('error al importar archivo')
		
	return render(request, 'subirEstadistica.html', { 'usuario':usuarioLogueado, 'modulo':Modulos, 'docente':Docentes, 'archivoEstadistica':Archivo_e })

#Funcion para mostrar cuando inicie sesión un alumno
def alumno(request, id):
	if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
	usuarioLogueado = request.user
	Modulos = Modulo.objects.all()
	Asignaturas = Asignatura.objects.all().order_by('id_asignatura')
	AlumnoS = Alumno.objects.get(id_alumno = id)
	Estadistica_alumno = Estadistica_modulo.objects.get(num_matricula = usuarioLogueado.first_name)
	ArchivoSubsistema = ['-']
	try:
		ArchivoSubsistemaA = Archivo.objects.get(id_alumno = id, tipo_archivo='Subsistema')
		ArchivoSubsistema.append(ArchivoSubsistemaA.tipo_archivo)
	except:
		ArchivoSubsistemaA = None
	Archivos = Archivo.objects.filter(id_alumno = id)

	#Se llama la función para generar los reportes declarando antes las variables a usar
	totalAlumnos = 0
	labels, data, labels2, data2, auxData3, auxLabels3 = [], [], [], [], [], []
	labels, data, labels2, data2, auxData3, auxLabels3, totalAlumnos = generar_reporteA(labels, data, labels2, data2, auxData3, auxLabels3, Estadistica_alumno, Modulos, totalAlumnos, Asignaturas)

	return render(request, 'alumno.html', { 'usuario':usuarioLogueado, 'modulo':Modulos, 'alumnoSel':AlumnoS, 'estadistica':Estadistica_alumno, 'labels':labels, 'data':data, 'labels2':labels2, 'data2':data2, 'archivoSubsistema':ArchivoSubsistema, 'archivos':Archivos})	

#Función para generar los reportes
def generar_reporteA(labels, data, labels2, data2, auxData3, auxLabels3, Estadistica_modulos, Modulos, totalAlumnos, Asignaturas):	
	#Para generar un reporte por módulos de manera general
	labels = []
	data = []
	try:
		size = len(Estadistica_modulos)
		if size == 0:
			size = 1
	except:
		size = 1
	#Para generar los promedios por modulos, se declaran variables para la suma y promedio de cada asignatura (32)
	#TODO:Analizar cambiarlos por arreglos y/o del modelo traido de la bd de los modelos (añadir clave de campo) no c pudo
	sum_mat1 = sum_fis1 = sum_ev1 = sum_met_inv = sum_tlr1 = sum_ing1 = sum_mat2 = sum_fis2 = sum_ev2 = sum_ics = sum_tlr2 = sum_ing2 = sum_mat3 = sum_q1 = sum_bio1 = sum_hm1 = sum_lit1 = sum_ing3 = sum_sft1 = sum_mat4 = sum_q2 = sum_bio2 = sum_hm2 = sum_lit2 = sum_ing4 = sum_sft2 = sum_geog = sum_huc = sum_cdemyce = sum_cdecsyh = sum_cdec = sum_sft3 = sum_filos = sum_ema = sum_met_invx = sum_derech2 = sum_cc2 = sum_cs2 = sum_proyes2 =  0
	prom_mat1 = prom_fis1 = prom_ev1 = prom_met_inv = prom_tlr1 = prom_ing1 = prom_mat2 = prom_fis2 = prom_ev2 = prom_ics = prom_tlr2 = prom_ing2 = prom_mat3 = prom_q1 = prom_bio1 = prom_hm1 = prom_lit1 = prom_ing3 = prom_sft1 = prom_mat4 = prom_q2 = prom_bio2 = prom_hm2 = prom_lit2 = prom_ing4 = prom_sft2 = prom_geog = prom_huc = prom_cdemyce = prom_cdecsyh = prom_cdec = prom_sft3 = prom_filos = prom_ema = prom_met_invx = prom_derech2 = prom_cc2 = prom_cs2 = prom_proyes2 =  0
	#Se acumulan los promedios por cada asignatura
	#for e in Estadistica_modulos:
	if Estadistica_modulos.prom_mat1 == None: Estadistica_modulos.prom_mat1 = 0  
	prom_mat1 = float(Estadistica_modulos.prom_mat1)
	if Estadistica_modulos.prom_fis1 == None: Estadistica_modulos.prom_fis1 = 0  
	prom_fis1 = float(Estadistica_modulos.prom_fis1)
	if Estadistica_modulos.prom_ev1 == None: Estadistica_modulos.prom_ev1 = 0  
	prom_ev1 = float(Estadistica_modulos.prom_ev1)
	if Estadistica_modulos.prom_met_inv == None: Estadistica_modulos.prom_met_inv = 0  
	prom_met_inv = float(Estadistica_modulos.prom_met_inv)
	if Estadistica_modulos.prom_tlr1 == None: Estadistica_modulos.prom_tlr1 = 0  
	prom_tlr1 = float(Estadistica_modulos.prom_tlr1)
	if Estadistica_modulos.prom_ing1 == None: Estadistica_modulos.prom_ing1 = 0  
	prom_ing1 = float(Estadistica_modulos.prom_ing1)
	if Estadistica_modulos.prom_mat2 == None: Estadistica_modulos.prom_mat2 = 0  
	prom_mat2 = float(Estadistica_modulos.prom_mat2)
	if Estadistica_modulos.prom_fis2 == None: Estadistica_modulos.prom_fis2 = 0  
	prom_fis2 = float(Estadistica_modulos.prom_fis2)
	if Estadistica_modulos.prom_ev2 == None: Estadistica_modulos.prom_ev2 = 0  
	prom_ev2 = float(Estadistica_modulos.prom_ev2)
	if Estadistica_modulos.prom_ics == None: Estadistica_modulos.prom_ics = 0    
	prom_ics = float(Estadistica_modulos.prom_ics)
	if Estadistica_modulos.prom_tlr2 == None: Estadistica_modulos.prom_tlr2 = 0  
	prom_tlr2 = float(Estadistica_modulos.prom_tlr2)
	if Estadistica_modulos.prom_ing2 == None: Estadistica_modulos.prom_ing2 = 0  
	prom_ing2 = float(Estadistica_modulos.prom_ing2)
	if Estadistica_modulos.prom_mat3 == None: Estadistica_modulos.prom_mat3 = 0  
	prom_mat3 = float(Estadistica_modulos.prom_mat3)
	if Estadistica_modulos.prom_q1 == None: Estadistica_modulos.prom_q1 = 0  
	prom_q1 = float(Estadistica_modulos.prom_q1)
	if Estadistica_modulos.prom_bio1 == None: Estadistica_modulos.prom_bio1 = 0  
	prom_bio1 = float(Estadistica_modulos.prom_bio1)
	if Estadistica_modulos.prom_hm1 == None: Estadistica_modulos.prom_hm1 = 0  
	prom_hm1 = float(Estadistica_modulos.prom_hm1)
	if Estadistica_modulos.prom_lit1 == None: Estadistica_modulos.prom_lit1 = 0  
	prom_lit1 = float(Estadistica_modulos.prom_lit1)
	if Estadistica_modulos.prom_ing3 == None: Estadistica_modulos.prom_ing3 = 0  
	prom_ing3 = float(Estadistica_modulos.prom_ing3)
	if Estadistica_modulos.prom_sft1 == None: Estadistica_modulos.prom_sft1 = 0  
	prom_sft1 = float(Estadistica_modulos.prom_sft1)
	if Estadistica_modulos.prom_mat4 == None: Estadistica_modulos.prom_mat4 = 0  
	prom_mat4 = float(Estadistica_modulos.prom_mat4)
	if Estadistica_modulos.prom_q2 == None: Estadistica_modulos.prom_q2 = 0  
	prom_q2 = float(Estadistica_modulos.prom_q2)
	if Estadistica_modulos.prom_bio2 == None: Estadistica_modulos.prom_bio2 = 0  
	prom_bio2 = float(Estadistica_modulos.prom_bio2)
	if Estadistica_modulos.prom_hm2 == None: Estadistica_modulos.prom_hm2 = 0  
	prom_hm2 = float(Estadistica_modulos.prom_hm2)
	if Estadistica_modulos.prom_lit2 == None: Estadistica_modulos.prom_lit2 = 0 
	prom_lit2 = float(Estadistica_modulos.prom_lit2)
	if Estadistica_modulos.prom_ing4 == None: Estadistica_modulos.prom_ing4 = 0 
	prom_ing4 = float(Estadistica_modulos.prom_ing4)
	if Estadistica_modulos.prom_sft2 == None: Estadistica_modulos.prom_sft2 = 0 
	prom_sft2 = float(Estadistica_modulos.prom_sft2)
	if Estadistica_modulos.prom_geog == None: Estadistica_modulos.prom_geog = 0  
	prom_geog = float(Estadistica_modulos.prom_geog)
	if Estadistica_modulos.prom_huc == None: Estadistica_modulos.prom_huc = 0 
	prom_huc = float(Estadistica_modulos.prom_huc)
	if Estadistica_modulos.prom_cdemyce == None: Estadistica_modulos.prom_cdemyce = 0  
	prom_cdemyce = float(Estadistica_modulos.prom_cdemyce)
	if Estadistica_modulos.prom_cdecsyh == None: Estadistica_modulos.prom_cdecsyh = 0 
	prom_cdecsyh = float(Estadistica_modulos.prom_cdecsyh)
	if Estadistica_modulos.prom_cdec == None: Estadistica_modulos.prom_cdec = 0 
	prom_cdec = float(Estadistica_modulos.prom_cdec)
	if Estadistica_modulos.prom_sft3 == None: Estadistica_modulos.prom_sft3 = 0 
	prom_sft3 = float(Estadistica_modulos.prom_sft3)
	if Estadistica_modulos.prom_filos == None: Estadistica_modulos.prom_filos = 0 
	prom_filos = float(Estadistica_modulos.prom_filos)
	if Estadistica_modulos.prom_ema == None: Estadistica_modulos.prom_ema = 0 
	prom_ema = float(Estadistica_modulos.prom_ema)
	if Estadistica_modulos.prom_met_invx == None: Estadistica_modulos.prom_met_invx = 0
	prom_met_invx = float(Estadistica_modulos.prom_met_invx)
	if Estadistica_modulos.prom_derech2 == None: Estadistica_modulos.prom_derech2 = 0
	prom_derech2 = float(Estadistica_modulos.prom_derech2)
	if Estadistica_modulos.prom_cc2 == None: Estadistica_modulos.prom_cc2 = 0 
	prom_cc2 = float(Estadistica_modulos.prom_cc2)
	if Estadistica_modulos.prom_cs2 == None: Estadistica_modulos.prom_cs2 = 0  
	prom_cs2 = float(Estadistica_modulos.prom_cs2)
	if Estadistica_modulos.prom_proyes2 == None: Estadistica_modulos.prom_proyes2 = 0  
	prom_proyes2 = float(Estadistica_modulos.prom_proyes2)
	#data contiene todos los promedios de todas las asignaturas
	data = [prom_mat1,  prom_fis1,  prom_ev1,  prom_met_inv,  prom_tlr1,  prom_ing1,  prom_mat2,  prom_fis2,  prom_ev2, prom_ics, prom_tlr2,  prom_ing2,  prom_mat3,  prom_q1,  prom_bio1,  prom_hm1,  prom_lit1,  prom_ing3,  prom_sft1,  prom_mat4,  prom_q2,  prom_bio2,  prom_hm2,  prom_lit2,  prom_ing4,  prom_sft2,  prom_geog,  prom_huc,  prom_cdemyce,  prom_cdecsyh,  prom_cdec,  prom_sft3,  prom_filos,  prom_ema,  prom_met_invx,  prom_derech2,  prom_cc2,  prom_cs2,  prom_proyes2]
	#Para acomodar las asignaturas x modulo
	mod1 = (prom_mat1 + prom_fis1)/2
	mod2 = (prom_ev1 + prom_met_inv)/2
	mod3 = (prom_tlr1 + prom_ing1)/2
	mod4 = (prom_mat2 + prom_fis2)/2
	mod5 = (prom_ev2 + prom_ics)/2
	mod6 = (prom_tlr2 + prom_ing2)/2
	mod7 = (prom_mat3 + prom_q1 + prom_bio1)/3
	mod8 = prom_hm1
	mod9 = (prom_lit1 + prom_ing3)/2
	mod10 = prom_sft1
	mod11 = (prom_mat4 + prom_q2 + prom_bio2)/3
	mod12 = prom_hm2
	mod13 = (prom_lit2 + prom_ing4)/2
	mod14 = prom_sft2
	mod15 = prom_geog
	mod16 = prom_huc
	mod17 = prom_cdemyce
	mod18 = prom_cdecsyh
	mod19 = prom_cdec
	mod20 = prom_sft3
	#data ahora contiene todos los promedios de todos los modulos
	data = [mod1, mod2, mod3, mod4, mod5, mod6, mod7, mod8, mod9, mod10, mod11, mod12, mod13, mod14, mod15, mod16, mod17, mod18, mod19, mod20]
	for mod in Modulos:
		labels.append(mod.nombre_modulo)
	#Para generar reporte por módulos, almacenar las calificaciones de cada modulo y sacar datos correspondientes a ponderación de [0-5, 6, 7, 8, 9, 10] (estos serán los labels)
	#labels2 = ['0-5', 6, 7, 8, 9, 10]
	for asi in Asignaturas:
		labels2.append(asi.nombre_asignatura)
	mat1, fis1, ev1, met_inv, tlr1, ing1, mat2, fis2, ev2, ics ,tlr2, ing2, mat3, q1, bio1, hm1, lit1, ing3, sft1, mat4, q2, bio2, hm2, lit2, ing4, sft2, geog, huc, cdemyce, cdecsyh, cdec, sft3, filos, ema, met_invx, derech2, cc2, cs2, proyes2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	#Se almacenan todas los promedios
	#for e in Estadistica_modulos:
	if Estadistica_modulos.prom_mat1 == None: Estadistica_modulos.prom_mat1 = 0
	mat1 = float(Estadistica_modulos.prom_mat1)
	if Estadistica_modulos.prom_fis1 == None: Estadistica_modulos.prom_fis1 = 0 
	fis1 = float(Estadistica_modulos.prom_fis1)
	if Estadistica_modulos.prom_ev1 == None: Estadistica_modulos.prom_ev1 = 0  
	ev1 = float(Estadistica_modulos.prom_ev1)
	if Estadistica_modulos.prom_met_inv == None: Estadistica_modulos.prom_met_inv = 0
	met_inv = float(Estadistica_modulos.prom_met_inv)
	if Estadistica_modulos.prom_tlr1 == None: Estadistica_modulos.prom_tlr1 = 0 
	tlr1 = float(Estadistica_modulos.prom_tlr1)
	if Estadistica_modulos.prom_ing1 == None: Estadistica_modulos.prom_ing1 = 0 
	ing1 = float(Estadistica_modulos.prom_ing1)
	if Estadistica_modulos.prom_mat2 == None: Estadistica_modulos.prom_mat2 = 0 
	mat2 = float(Estadistica_modulos.prom_mat2)
	if Estadistica_modulos.prom_fis2 == None: Estadistica_modulos.prom_fis2 = 0  
	fis2 = float(Estadistica_modulos.prom_fis2)
	if Estadistica_modulos.prom_ev2 == None: Estadistica_modulos.prom_ev2 = 0  
	ev2 = float(Estadistica_modulos.prom_ev2)
	if Estadistica_modulos.prom_ics == None: Estadistica_modulos.prom_ics = 0   
	ics = float(Estadistica_modulos.prom_ics)
	if Estadistica_modulos.prom_tlr2 == None: Estadistica_modulos.prom_tlr2 = 0
	tlr2 = float(Estadistica_modulos.prom_tlr2)
	if Estadistica_modulos.prom_ing2 == None: Estadistica_modulos.prom_ing2 = 0 
	ing2 = float(Estadistica_modulos.prom_ing2)
	if Estadistica_modulos.prom_mat3 == None: Estadistica_modulos.prom_mat3 = 0
	mat3 = float(Estadistica_modulos.prom_mat3)
	if Estadistica_modulos.prom_q1 == None: Estadistica_modulos.prom_q1 = 0 
	q1 = float(Estadistica_modulos.prom_q1)
	if Estadistica_modulos.prom_bio1 == None: Estadistica_modulos.prom_bio1 = 0 
	bio1 = float(Estadistica_modulos.prom_bio1)
	if Estadistica_modulos.prom_hm1 == None: Estadistica_modulos.prom_hm1 = 0 
	hm1 = float(Estadistica_modulos.prom_hm1)
	if Estadistica_modulos.prom_lit1 == None: Estadistica_modulos.prom_lit1 = 0
	lit1 = float(Estadistica_modulos.prom_lit1)
	if Estadistica_modulos.prom_ing3 == None: Estadistica_modulos.prom_ing3 = 0
	ing3 = float(Estadistica_modulos.prom_ing3)
	if Estadistica_modulos.prom_sft1 == None: Estadistica_modulos.prom_sft1 = 0 
	sft1 = float(Estadistica_modulos.prom_sft1)
	if Estadistica_modulos.prom_mat4 == None: Estadistica_modulos.prom_mat4 = 0 
	mat4 = float(Estadistica_modulos.prom_mat4)
	if Estadistica_modulos.prom_q2 == None: Estadistica_modulos.prom_q2 = 0 
	q2 = float(Estadistica_modulos.prom_q2)
	if Estadistica_modulos.prom_bio2 == None: Estadistica_modulos.prom_bio2 = 0 
	bio2 = float(Estadistica_modulos.prom_bio2)
	if Estadistica_modulos.prom_hm2 == None: Estadistica_modulos.prom_hm2 = 0  
	hm2 = float(Estadistica_modulos.prom_hm2)
	if Estadistica_modulos.prom_lit2 == None: Estadistica_modulos.prom_lit2 = 0
	lit2 = float(Estadistica_modulos.prom_lit2)
	if Estadistica_modulos.prom_ing4 == None: Estadistica_modulos.prom_ing4 = 0 
	ing4 = float(Estadistica_modulos.prom_ing4)
	if Estadistica_modulos.prom_sft2 == None: Estadistica_modulos.prom_sft2 = 0
	sft2 = float(Estadistica_modulos.prom_sft2)
	if Estadistica_modulos.prom_geog == None: Estadistica_modulos.prom_geog = 0
	geog = float(Estadistica_modulos.prom_geog)
	if Estadistica_modulos.prom_huc == None: Estadistica_modulos.prom_huc = 0 
	huc = float(Estadistica_modulos.prom_huc)
	if Estadistica_modulos.prom_cdemyce == None: Estadistica_modulos.prom_cdemyce = 0
	cdemyce = float(Estadistica_modulos.prom_cdemyce)
	if Estadistica_modulos.prom_cdecsyh == None: Estadistica_modulos.prom_cdecsyh = 0
	cdecsyh = float(Estadistica_modulos.prom_cdecsyh)
	if Estadistica_modulos.prom_cdec == None: Estadistica_modulos.prom_cdec = 0 
	cdec = float(Estadistica_modulos.prom_cdec)
	if Estadistica_modulos.prom_sft3 == None: Estadistica_modulos.prom_sft3 = 0 
	sft3 = float(Estadistica_modulos.prom_sft3)
	if Estadistica_modulos.prom_filos == None: Estadistica_modulos.prom_filos = 0 
	filos = float(Estadistica_modulos.prom_filos)
	if Estadistica_modulos.prom_ema == None: Estadistica_modulos.prom_ema = 0 
	ema = float(Estadistica_modulos.prom_ema)
	if Estadistica_modulos.prom_met_invx == None: Estadistica_modulos.prom_met_invx = 0
	met_invx = float(Estadistica_modulos.prom_met_invx)
	if Estadistica_modulos.prom_derech2 == None: Estadistica_modulos.prom_derech2 = 0
	derech2 = float(Estadistica_modulos.prom_derech2)
	if Estadistica_modulos.prom_cc2 == None: Estadistica_modulos.prom_cc2 = 0 
	cc2 = float(Estadistica_modulos.prom_cc2)
	if Estadistica_modulos.prom_cs2 == None: Estadistica_modulos.prom_cs2 = 0 
	cs2 = float(Estadistica_modulos.prom_cs2)
	if Estadistica_modulos.prom_proyes2 == None: Estadistica_modulos.prom_proyes2 = 0
	proyes2 = float(Estadistica_modulos.prom_proyes2)
	#Se procede a buscar en el arreglo y llevar conteo de cuantos pertenecen a la ponderación [0-5, 6, 7, 8, 9, 10]
	f = s = sv = e = n = t = 0 #[0-5, 6, 7, 8, 9, 10]
	#Se genera el total de alumnos por institución
	totalAlumnos = 1
	#Se acomodan los modulos respecto a sus asignaturas
	#modM1 = mat1 + fis1
	modM1, modM2, modM3, modM4, modM5, modM6, modM7, modM8, modM9, modM10, modM11, modM12, modM13, modM14, modM15, modM16, modM17, modM18, modM19, modM20,  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
	modM1.append(mat1)
	modM1.append(fis1)
	modM2.append(ev1)
	modM2.append(met_inv)
	modM3.append(tlr1)
	modM3.append(ing1)
	modM4.append(mat2)
	modM4.append(fis2)
	modM5.append(ev2)
	modM5.append(ics)
	modM6.append(tlr2)
	modM6.append(ing2)
	modM7.append(mat3)
	modM7.append(q1)
	modM7.append(bio1)
	modM8.append(hm1)
	modM9.append(lit1)
	modM9.append(ing3)
	modM10.append(sft1)
	modM11.append(mat4)
	modM11.append(q2)
	modM11.append(bio2)
	modM12.append(hm2)
	modM13.append(lit2)
	modM13.append(ing4)
	modM14.append(sft2)
	modM15.append(geog)
	modM16.append(huc)
	modM17.append(cdemyce)
	modM18.append(cdecsyh)
	modM19.append(cdec)
	modM20.append(sft3)
	#arr contendrá los arreglos de todos los prmedios por modMulo i.e -> modM1[6,7,8.2,9,5,1,2,3]
	data2 = []
	data2 = [modM1, modM2, modM3, modM4, modM5, modM6, modM7, modM8, modM9, modM10, modM11, modM12, modM13, modM14, modM15, modM16, modM17, modM18, modM19, modM20]
	return labels, data, labels2, data2, auxData3, auxLabels3, totalAlumnos