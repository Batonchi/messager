async function get_messages(user2_id) {
   await fetch(`/chat/get?user2_id=${user2_id}`).then(response => {
        return response.json()
    }).then((messages) => {
        console.log(messages)
        // const user2_id = 1 // ID ПОЛЬЗОВАТЕЛЯ С КОТОРЫМ ОТКРЫТ ТЕКУЩИЙ ЧАТ
        // const ws = new WebSocket(`/chat/send/${user2_id}`)
        // ws.onmessage = function(event) {
        // if (event.data == user2_id) {
        //     get_messages(user2_id)
        //     }
        // }
   })

}

async function send_message() {
    // ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ
    // ПОЛУЧИМ ТЕКСТ С ИНПУТА и тд.
    text = ''
    ws.send(text)
}

document.addEventListener('DOMContentLoaded',  async () => {
    await fetch('/chat/all').then(response => {
        return response.json()
    }).then((users) => {
        const chats = document.getElementById('chats')
        for (const user of users) {
            chats.insertAdjacentHTML('beforeend', `
                                <div class="scroll-elem" onclick="get_messages(${user.user_id})">
                                    <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png');"></div>
                                    <div class="content">
                                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                                        <span>ИМЯ: ${user.first_name}</span>
                                    </div>
                                </div>`)
        }
    })
})