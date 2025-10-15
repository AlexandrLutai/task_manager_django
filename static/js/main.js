let accessToken = null;
const socket = new WebSocket("ws://127.0.0.1:8000/ws/tasks/");

socket.onopen = () => console.log("✅ WebSocket соединение установлено");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.event === "task_updated") {
    console.log("🔄 Обновление задач:", data.message);
    loadTasks();  // Повторная загрузка задач
  }
};

socket.onerror = (error) => {
  console.error("❌ WebSocket ошибка:", error);
};

function connectWebSocket() {
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const socketUrl = `${wsScheme}://${window.location.host}/ws/tasks/`;

  socket = new WebSocket(socketUrl);

  socket.onopen = () => {
    console.log("✅ WebSocket соединение установлено");
  };

  socket.onmessage = (event) => {
    const task = JSON.parse(event.data);
    console.log("📬 Обновление по задаче:", task);

    loadTasks();
  };

  socket.onclose = () => {
    console.log("⚠️ WebSocket отключён. Переподключение через 3 сек...");
    setTimeout(connectWebSocket, 3000);
  };

  socket.onerror = (error) => {
    console.error("❌ WebSocket ошибка:", error);
  };
}


async function loginUser() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/api/token/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  });

  const data = await response.json();

  if (response.ok) {
    accessToken = data.access;
    document.getElementById("login-ui").style.display = "none";
    document.getElementById("task-ui").style.display = "block";

    await loadTasks();
  } else {
    alert("Ошибка авторизации");
  }
}

async function loadTasks() {
  const response = await fetch("/api/my-tasks/", {
    headers: {
      "Authorization": `Bearer ${accessToken}`
    }
  });

  const tasks = await response.json();
  const list = document.getElementById("task-list");
  list.innerHTML = "";

  tasks.forEach(task => {
    const item = document.createElement("li");
    item.innerHTML = `${task.title} — до ${task.deadline} 
      ${task.completed ? "✅" : `<button onclick="completeTask(${task.id})">Выполнить</button>`}`;
    list.appendChild(item);
  });
}

async function completeTask(id) {
  await fetch(`/api/complete-task/${id}/`, {
    method: "PATCH",
    headers: {
      "Authorization": `Bearer ${accessToken}`
    }
  });
  loadTasks();
}

async function createTask() {
  const title = document.getElementById("title").value;
  const deadline = document.getElementById("deadline").value;

  if (!title || !deadline) {
    alert("Введите название и срок задачи");
    return;
  }

  const response = await fetch("/api/create-task/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      title,
      deadline,
      completed: false
     
    })
  });

  if (response.ok) {
    loadTasks();
    document.getElementById("title").value = '';
    document.getElementById("deadline").value = '';
  } else {
    const error = await response.json();
    alert("Ошибка при создании задачи: " + JSON.stringify(error));
  }
}

async function linkTelegram() {
  const telegramId = document.getElementById("telegram-id").value;

  const response = await fetch("/api/link-telegram/", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({telegram_id: telegramId})
  });

  const data = await response.json();

  if (response.ok) {
    alert("Telegram успешно привязан!");
  } else {
    alert("Ошибка: " + JSON.stringify(data));
  }
}



connectWebSocket();