async function get_messages(user2_id) {
   await fetch(`/chat/get?user2_id=${user2_id}`).then(response => {
        return response.json()
    }).then((messages) => {
        console.log(messages)
       const chatick = document.getElementById('chatick')
       chatick.innerHTML = ''
       for (let message of messages) {
           const div = document.createElement('div')
           if (message.sender_id != user2_id) {
               div.className = 'me'
           } else {
               div.className = 'not_me'
           }
           div.insertAdjacentHTML('beforeend', `<p>${message.sender}</p><p>${message.text_message}</p>`)
           document.getElementById('chatick').insertAdjacentElement('beforeend', div)
       }
       chatick.scrollTop = chatick.scrollHeight
   })
}

let ws;

async function get_current_chat(user2_id) {
    const current_user_id = document.getElementById('current_user_id').value
    // Проверим что веб сокет уже подключен и если это так, то закроем его
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
    }
    ws = new WebSocket(`/chat/send/${current_user_id}?user2_id=${user2_id}`)
    ws.onmessage = function(event) {
    if (event.data == user2_id) {
            get_messages(user2_id)
        }
    }

    get_messages(user2_id)
    document.getElementById('send').addEventListener('click', async e => {
        e.preventDefault();
        const message = document.getElementById('send_message').value
        if (message.trim() !== '') {
            ws.send(message)
            get_messages(user2_id)
        }
        document.getElementById('send_message').value = ''
    })
}


document.addEventListener('DOMContentLoaded',  async () => {
    await fetch('/chat/all').then(response => {
        return response.json()
    }).then((users) => {
        const chats = document.getElementById('scroll_area')
        for (const user of users) {
            chats.insertAdjacentHTML('afterbegin', `
                                <div class="scroll-elem" onclick="get_current_chat(${user.user_id})">
                                    <div class="photo" style="background-image: url('/static/avatars/${user.photo_of_profile}.png');"></div>
                                    <div class="inf">
                                        <p>ФАМИЛИЯ: ${user.first_name}</p>
                                        <p>ИМЯ: ${user.last_name}</p>
                                    </div>
                                </div>`)
        }
    })
})
