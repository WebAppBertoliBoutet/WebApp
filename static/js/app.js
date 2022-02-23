const sendMessage = () => {
    const message = $('#message_send').val()
    const href = $(location).attr('href')
    console.log(href)
    if (message) {

        $.post(href+'/message',
            {
                message: message
            },
        )
            .done((messageModel) => {
                $('#message_send').val('')
                $('#messages').append(
                    `<div class="self-end">
                        <p class="text-xs w-min whitespace-nowrap ml-auto mr-4 mt-2 self-end">
                            You, ${messageModel.created_at}
                        </p>
                        <div class="p-4 m-4 rounded-lg text-slate-50 bg-slate-500 shadow-lg ml-auto w-min whitespace-nowrap">
                            ${messageModel.content}
                        </div>
                    </>`
                )
                $("#messages").animate({scrollTop: $('#messages').prop("scrollHeight")}, 1000);
            });
    }

}

$(window).on('load', function () {
    $("#messages").animate({scrollTop: $('#messages').prop("scrollHeight")}, 1000);

    $(document).on('keypress', function (e) {
        if (e.which === 13) {
            sendMessage();
        }
    });
});