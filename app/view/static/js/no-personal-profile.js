const current_user_id = document.getElementById('current_user_id').value
const parts = window.location.href.split('/').slice(-1, -2)
const friend_id = parts[parts.length - 1]

const ws = new WebSocket(`/users/friend/add/${friend_id}?current_user_id=${current_user_id}`)