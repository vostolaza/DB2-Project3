$(function () {



    $("#kval").val("8");

    $('#typeSearch').on('change', function() {
        switch(this.value) {
            case '2':$("#kval").val("5");
            break;
            default:$("#kval").val("8");
            break;
        }
      });


    $('#imageUploadForm').on('submit',(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        var option=$("#typeSearch").val();
        var k=$("#kval").val();
        formData.append("typesearch", option);
        formData.append('kvalue',k);
        
        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data:formData,
            cache:false,
            contentType: false,
            processData: false,
            success:function(data){
              // $.growl.error({ message: "The kitten is attacking!" });
            //   $.growl.notice({ message: data.msg });
              // $.growl.warning({ message: "The kitten is ugly!" });
            // </script>
            // console.log(data);
            $("#searchimage").empty();
            var len=data.length;
            var cont=0;
            var template=''
            template+='<div class="row">';
            for(var i=0;i<len;i++){
                var name=data[i].split("/")[4];
                tmp='<div class="col-md-4">'+
                '<div class="thumbnail">'+
                    '<a href="'+data[i]+'">'+
                  '<img src="'+data[i]+'" style="width:100%">'+
                  '<div class="caption">'+
                    '<p>'+name+'</p>'+
                  '</div>'+
                '</a>'+
              '</div></div>';
                if(cont!=3){
                    template+=tmp
                    cont+=1;
                }else{
                    cont=0;
                    template+='</div>';
                    $("#searchimage").append(template);
                    template='';
                    template+='<div class="row">';
                    template+=tmp;
                    cont+=1;
                }
                if(i+1==len){
                    template+='</div>';
                    $("#searchimage").append(template);
                }

            }
            },
            error: function(data){
            //   $.growl.error({ message: data.msg});
                console.log(data);
            }
        });
  
        
    }));

    
  $('.btn-file :file').on('change', function() {
    // console.log("entro1");
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);

    var reader = new FileReader();
    reader.onload = function (e) {
        $('#blah')
            .attr('src', e.target.result)
            .width(500)
            .height(360)
            .show();
            
    };
    reader.readAsDataURL(input.get(0).files[0]);

  });
  
    $('.btn-file :file').on('fileselect', function(event, numFiles, label) {
      // console.log("entro2");
      var input = $(this).parents('.input-group').find(':text'),
          log = numFiles > 1 ? numFiles + ' files selected' : label;
      
      if( input.length ) {
          input.val(log);
      } else {
          if( log ) alert(log);
      }
  });


});
