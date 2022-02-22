const sendMessage = () => {
    const message = $('#message_send').val()

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
                        <div class="p-4 m-4 rounded-lg text-slate-50 bg-slate-500 shadow-lg max-w-2xl self-end">
                            ${messageModel.content}
                        </div>
                    </>`
            )
            $("#messages").animate({scrollTop: $('#messages').prop("scrollHeight")}, 1000);
        });
}

$(window).on('load', function () {
    $("#messages").animate({scrollTop: $('#messages').prop("scrollHeight")}, 1000);
});