
function materialURL(tipoUsuario){
    $.ajax({
        url: '/TBC/material-didactico-CCT/',
        dataType: "json",
        success:function(response){
            console.log("Llamada")    
        }
    }) 
}