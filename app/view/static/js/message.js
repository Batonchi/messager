async function get_messages(user2_id) {
   await fetch(`/chat/get?user2_id=${user2_id}`).then(response => {
        return response.json()
    }).then((messages) => {
        console.log(messages)
   })
}

async function get_current_chat(user2_id) {
    get_messages(user2_id)
    const current_user_id = document.getElementById('current_user_id').value
    const ws = new WebSocket(`/chat/send/${current_user_id}?user2_id=${user2_id}`)
    ws.onmessage = function(event) {
    if (event.data == user2_id) {
            get_messages(user2_id)
        }
    }
    document.getElementById('send').addEventListener('click', async e => {
        e.preventDefault();
        const message = document.getElementById('message').value
        ws.send(message)
    })
}


document.addEventListener('DOMContentLoaded',  async () => {
    await fetch('/chat/all').then(response => {
        return response.json()
    }).then((users) => {
        const chats = document.getElementById('chats')
        for (const user of users) {
            chats.insertAdjacentHTML('beforeend', `
                                <div class="scroll-elem" onclick="get_current_chat(${user.user_id})">
                                    <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png');"></div>
                                    <div class="content">
                                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                                        <span>ИМЯ: ${user.first_name}</span>
                                    </div>
                                </div>`)
        }
    })
})