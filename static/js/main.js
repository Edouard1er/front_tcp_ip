function validerFichier() {
    var checkedBoxes = [];
    $('input[name="file-list"]:checked').each(function() {
        checkedBoxes.push($(this).val());
    });
    
    if(checkedBoxes.length > 0) {
        data = {
            "file-list": checkedBoxes
        }
        $.ajax( {
            type: "POST",
            url: "/process_files",
            data: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            },
            success: function( response ) {
                if(response) {
                    response = JSON.parse(response);
                    divHtml = ``;
                    var files = response.data;
                    files.forEach((file, index) => {
                        divHtml += `<div id="div-${index}-${file}" class="flex all-div-file-list-to-dowload">
                                        <div class="mr-2">
                                            <a title="Télécharger le fichier" class="underline hover:text-blue-500" href="/download_file/${file}" class="">${file}</a>
                                        </div>
                                        <div class="mr-2">
                                            <img onclick="closeFile('div-${index}-${file}')" class="h-6 w-6  cursor-pointer" src="static/images/croix.svg" alt="Enlever" title="Enlever de la liste"/>
                                        </div>
                                    </div>`
                    });
                    $("#file-to-download").html(divHtml);
                    $("#text-download").show();
                    $("#validate").hide();
                    $("#done").show()
                }
            },
            error: function( response ) {}						
        } );
    }else{
        alert("Veuillez sélectionner au moins un fichier");
    }
}

function downloadFile(filename) {
    
    $.ajax( {
        type: "GET",
        url: `/download_file/${filename}`,
        success: function( response ) {
            if(response) {
                response = JSON.parse(response);
            }
        },
        error: function( response ) {}						
    } );
}

function terminer(){
    var checkedBoxes = [];
    $('input[name="file-list"]:checked').each(function() {
        checkedBoxes.push($(this).val());
    });
    
    data = {
        "file-list": checkedBoxes
    }
    $.ajax( {
        type: "POST",
        url: "/terminer",
        data: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        },
        success: function( response ) {
            if(response) {
                $("#file-to-download").html(``);
                $("#validate").show();
                $("#done").hide()
                $('.file-list').prop('checked', false);
                document.getElementById("all-file").checked = false;
                $("#text-download").hide();
            }
        },
        error: function( response ) {}						
    } );
}

function closeFile(id_div) { 
    //Action du bouton de fermeture du fichier
    if(id_div){
        document.getElementById(id_div).style.display = "none";
        if ($('.all-div-file-list-to-dowload').length == $('.all-div-file-list-to-dowload:hidden').length){
            document.getElementById("done").click();
        }
    }
}

function clickAllCheckBox (id) {
    if(id){
        checked = document.getElementById(id).checked;
        if(checked){
            $('.file-list').prop('checked', true);
        }else{
            $('.file-list').prop('checked', false);
        }
    } 
}

onclickOneCheckBox = function(id){
    
    if(areAllChecked('file-list')){
        document.getElementById(id).checked = true;
    }else{
        document.getElementById(id).checked = false;
    }
}

function areAllChecked(className) {
    var allChecked = true;
    $('.' + className).each(function() {
      if (!$(this).prop('checked')) {
        allChecked = false;
        return false;
      }
    });
    return allChecked;
}
  
$('.file-list').prop('checked', false); 