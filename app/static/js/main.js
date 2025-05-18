document.addEventListener("DOMContentLoaded", async function () {
	// Initialize the calendar
	const calendarEl = document.getElementById("calendar");
	const calendar = new FullCalendar.Calendar(calendarEl, {
		initialView: "dayGridMonth",
		locale: "es",
		headerToolbar: {
			left: "prev",
			center: "title",
			right: "next",
		},
		fixedWeekCount: false,
		events: [
			{
				title: "Visita regular",
				start: "2025-05-21T16:30:00",
			},
			{
				title: "Cumpleaños abuela Isabel",
				start: "2025-05-23",
				allDay: true,
			},
		],
	});
	calendar.render();

	// Chatbot Emocional (Agente Emociones)
	const input = document.getElementById("chatInput");
	const sendBtn = document.getElementById("sendMessage");
	const chatContainer = document.getElementById("chatContainer");

	sendBtn.addEventListener("click", async () => {
		const mensaje = input.value.trim();
		if (!mensaje) return;

		// Mostrar el mensaje del usuario en el chat
		const userMsg = `
		<div class="d-flex justify-content-end align-items-start mb-3">
			<div class="bg-primary text-white rounded-3 p-3 shadow-sm text-start" style="max-width: 80%;">
				<small>${mensaje}</small>
			</div>
			<div class="rounded-circle bg-light p-2 ms-2" style="width: 32px; height: 32px;">
				<span class="fw-bold text-primary small d-block text-center">JR</span>
			</div>
		</div>`;
		chatContainer.insertAdjacentHTML("beforeend", userMsg);

		input.value = "";
		input.disabled = true;
		sendBtn.disabled = true;

		try {
			// ✅ Usar el nuevo endpoint del agente emociones
			const res = await fetch("/api/emociones", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ mensaje: mensaje }),
			});

			const data = await res.json();

			if (data.respuesta) {
				const botMsg = `
			<div class="d-flex align-items-start mb-3">
				<div class="rounded-circle bg-light p-2 me-2" style="width: 32px; height: 32px;">
					<i class="bi bi-robot text-primary"></i>
				</div>
				<div class="bg-light-subtle text-dark rounded-3 p-3 shadow-sm" style="max-width: 80%;">
					<small>${data.respuesta}</small>
				</div>
			</div>`;
				chatContainer.insertAdjacentHTML("beforeend", botMsg);
				chatContainer.scrollTop = chatContainer.scrollHeight;
			}
		} catch (err) {
			alert("Hubo un error al contactar con el agente emocional.");
			console.error(err);
		} finally {
			input.disabled = false;
			sendBtn.disabled = false;
		}
	});

	// Cargar historial del chat
	try {
		const usuario = "Jerick";
		const agente = "Emociones";
		const url = `/api/chat/historial?usuario=${usuario}&agente=${agente}`;
		const res = await fetch(url);
		const historial = await res.json();

		historial.forEach((msg) => {
			const userMsg = `
                <div class="d-flex justify-content-end align-items-start mb-3">
                    <div class="bg-primary text-white rounded-3 p-3 shadow-sm text-start" style="max-width: 80%;">
                        <small>${msg.mensaje_usuario}</small>
                    </div>
                    <div class="rounded-circle bg-light p-2 ms-2" style="width: 32px; height: 32px;">
                        <span class="fw-bold text-primary small d-block text-center">JR</span>
                    </div>
                </div>`;

			const botMsg = `
                <div class="d-flex align-items-start mb-3">
                    <div class="rounded-circle bg-light p-2 me-2" style="width: 32px; height: 32px;">
                        <i class="bi bi-robot text-primary"></i>
                    </div>
                    <div class="bg-light-subtle text-dark rounded-3 p-3 shadow-sm" style="max-width: 80%;">
                        <small>${msg.respuesta_gemini}</small>
                    </div>
                </div>`;

			chatContainer.insertAdjacentHTML("beforeend", userMsg);
			chatContainer.insertAdjacentHTML("beforeend", botMsg);
		});

		chatContainer.scrollTop = chatContainer.scrollHeight;
	} catch (err) {
		console.error("Error al cargar historial:", err);
	}
});
