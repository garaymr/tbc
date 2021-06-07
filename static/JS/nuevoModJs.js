var selectedUnidad ="";
var selectedAprendizaje ="";
var moduloGuardado = false;
var nombreModulo = "";
var nombreUnidad = "";
var nombreAPES = "";
var semestre="";
var creditos="";
var AD="";
var token="";
var moduloPK="";

function crearUnidad(){
    var tituloAPES =  document.getElementById("tituloAPES");
    var btnNAE =  document.getElementById("btnNAE");
    var propUnidad = document.getElementById("propositoUnidad");
    var tituloPropUnidad = document.getElementById("tituloPropUnidad");
    Swal.fire({
        title: 'Nueva unidad',
        input: 'text',
        inputPlaceholder: "Ingrese el nombre de la unidad",
        showCancelButton: true,
        confirmButtonColor: '#02991B',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value) {
            var elemento = document.createElement("a");
            elemento.innerHTML=result.value
            var elemento2 = document.createElement("a");
            var elemento3 = document.createElement("a");

            nombreUnidad=result.value;
            tituloAPES.innerHTML= "Aprendizajes esperados de la unidad: "+ nombreUnidad;
            $.ajax({
                url: '/TBC/Modulos/nuevo/unidad/guardar',
                data:
                {
                    'moduloDeLaUnidad':moduloPK,
                    'nombreUnidad':nombreUnidad,
                },
                dataType: "json",
                success:function(response){
                    console.log(response);  
                    $.each(JSON.parse(response),function(i,item){
                        selectedUnidad = item["pk"]
                        elemento.setAttribute("id", ''+item["pk"]);
                        elemento.setAttribute('onclick','getAPES(this.id)')
                        elemento2.setAttribute('onclick','deleteUnidad(this.id)')
                        elemento3.setAttribute('onclick','updateUnidad(this.id)');
                        elemento2.setAttribute("id",''+item["pk"]);
                        elemento3.setAttribute("id",''+item["pk"]);           

                        tituloPropUnidad.innerHTML= "Próposito de la unidad: "+ nombreUnidad;
                        propUnidad.readOnly=false;
                        btnNAE.className="col-lg-6 btn btn-block btn-outline-success";
                        elemento.className="col-lg-8 btn btn-block btn-outline-info";
                        elemento3.style.marginTop="2px";
                        elemento3.className="col-lg-4 btn btn-info btn-circle";
                        elemento3.innerHTML="Modificar";
                        elemento3.style.color="#FFFFFF";
                        elemento3.style.fontSize="10px";
                        elemento.style.marginTop="2%";
            
                        elemento2.style.marginTop="2px";
            
                        elemento2.className="col-lg-4 btn btn-danger btn-circle";
            
                        elemento2.innerHTML="Eliminar";
            
                        elemento2.style.fontSize="10px";
            
                        elemento2.style.color="#FFFFFF";
            
                        document.getElementById("divUnidades").appendChild(elemento);

                        var divRow = document.createElement("div");
                        divRow.setAttribute("id","divRow"+selectedUnidad);
                        divRow.className="row col-lg-10";        
                        document.getElementById("divUnidades").appendChild(divRow);
                        document.getElementById("divRow"+item["pk"]).appendChild(elemento3);
                        document.getElementById("divRow"+item["pk"]).appendChild(elemento2);
                        $("#"+selectedUnidad).hide().fadeIn('slow');
                        document.getElementById("divApEsperados").innerHTML="";
                    });       
                }
            })
        }
        })
    };

    function deleteUnidad(idNombre){
        var unidad = document.getElementById(''+idNombre);
        var divU = document.getElementById("divUnidades");
        Swal.fire({
            title: '¿Eliminar la unidad '+unidad.innerHTML+'?',
            text: 'Se eliminarán todos los aprendizajes esperados de la unidad',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#ffcc66',
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: '/TBC/Modulos/delete/unidad/'+idNombre,
                    dataType: "json",
                    success:function(response){
                        console.log("Unidad eliminada")    
                        divU.innerHTML="";
                        getUnidades();
                    }
                })    
            }
            })
    };

    function updateUnidad(idNombre){
        var unidad = document.getElementById(''+idNombre);
        var divU = document.getElementById("divUnidades");
        selectedUnidad = unidad.id;
        Swal.fire({
            title: 'Actualizar unidad: '+unidad.innerHTML+'?',
            text: 'Ingrese el nuevo nombre de la unidad',
            input: 'text',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#ffcc66',
            confirmButtonText: 'Guardar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: '/TBC/Modulos/update/unidad',
                    data:
                    {
                        'idNombre':selectedUnidad,
                        'nombreUnidad':result.value
                    },
                    dataType: "json",
                    success:function(response){
                        console.log("Unidad eliminada")    
                        divU.innerHTML="";
                        getUnidades();
                    }
                })    
            }
            })
    };

    function deleteAPES(idNombre){
        var apes = document.getElementById(''+idNombre);
        var divAP = document.getElementById("divApEsperados");
        Swal.fire({
            title: '¿Eliminar el aprendizaje esperado: '+apes.innerHTML+'?',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#ffcc66',
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: '/TBC/Modulos/delete/APES',
                    data:
                    {
                        'aprendizajeEsperado':apes.id,
                    },
                    dataType: "json",
                    success:function(response){
                        console.log("APES eliminado")    
                        divAP.innerHTML="";
                        getAPES(selectedUnidad);
                    }
                })
            }
            })
    };

    function updateAPES(idNombre){
        var apes = document.getElementById(''+idNombre);
        selectedAprendizaje = apes.id;
        var divAP = document.getElementById("divApEsperados");
        Swal.fire({
            title: 'Actualizar unidad: '+apes.innerHTML+'?',
            text: 'Ingrese el nuevo aprendizaje esperado',
            input: 'text',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#ffcc66',
            confirmButtonText: 'Guardar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    url: '/TBC/Modulos/update/APES',
                    data:
                    {
                        'aprendizajeActual': apes.id,
                        'aprendizajeNuevo': result.value
                    },
                    dataType: "json",
                    success:function(response){    
                        getAPES(selectedUnidad);
                    }
                })       
            }
            })
    };

    function getUnidades(){
        var tituloAPES =  document.getElementById("tituloAPES");
        var tituloPropUnidad = document.getElementById("tituloPropUnidad");
        document.getElementById("divApEsperados").innerHTML="";
        console.log(nombreModulo)
        $.ajax({
            url: '/TBC/Modulos/get/Unidades',
            dataType: "json",
            data:
            {
                'idNombre': nombreModulo
            },
            success:function(response){
                console.log(response); 
                $.each(JSON.parse(response),function(i,item){

                    //Creamos los 3 botones que vamos a agregar al div
                    var elemento = document.createElement("a");
                    var elemento2 = document.createElement("a");
                    var elemento3 = document.createElement("a");

                    //Agregar listener a los botones
                    elemento.setAttribute('onclick','getAPES(this.id)')
                    elemento2.setAttribute('onclick','deleteUnidad(this.id)')
                    elemento3.setAttribute('onclick','updateUnidad(this.id)');

                    //Agregamos el id de la unidad como id de los botones
                    elemento.setAttribute("id", ''+item["pk"]);
                    elemento2.setAttribute("id",''+item["pk"]);
                    elemento3.setAttribute("id",''+item["pk"]);

                    //Agregamos el texto a los botones
                    elemento.innerHTML=item["fields"]["nombre_unidad"];
                    elemento2.innerHTML="Eliminar";
                    elemento3.innerHTML="Modificar";

                    //Definimos las clases de bootstrap de los botones
                    elemento.className="col-lg-8 btn btn-block btn-outline-info";
                    elemento2.className="col-lg-4 btn btn-danger btn-circle";
                    elemento3.className="col-lg-4 btn btn-info btn-circle";

                    //Definimos los estilos de los botones
                    elemento.style.marginTop="2%";
                    elemento2.style.marginTop="2px";
                    elemento2.style.fontSize="10px";
                    elemento2.style.color="#FFFFFF";
                    elemento3.style.marginTop="2px";
                    elemento3.style.color="#FFFFFF";
                    elemento3.style.fontSize="10px";
                    
                    // Creamos un div row para agregar los botones previos, tambien definimos sus caracteristicas
                    var divRow = document.createElement("div");
                    divRow.setAttribute("id","divRow"+item["pk"]);
                    divRow.className="row col-lg-10";      

                    //Agregamos el boton de unidad al div principal
                    document.getElementById("divUnidades").appendChild(elemento)
                    
                    //Agregamos el div row al div principal
                    document.getElementById("divUnidades").appendChild(divRow);

                    //Agregamos nuestros botones al div row
                    document.getElementById("divRow"+item["pk"]).appendChild(elemento3);
                    document.getElementById("divRow"+item["pk"]).appendChild(elemento2);

                    $("#"+item["pk"]).hide().fadeIn('slow');
                });   
                tituloAPES.innerHTML= "Aprendizajes esperados";
                tituloPropUnidad.innerHTML =   "Próposito de la unidad";
            }
        })
    };

    function getAPES(idNombre){
        selectedUnidad=idNombre;
        var tituloAPES =  document.getElementById("tituloAPES");
        var tituloPropUnidad = document.getElementById("tituloPropUnidad");
        var btnNAE =  document.getElementById("btnNAE");
        btnNAE.className="col-lg-6 btn btn-block btn-outline-success";
        var unidad = document.getElementById(idNombre);
        document.getElementById("divApEsperados").innerHTML="";
        var prop = document.getElementById("propositoUnidad");

        $.ajax({
            url: '/TBC/Modulos/update/getpropositoUnidad',
            data:
            {
                'modulo':moduloPK,
                'unidad':selectedUnidad,
            },
            dataType: "json",
            success:function(response){
                $.each(JSON.parse(response),function(i,item){
                    prop.value = item["fields"]["proposito_unidad"]
                })
            }
        })

        $.ajax({
            url: '/TBC/Modulos/get/APES/'+idNombre,
            dataType: "json",
            success:function(response){
                console.log(response);  
                $.each(JSON.parse(response),function(i,item){
                             //Creamos los 3 botones que vamos a agregar al div
                             var elemento = document.createElement("a");
                             var elemento2 = document.createElement("a");
                             var elemento3 = document.createElement("a");
         
                             //Agregar listener a los botones
                             elemento2.setAttribute('onclick','deleteAPES(this.id)')
                             elemento3.setAttribute('onclick','updateAPES(this.id)');
                             //Si hay un proposito de la unidad, que lo muestre
                             //Agregamos el id de la unidad como id de los botones
                             elemento.setAttribute("id", 'apes-'+item["pk"]);
                             elemento2.setAttribute("id",'apes-'+item["pk"]);
                             elemento3.setAttribute("id",'apes-'+item["pk"]);
         
                             //Agregamos el texto a los botones
                             elemento.innerHTML=item["fields"]["aprendizaje_esperado"];
                             elemento2.innerHTML="Eliminar";
                             elemento3.innerHTML="Modificar";
         
                             //Definimos las clases de bootstrap de los botones
                             elemento.className="col-lg-8 btn btn-block btn-outline-info";
                             elemento2.className="col-lg-4 btn btn-danger btn-circle";
                             elemento3.className="col-lg-4 btn btn-info btn-circle";
         
                             //Definimos los estilos de los botones
                             elemento.style.marginTop="2%";
                             elemento2.style.marginTop="2px";
                             elemento2.style.fontSize="10px";
                             elemento2.style.color="#FFFFFF";
                             elemento3.style.marginTop="2px";
                             elemento3.style.color="#FFFFFF";
                             elemento3.style.fontSize="10px";
                             
                             // Creamos un div row para agregar los botones previos, tambien definimos sus caracteristicas
                             var divRow = document.createElement("div");
                             divRow.setAttribute("id","divRowApes"+item["pk"]);
                             divRow.className="row col-lg-10";      
         
                             //Agregamos el boton de unidad al div principal
                             document.getElementById("divApEsperados").appendChild(elemento)
                             
                             //Agregamos el div row al div principal
                             document.getElementById("divApEsperados").appendChild(divRow);
         
                             //Agregamos nuestros botones al div row
                             document.getElementById("divRowApes"+item["pk"]).appendChild(elemento3);
                             document.getElementById("divRowApes"+item["pk"]).appendChild(elemento2);
         
                             $("#"+item["pk"]).hide().fadeIn('slow');
                });   
                tituloAPES.innerHTML= "Aprendizajes esperados de la unidad: "+ unidad.innerHTML; 
                tituloPropUnidad.innerHTML =   "Próposito de la unidad:\n"+ unidad.innerHTML;
            }
        })
    };

    function crearApes(){
        Swal.fire({
            title: 'Nuevo aprendizaje esperado',
            input: 'text',
            inputPlaceholder: "Ingrese un aprendizaje esperado",
            showCancelButton: true,
            confirmButtonColor: '#02991B',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Guardar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.value) {
                nombreAPES=result.value;
                console.log(selectedUnidad)
                $.ajax({
                    url: '/TBC/Modulos/nuevo/apes/guardar',
                    data:
                    {
                        'apesDeLaUnidad':nombreAPES,
                        'nombreUnidad':selectedUnidad,
                        'modulo':nombreModulo
                    },
                    dataType: "json",
                    success:function(response){
                        console.log(response);  
                        $.each(JSON.parse(response),function(i,item){
                    selectedAprendizaje=item["pk"];
                    //Creamos los 3 botones que vamos a agregar al div
                    var elemento = document.createElement("a");
                    var elemento2 = document.createElement("a");
                    var elemento3 = document.createElement("a");

                    //Agregar listener a los botones
                    elemento2.setAttribute('onclick','deleteAPES(this.id)')
                    elemento3.setAttribute('onclick','updateAPES(this.id)');

                    //Agregamos el id del apes como id de los botones
                    elemento.setAttribute("id", 'apes-'+item["pk"]);
                    elemento2.setAttribute("id",'apes-'+item["pk"]);
                    elemento3.setAttribute("id",'apes-'+item["pk"]);

                    //Agregamos el texto a los botones
                    elemento.innerHTML=nombreAPES;
                    elemento2.innerHTML="Eliminar";
                    elemento3.innerHTML="Modificar";

                    //Definimos las clases de bootstrap de los botones
                    elemento.className="col-lg-8 btn btn-block btn-outline-info";
                    elemento2.className="col-lg-4 btn btn-danger btn-circle";
                    elemento3.className="col-lg-4 btn btn-info btn-circle";

                    //Definimos los estilos de los botones
                    elemento.style.marginTop="2%";
                    elemento2.style.marginTop="2px";
                    elemento2.style.fontSize="10px";
                    elemento2.style.color="#FFFFFF";
                    elemento3.style.marginTop="2px";
                    elemento3.style.color="#FFFFFF";
                    elemento3.style.fontSize="10px";
                    
                    // Creamos un div row para agregar los botones previos, tambien definimos sus caracteristicas
                    var divRow = document.createElement("div");
                    divRow.setAttribute("id","divRowApes"+item["pk"]);
                    divRow.className="row col-lg-10";      

                    //Agregamos el boton de unidad al div principal
                    document.getElementById("divApEsperados").appendChild(elemento)
                    
                    //Agregamos el div row al div principal
                    document.getElementById("divApEsperados").appendChild(divRow);

                    //Agregamos nuestros botones al div row
                    document.getElementById("divRowApes"+item["pk"]).appendChild(elemento3);
                    document.getElementById("divRowApes"+item["pk"]).appendChild(elemento2);

                    $("#"+item["pk"]).hide().fadeIn('slow');
                            
                        });       
                    }
                })

               
            }
            })
        };

    function textEnteredModulo(){
        var btnGuardar =  document.getElementById("btnGuardarModulo");
        var txt = document.getElementById("inputNombre").value;
        if(txt != "" && !moduloGuardado)
        {
            btnGuardar.className="col-lg-2 btn btn-block btn-info";
        }else{
            if(!moduloGuardado){
            btnGuardar.className="col-lg-2 btn btn-block btn-info disabled";
            }
        }
        };

        function desactivarBtnGuardar(){
            var tblModulos = document.getElementById("tableModulos");
            var selectSemestre = document.getElementById("selectSemestre");
            var selectAD = document.getElementById("selectAD");
            var inputCreditos = document.getElementById("inputCreditos");
            var tituloModulo = document.getElementById("tituloModulo");
            var btnNU =  document.getElementById("btnNU");
            var inputNombre = document.getElementById("inputNombre"); 
            var  tituloUnidades =document.getElementById("tituloUnidades");

            //Validaciones para poder guardar el modulo
            if(selectSemestre.options[selectSemestre.selectedIndex].text.startsWith("Selec"))
            {
                Swal.fire({
                    title: 'Seleccione el semestre al que pertenece el módulo',
                    icon: 'warning',
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: 'Confirmar'
                }).then((result) => {
                    if (result.value) {
                        
                    }
                    })
            }
            else{
                //SI HAY SEMESTRE SELECCIONADO ENTONCES LO GUARDAMOS EN UNA VARIABLE
                semestre = parseInt(selectSemestre.options[selectSemestre.selectedIndex].value);
                if(selectAD.options[selectAD.selectedIndex].text.startsWith("Selec")){
                    Swal.fire({
                        title: 'Seleccione el area disciplinaría a la que pertenece el módulo',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Confirmar'
                    }).then((result) => {
                        if (result.value) {
                            
                        }
                        })
                }
                else{
                    //SI HAY AREA DISCIPLINARIA SELECCIONADA ENTONCES LA GUARDAMOS EN UNA VARIABLE
                    AD = parseInt(selectAD.options[selectAD.selectedIndex].value);
                    if(inputCreditos.value == ""){
                        Swal.fire({
                            title: 'Ingrese cuantos creditos otorga este módulo',
                            icon: 'warning',
                            confirmButtonColor: '#3085d6',
                            confirmButtonText: 'Confirmar'
                        }).then((result) => {
                            if (result.value) {
                                
                            }
                            })
                    }
                    else{

                        //SI HAY CREDITOS INGRESADOS ENTONCES LOS GUARDAMOS EN UNA VARIABLE
                        creditos = parseInt(inputCreditos.value);
                        moduloGuardado =true;
                        tituloModulo.innerHTML=inputNombre.value;
                        nombreModulo= inputNombre.value;
                        //console.log('/TBC/Modulos/nuevo/guardar/'+nombreModuloF+"/"+semestre+"/"+AD+"/"+creditos);
                            $.ajax({
                                url: '/TBC/Modulos/nuevo/guardar',
                                data:
                                {
                                    'nombre':nombreModulo,
                                    'semestre':semestre,
                                    'AD':AD,
                                    'creditos':creditos
                                },
                                dataType: "json",
                                success:function(response){
                                    console.log(response);  
                                    $.each(JSON.parse(response),function(i,item){
                                        moduloPK = item["pk"]
                                        var newRow = tblModulos.insertRow(1);
                                        newRow.setAttribute('onclick','setModulo(this.id)');
                                        newRow.id="tableRow"+moduloPK;
                                        var cell1 = newRow.insertCell(0);
                                        var cell2 = newRow.insertCell(1);
                                        cell1.id="tableMod-"+moduloPK;
                                        cell2.id="tableAD-{{mod.areadisciplinar_modulo.id_areadisciplinar}}-{{mod.semestre_modulo.id_semestre}}"
                                        cell1.innerHTML=item["fields"]["nombre_modulo"];
                                        cell2.id="tableAD-"+item["fields"]["areadisciplinar_modulo"]+"-"+item["fields"]["semestre_modulo"];
                                        cell2.innerHTML=selectAD.options[selectAD.selectedIndex].text;
                                    });
                                     
                                }
                            })
                        tituloUnidades.innerHTML="Unidades del módulo: "+nombreModulo;
                        //inputNombre.readOnly= true;
                        btnNU.className="col-lg-6 btn btn-block btn-outline-success";   
                    }
                          
                }
                }
                
        };
        
        function setModulo(idRow){
            var tblRow = document.getElementById(idRow);
            var divUnidades = document.getElementById("divUnidades");
            var tituloModulo = document.getElementById("tituloModulo");
            var selectSemestre = document.getElementById("selectSemestre");
            var selectAD = document.getElementById("selectAD");
            var Cells = tblRow.getElementsByTagName("td");
            var btnNU =  document.getElementById("btnNU");
            nombreModulo = Cells[0].innerText;
            moduloPK = Cells[0].id.split("-")[1];
            var idAD = Cells[1].id.split("-")[1];
            var idSemestre = Cells[1].id.split("-")[2];
            
            var nombreModinput = document.getElementById("inputNombre");
            nombreModinput.value = ""+Cells[0].innerText;
            tituloModulo.innerHTML = ""+Cells[0].innerText;
            nombreModulo = Cells[0].innerText;

            var  tituloUnidades =document.getElementById("tituloUnidades");
            tituloUnidades.innerHTML="Unidades del módulo: "+nombreModulo;

            btnNU.className="col-lg-6 btn btn-block btn-outline-success";
            divUnidades.innerHTML="";
            selectSemestre.selectedIndex=idSemestre;
            selectAD.selectedIndex=idAD;
            getUnidades();
            
        };

        function updProposito(){

            var prop = document.getElementById("propositoUnidad");
            $.ajax({
                url: '/TBC/Modulos/update/propositoUnidad',
                data:
                {
                    'modulo':moduloPK,
                    'unidad':selectedUnidad,
                    'proposito': prop.value,
                },
                dataType: "json",
                success:function(response){
                    console.log(moduloPK);  
                    console.log(selectedUnidad); 
                    console.log(prop.value); 
                }
            })
        };

        function updArchivo(){
            

            var pdfModulo = $('#pdfInput').get(0).files[0];

            var formData = new FormData();
            formData.append("archivo", pdfModulo);
            formData.append("modulo", moduloPK);
            $.ajax({
                url: '/TBC/Modulos/update/archivo',
                headers:{ "X-CSRFToken": $('meta[name="_token"]').attr('content') },
                data: formData,
                type: 'POST',
                async: true,
                processData: false,
                contentType: false,
                dataType: "json",
                enctype: 'multipart/form-data',
                success:function(response){
                    console.log(response);  
                }
            })
        };


        function cargarListeners() { 
            var inputNombre = document.getElementById("inputNombre"); 
            var btnGuardar = document.getElementById("btnGuardarModulo");
            var btnNU =  document.getElementById("btnNU");
            var btnNAE =  document.getElementById("btnNAE");
            var btnGuardarProposito = document.getElementById("btnGuardarProposito");
            var btnGuardarArchivo = document.getElementById("btnGuardarArchivo");

            inputNombre.addEventListener("keyup", textEnteredModulo, false); 
            btnGuardar.addEventListener("click",desactivarBtnGuardar,false);
            btnNU.addEventListener("click", crearUnidad,false);
            btnNAE.addEventListener("click",crearApes,false);       
            btnGuardarProposito.addEventListener("click",updProposito,false);
            btnGuardarArchivo.addEventListener("click",updArchivo,false);

            $.ajaxSetup({
                headers: {
                  'X-CSRF-Token': $('meta[name="_token"]').attr('content')
                }
            });
          }

 
    document.addEventListener("DOMContentLoaded", cargarListeners, false);
