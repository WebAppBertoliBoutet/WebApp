const sendMessage = () => {
    const message = $('#message_send').val()

    if (message) {

        $.post('/conversation/1/message',
            {
                message: message
            },
        )
            .done((messageModel) => {
                $('#message_send').val('')
                $('#messages').append(
                    `<div class="self-end">
                        <p class="text-xs mr-5 mt-2 self-end">
                            You, ${messageModel.created_at}
                        </p>
                        <div class="p-4 m-4 rounded-lg text-slate-50 bg-slate-500 shadow-lg max-w-2xl ml-auto w-min">
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