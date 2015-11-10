$('body').on('click', '.change', function(){
            var text = $(this).closest('.record').find('.record-inner').text();
            $(this).closest('.record').addClass('changed');
            $(this).closest('.record').html("<textarea type=\"text\" class=\"form-control\" maxlength=\"255\">" + text + "</textarea><p class=\"counter\"></p><button class=\"btn btn-inverse apply pull-right\" type=\"button\" value=\""+$(this).closest('.record').attr('id') +"\">Готово</button>");
        });

        function getCSRF(){
                function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        var csrftoken = $.cookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
            }

        $('body').on('click', '.remove', function(){
            var id = $(this).attr('value');
            getCSRF();
            $.post('/remove/', 
                   {
                record_id: id,
                }
            , onRemoveSuccess);
        });

        function onRemoveSuccess(data){
            $('#'+data).remove();
        }

        $('body').on('click', '.add', function(){
            var text = $(this).closest('div').find('.form-control').val();
            getCSRF();
            $.post('/add/',
                   {
                record: text,
                },
                   onAddSuccess);
        });

            function onAddSuccess(data){
                $('.add-form').after('<div class="col-lg-12 record" id="'+data.id+'">'+
                                     '<div class="record-info">'+
                            '<a href="/id'+data.author_id+'">'+data.author_name+'</a><span class="secondary"> @'+data.author_alias+' - '+data.date+'</span>'+
                                '<div class="btn-group-vertical pull-right">'+
                                    '<button class="btn btn-default remove" type="button" name="record_id" value="'+data.id+'">'+
                                        '<span class="glyphicon glyphicon-remove"></span>'+
                                    '</button>'+
                                    '<button class="btn btn-default change" type="button" value="'+data.id+'">'+
                                    '<span class="glyphicon glyphicon-pencil"></span>'+
                                    '</button>'+
                                '</div>'+
                            '</div>'+
                            '<p class="record-inner">'+data.text+'</p>'+
                        '</div>');
                $('.add-form').find('.form-control').val('');
            }
        
        $('body').on('keydown', '.form-control', function(){
                var length = $(this).val().length;
                $(this).closest('div').find('.counter').text(255 - length);
        });
        $('body').on('click', '.apply', function(){
            var text = $(this).closest('.record').find('.form-control').val();
            var id = $(this).val();
            getCSRF();
            $.post('/update/', {
                record: text,
                record_id: id,

            },
                   onUpdateSuccess);
        });

            function onUpdateSuccess(data){
               $('.changed').html('<div class="record-info">'+
                            '<a href="/id'+data.author_id+'">'+data.author_name+'</a><span class="secondary"> @'+data.author_alias+' - '+data.date+'</span>'+
                                '<div class="btn-group-vertical pull-right">'+
                                    '<button class="btn btn-default remove" type="button" name="record_id" value="'+data.id+'">'+
                                        '<span class="glyphicon glyphicon-remove"></span>'+
                                    '</button>'+
                                    '<button class="btn btn-default change" type="button" value="'+data.id+'">'+
                                    '<span class="glyphicon glyphicon-pencil"></span>'+
                                    '</button>'+
                                '</div>'+
                            '</div>'+'<p class="record-inner">'+data.text+'</p>');
                $('.changed').removeClass('changed');
            }