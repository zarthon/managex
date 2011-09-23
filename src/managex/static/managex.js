
//home page
$(document).ready(function(){
        $(".accordion pre").hide();
        $(".accordion h3").click(function(){
            $(this).next("pre").slideToggle("normal")
            $(this).toggleClass("active");
        })
    }    
)
$(document).ready(function(){
 
    $('#summary img').bind("click",function(){
        var temp = $(this).attr('id')
        if(confirm("Are you sure you want to remove the oder")){
            var called_obj = $(this);
            
            $.ajax({
                cache:"false",
                url: "/removexpense",
                type:"GET",
                data:"id="+temp,
                error:function(){
                    alert("Network Error. Could not Contact Server");
                },
                success:function(data){
                    $('.'+temp+'row').hide();
                },
            });
            return true;
        }
        else{
            return false;
        }
    })
})
