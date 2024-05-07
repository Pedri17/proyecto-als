function addUser(){
    const divFormUser = document.getElementById( "div-user-selector" );
    var listUserSelector = document.getElementById( "list-user-selector" );
    var username = document.getElementById( "user-add-name" ).value;
    var divUsuario = document.createElement("div");
        divUsuario.id = "div-user-" + username;

    var textoNombre = document.createElement("label");
        textoNombre.innerHTML = username+"&nbsp;&nbsp;&nbsp;";
        divUsuario.appendChild(textoNombre);

    var botonEliminar = document.createElement("input");
        botonEliminar.type = "button";
        botonEliminar.name = "buttonUsers";
        botonEliminar.value = "Eliminar";
        botonEliminar.addEventListener("click", function() {
          removeUser(username);
        });

        divUsuario.appendChild(botonEliminar);

        if(listUserSelector){
            separador = document.createElement("li")
            separador.appendChild(divUsuario)
            separador.id = "li-user-"+username;
            listUserSelector.appendChild(separador)
        }else{
            divFormUser.appendChild(divUsuario);
        }

        document.getElementById( "user-add-name" ).value = ""

    var nombreComoInput = document.createElement("input");
        nombreComoInput.type = "hidden";
        nombreComoInput.name = "username_from_selector";
        nombreComoInput.value = username;

    var mainForm = document.getElementById( "main-form" );
        mainForm.appendChild(nombreComoInput);
}

function removeUser(username){
    var thisUser = document.getElementById("div-user-"+username);
    var thisUserList = document.getElementById("li-user-"+username);
    if(thisUserList){
        thisUserList.remove();
    }else if(thisUser){
        thisUser.remove()
    }
}