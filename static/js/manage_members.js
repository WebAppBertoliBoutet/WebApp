const manage_members = (id) => {
    let manage_members_form = `<div class="create_conv_modal fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title"
                                role="dialog" id="manage_members_modal"
                                aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div
                class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6 ">
                <button type="button" onclick="closeModal()"
                            class="rounded-full text-red-400 border border-hidden shadow-sm px-2 py-2 text-base font-medium hover:bg-red-400 hover:text-white  sm:text-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                <div>
                    <div class="mt-3 text-center sm:mt-5 text-slate-600">
                        <h3 class="text-lg leading-6 font-medium" id="modal-title">Group members</h3>
                        <div>Manage members of the group</div>
                    </div>
                </div>
                <div class="mt-4">
                    <form id="manage_members_form" class="w-full">
                        <input type="email" name="email" placeholder="Email to add..." class="rounded mt-4 border border-gray-300 p-3 w-full" />
                        <input type="submit" value="Add a member" class="bg-indigo-500 mt-4 text-sm inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white hover:bg-indigo-700"/>
                    </form>
                </div>
                <div class="mt-4">
                    <button type="button"
                            class="inline-flex justify-center w-full rounded-md border border-red-400 shadow-sm px-4 py-2 bg-white text-base font-medium text-red-400 hover:bg-red-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:text-sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7a4 4 0 11-8 0 4 4 0 018 0zM9 14a6 6 0 00-6 6v1h12v-1a6 6 0 00-6-6zM21 12h-6" />
                        </svg>
                        Leave the group
                    </button>
                </div>
            </div>
        </div>
    </div>`

    $('body').append(manage_members_form)

    let alreadySubmitted = false;

    const formElem = document.querySelector('#manage_members_form')
    formElem.addEventListener('submit', (event) => {
        event.preventDefault()
        const formData = new FormData(formElem);
        const email = formData.get('email');
        $.post("/conversation/" + id + '/members', {
            'email': email
        })
            .done((res) => {
                if (res.error && !alreadySubmitted) {
                    alreadySubmitted = true;
                    const error_element = `<div class="rounded-md bg-red-50 p-4 mt-2">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg"
                                         viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                        <path fill-rule="evenodd"
                                              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                              clip-rule="evenodd"/>
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <h3 class="text-sm font-medium text-red-800">Il y a une erreur avec votre soumission</h3>
                                    <div class="mt-2 text-sm text-red-700">
                                        <ul role="list" class="list-disc pl-5 space-y-1">
                                            <li>${res.error}</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>`
                    $('#manage_members_form').append(error_element)
                } else {
                    alreadySubmitted = false;
                }
            })

    })
}