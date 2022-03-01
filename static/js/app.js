const sendMessage = () => {
    const message = $('#message_send').val()
    const href = $(location).attr('href')
    if (message) {

        $.post(href + '/message',
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

$(document).on('ready', function() {
    const form = $('#create_conv_form')
    form.onsubmit = async (e) => {
        e.preventDefault()
        const form_data = new FormData(form);
        console.log(form_data)
    }
})

function closeModal() {
    let modal = $('#create_conv_modal')
    modal.hide();
}

function create_conversation() {


    let create_conv_form = `<div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title"
                                role="dialog" id="create_conv_modal"
                                aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div
                class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6">
                <div>
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                        <svg class="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none"
                             viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M5 13l4 4L19 7"/>
                        </svg>
                    </div>
                    <div class="mt-3 text-center sm:mt-5">
                        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Créer une conversation</h3>
                        <form class="w-full" action="/conversation" method="POST">
                            <input placeholder="Nom de la conversation..." class="rounded mt-4 border border-gray-300 p-3 w-full" name="name"/>
                            <input type="submit" value="Créer" class="bg-indigo-500 mt-4 text-sm inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white hover:bg-indigo-700"/>
                        </form>
                    </div>
                </div>
                <div class="mt-4">
                    <button type="button" onclick="closeModal()"
                            class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
                        Annuler
                    </button>
                </div>
            </div>
        </div>
    </div>`

    $('body').append(create_conv_form)
}