
//home page
$(document).ready(function(){
        $(".accordion pre").hide();
        $(".accordion h3").click(function(){
            $(this).next("pre").slideToggle("normal")
            $(this).toggleClass("active");
        })
    }    
)
