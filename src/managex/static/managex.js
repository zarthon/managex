
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
                    apprise("Network Error. Could not Contact Server");
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

    $('.authorize_url').bind("click",function(){
        var temp = $(this).attr("id");
        var username=temp.split("@");
        apprise('Enter the Message?',{'input':true},function(r){
            if(r){
                $.ajax({
                    cache:"false",
                    url:"/sendDM",
                    type:"GET",
                    data:"message="+r+"@"+username[0],
                    error:function(){
                        apprise("Network Error. Could not Contact Server");
                    },
                    success:function(data){
                        apprise(data);
                    }
                })         
            }
            else{
                return false;
            }
        });
    });

    $("#removeFriend").bind("click",function(){
        if(confirm("Are you sure you want to remove the friend ? ")){
            return true;
        }
        else{
            return false;
        }
    });
})
