const current_user_id = document.getElementById('current_user_id').value
const parts = window.location.href.split('/').slice(-1, -2)
const friend_id = parts[parts.length - 1]

const ws = new WebSocket(`/users/friend/add/${current_user_id}?friend_id=${friend_id}`)