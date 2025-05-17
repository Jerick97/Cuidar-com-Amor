document.addEventListener("DOMContentLoaded", function () {
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
});
