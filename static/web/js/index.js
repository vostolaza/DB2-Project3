$(function () {

    $('#imageUploadForm').on('submit',(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        console.log(formData)

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
                console.log(data);
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
