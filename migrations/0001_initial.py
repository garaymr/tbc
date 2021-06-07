# Generated by Django 3.0.6 on 2020-09-17 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad_docente',
            fields=[
                ('id_actividad', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_actividad', models.CharField(max_length=400)),
                ('unidad', models.IntegerField()),
                ('tipo_actividad', models.CharField(max_length=200)),
                ('tema', models.CharField(max_length=200)),
                ('subtema', models.CharField(max_length=200)),
                ('objetivo', models.CharField(max_length=500)),
                ('recurso', models.FileField(upload_to='Archivos/TBC')),
                ('rubrica', models.FileField(upload_to='Archivos/TBC')),
                ('valor_parcial', models.IntegerField()),
                ('fecha_hora_limite', models.CharField(max_length=50)),
                ('fechaAct', models.CharField(max_length=200)),
                ('id_docente', models.IntegerField()),
                ('id_curso', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id_alumno', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_escuela', models.CharField(max_length=150)),
                ('cct', models.CharField(max_length=50)),
                ('nombre_alumno', models.CharField(max_length=150)),
                ('num_matricula', models.CharField(max_length=150)),
                ('curp_alumno', models.CharField(max_length=20)),
                ('mat1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat1pr', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_mat1', models.CharField(max_length=20, null=True)),
                ('q1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('q1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('q1p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_q1', models.CharField(max_length=20, null=True)),
                ('evp1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('evp2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('evp3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ev1', models.CharField(max_length=20, null=True)),
                ('icsp1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('icsp2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('icsp3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_icsp', models.CharField(max_length=20, null=True)),
                ('tlrp1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('tlrp2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('tlrp3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_tlr1', models.CharField(max_length=20, null=True)),
                ('lae1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae1p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_lae1', models.CharField(max_length=20, null=True)),
                ('app1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('app2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('app3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap1', models.CharField(max_length=20, null=True)),
                ('prom_general_1', models.CharField(max_length=20, null=True)),
                ('periodo2', models.CharField(max_length=20, null=True)),
                ('semestre2', models.CharField(max_length=20, null=True)),
                ('mat2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_mat2', models.CharField(max_length=20, null=True)),
                ('q2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('q2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('q2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_q2', models.CharField(max_length=20, null=True)),
                ('ev2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ev2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ev2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ev2', models.CharField(max_length=20, null=True)),
                ('hmi1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('hmi2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('hmi3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_hmi', models.CharField(max_length=20, null=True)),
                ('tlr2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('tlr2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('tlr2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_tlr2', models.CharField(max_length=20, null=True)),
                ('lae2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_lae2', models.CharField(max_length=20, null=True)),
                ('ap2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap2', models.CharField(max_length=20, null=True)),
                ('promedio_general_2', models.CharField(max_length=20, null=True)),
                ('ciclo_escolar_2', models.CharField(max_length=20, null=True)),
                ('periodo_3', models.CharField(max_length=20, null=True)),
                ('semestre_3', models.CharField(max_length=20, null=True)),
                ('mat3p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat3p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat3p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_mat3', models.CharField(max_length=20, null=True)),
                ('bio1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('bio1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('bio1p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_bio1', models.CharField(max_length=20, null=True)),
                ('fis1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('fis1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('fis1p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_fis1', models.CharField(max_length=20, null=True)),
                ('hmiip1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('hmiip2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('hmiip3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_hmii', models.CharField(max_length=20, null=True)),
                ('litip1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('litip2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('litip3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_liti', models.CharField(max_length=20, null=True)),
                ('lae3p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae3p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae3p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_lae3', models.CharField(max_length=20, null=True)),
                ('dc1p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc1p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc1p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_dc1', models.CharField(max_length=20, null=True)),
                ('ap3p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap3p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap3p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap3', models.CharField(max_length=20, null=True)),
                ('promedio_general_3', models.CharField(max_length=20, null=True)),
                ('periodo_4', models.CharField(max_length=20, null=True)),
                ('semestre_4', models.CharField(max_length=20, null=True)),
                ('mat4p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat4p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('mat4p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_mat4', models.CharField(max_length=20, null=True)),
                ('bio2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('bio2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('bio2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_bio2', models.CharField(max_length=20, null=True)),
                ('fis2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('fis2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('fis2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_fis2', models.CharField(max_length=20, null=True)),
                ('esmp1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('esmp2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('esmp3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_esm', models.CharField(max_length=20, null=True)),
                ('lit2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lit2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lit2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_lit2', models.CharField(max_length=20, null=True)),
                ('lae4p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae4p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('lae4p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_lae4', models.CharField(max_length=20, null=True)),
                ('dc2p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc2p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc2p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_dc2', models.CharField(max_length=20, null=True)),
                ('ap4p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap4p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap4p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap4', models.CharField(max_length=20, null=True)),
                ('promedio_general_4', models.CharField(max_length=20, null=True)),
                ('periodo_5', models.CharField(max_length=20, null=True)),
                ('semestre_5', models.CharField(max_length=20, null=True)),
                ('geog1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('geog2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('geog3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_geog', models.CharField(max_length=20, null=True)),
                ('huc1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('huc2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('huc3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_huc', models.CharField(max_length=20, null=True)),
                ('derech1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('derech2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('derech3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_derech', models.CharField(max_length=20, null=True)),
                ('cc1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cc2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cc3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_cc', models.CharField(max_length=20, null=True)),
                ('cs1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cs2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cs3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_cs', models.CharField(max_length=20, null=True)),
                ('proyes1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('proyes2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('proyes3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_proyes', models.CharField(max_length=20, null=True)),
                ('dc3p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc3p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc3p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_dc3', models.CharField(max_length=20, null=True)),
                ('ap5p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap5p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap5p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap5', models.CharField(max_length=20, null=True)),
                ('promedio_general_5', models.CharField(max_length=20, null=True)),
                ('periodo_6', models.CharField(max_length=20, null=True)),
                ('semestre_6', models.CharField(max_length=20, null=True)),
                ('filos1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('filos2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('filos3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_filos', models.CharField(max_length=20, null=True)),
                ('ema1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ema2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ema3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ema', models.CharField(max_length=20, null=True)),
                ('met_inv1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('met_inv2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('met_inv3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_met_inv', models.CharField(max_length=20, null=True)),
                ('derech16', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('derech27', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('derech38', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_derech2', models.CharField(max_length=20, null=True)),
                ('cc19', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cc210', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cc311', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_cc2', models.CharField(max_length=20, null=True)),
                ('cs112', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cs213', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('cs314', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_cs2', models.CharField(max_length=20, null=True)),
                ('proyes115', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('proyes216', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('proyes317', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_proyes2', models.CharField(max_length=20, null=True)),
                ('dc3p118', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc3p219', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('dc3p320', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_dc4', models.CharField(max_length=20, null=True)),
                ('ap6p1', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap6p2', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('ap6p3', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('prom_ap6', models.CharField(max_length=20, null=True)),
                ('promedio_general_6', models.CharField(max_length=20, null=True)),
                ('promedio_final', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('tel_fijo', models.CharField(max_length=150, null=True)),
                ('tel_celular', models.CharField(max_length=150, null=True)),
                ('calle', models.CharField(max_length=150, null=True)),
                ('colonia', models.CharField(max_length=150, null=True)),
                ('num_int', models.CharField(max_length=150, null=True)),
                ('num_ext', models.CharField(max_length=150, null=True)),
                ('semestre', models.CharField(max_length=150)),
                ('tipo_secundaria', models.CharField(max_length=150, null=True)),
                ('acta_nacimiento', models.FileField(null=True, upload_to='Archivos/TBC')),
                ('curp_archivo', models.FileField(null=True, upload_to='Archivos/TBC')),
                ('certificado_secundaria', models.FileField(null=True, upload_to='Archivos/TBC')),
            ],
        ),
        migrations.CreateModel(
            name='Alumno_curso',
            fields=[
                ('id_ac', models.AutoField(primary_key=True, serialize=False)),
                ('id_dc', models.IntegerField()),
                ('id_alumno', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id_archivo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_archivo', models.CharField(max_length=500)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='TBC/archivos')),
                ('descripcion', models.CharField(max_length=500, null=True)),
                ('tipo_archivo', models.CharField(max_length=100)),
                ('id_actividad', models.IntegerField(null=True)),
                ('url', models.CharField(max_length=500)),
                ('id_alumno', models.IntegerField(null=True)),
                ('id_docente', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Area_disciplinar',
            fields=[
                ('id_areadisciplinar', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_areadisciplinar', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('cct', models.CharField(max_length=200)),
                ('fecha', models.CharField(max_length=100)),
                ('semestre', models.IntegerField()),
                ('id_alumno', models.IntegerField()),
                ('id_dc', models.IntegerField()),
                ('asistencia', models.BooleanField()),
                ('retardo', models.BooleanField()),
                ('justificacion', models.BooleanField()),
                ('falta', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id_curso', models.IntegerField(primary_key=True, serialize=False)),
                ('clave_curso', models.CharField(max_length=150)),
                ('nombre_curso', models.CharField(max_length=150)),
                ('semestre', models.IntegerField()),
                ('descripcion', models.CharField(max_length=150)),
                ('creditos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Docente_curso',
            fields=[
                ('id_dc', models.AutoField(primary_key=True, serialize=False)),
                ('id_curso', models.IntegerField()),
                ('id_docente', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Entrega_actividad',
            fields=[
                ('id_entrega', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_actividad', models.CharField(max_length=400)),
                ('calificacion', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('retroalimentacion', models.CharField(max_length=500, null=True)),
                ('archivo', models.CharField(max_length=500)),
                ('fecha_hora_subida', models.CharField(max_length=50)),
                ('id_alumno', models.IntegerField()),
                ('id_actividad', models.IntegerField()),
                ('url', models.CharField(max_length=300)),
                ('comentario', models.CharField(max_length=500)),
                ('calificada', models.BooleanField()),
                ('entregada', models.BooleanField()),
                ('totalO', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id_modulo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_modulo', models.CharField(max_length=150)),
                ('pdf_modulo', models.FileField(upload_to='Archivos/modulos')),
                ('fecha_alta_modulo', models.DateField(auto_now=True)),
                ('creditos_modulo', models.IntegerField()),
                ('areadisciplinar_modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBC.Area_disciplinar')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion_act',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('id_dc', models.IntegerField()),
                ('id_actividad', models.IntegerField()),
                ('mensaje', models.CharField(max_length=500)),
                ('tipo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion_act_alumno',
            fields=[
                ('id_notificacion_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('id_alumno', models.IntegerField()),
                ('status', models.IntegerField()),
                ('id_notificacion', models.CharField(max_length=500)),
                ('id_dc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion_act_docente',
            fields=[
                ('id_notificacion_docente', models.AutoField(primary_key=True, serialize=False)),
                ('id_docente', models.IntegerField()),
                ('status', models.IntegerField()),
                ('id_notificacion', models.CharField(max_length=500)),
                ('id_alumno', models.IntegerField()),
                ('id_dc', models.IntegerField()),
                ('tipo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion_mod',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('id_curso', models.IntegerField()),
                ('mensaje', models.CharField(max_length=500)),
                ('tipo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion_mod_docente',
            fields=[
                ('id_notificacion_mod_doc', models.AutoField(primary_key=True, serialize=False)),
                ('id_docente', models.IntegerField()),
                ('status', models.IntegerField()),
                ('id_notificacion', models.IntegerField()),
                ('fecha_hora', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id_semestre', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_semestre', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Unidad_modulo',
            fields=[
                ('id_unidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_unidad', models.CharField(max_length=500)),
                ('proposito_unidad', models.CharField(max_length=800)),
                ('id_modulo_unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBC.Modulo')),
            ],
        ),
        migrations.AddField(
            model_name='modulo',
            name='semestre_modulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBC.Semestre'),
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id_docente', models.IntegerField(primary_key=True, serialize=False)),
                ('nombres_docente', models.CharField(max_length=150)),
                ('apellidos_docente', models.CharField(max_length=150, null=True)),
                ('edad_docente', models.IntegerField()),
                ('email', models.CharField(max_length=150)),
                ('clave_docente', models.CharField(max_length=150)),
                ('cct', models.CharField(max_length=50)),
                ('curp_docente', models.CharField(max_length=20)),
                ('rfc_docente', models.CharField(max_length=30)),
                ('tel_fijo', models.CharField(max_length=150, null=True)),
                ('tel_cel', models.CharField(max_length=150)),
                ('nombre_escuela', models.CharField(max_length=150)),
                ('domicilio', models.CharField(max_length=500, null=True)),
                ('num_empleado', models.CharField(max_length=150, null=True)),
                ('curriculum', models.FileField(blank=True, null=True, upload_to='TBC/Archivos')),
                ('perfil_profesional', models.CharField(max_length=200, null=True)),
                ('maximo_grado', models.CharField(max_length=200, null=True)),
                ('localidad', models.CharField(max_length=200, null=True)),
                ('areadisciplinar_docente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TBC.Area_disciplinar')),
            ],
        ),
        migrations.CreateModel(
            name='Aprendizaje_esperado_modulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('aprendizaje_esperado', models.CharField(max_length=700)),
                ('modulo_aprendizaje_esperado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBC.Modulo')),
                ('unidad_aprendizaje_esperado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TBC.Unidad_modulo')),
            ],
        ),
    ]