async function get_messages() {
    // ПОЛУЧАЕМ ВСЕ СООБЩЕНИЯ ТЕКУЩЕГО ОТКРЫТОГО ЧАТА
}

const user2_id = 1 // ID ПОЛЬЗОВАТЕЛЯ С КОТОРЫМ ОТКРЫТ ТЕКУЩИЙ ЧАТ
const ws = new WebSocket(`/chat/send/${user2_id}`)
ws.onmessage = function(event) {
    if (event.data == user2_id) {
        get_messages()
    }
}


async function send_message() {
    // ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ
    // ПОЛУЧИМ ТЕКСТ С ИНПУТА и тд.
    text = ''
    ws.send(text)
}