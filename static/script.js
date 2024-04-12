const daysTag = document.querySelector(".days"),
currentDate = document.querySelector(".current-date"),
prevNextIcon = document.querySelectorAll(".icons span");
let selectedDate; 

let date = new Date(),
  currYear = date.getFullYear(),
  currMonth = date.getMonth();

// Storing full names of all months in an array
const months = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"];


    function updateEventList(events, clickedDate,selectedMonthYear1) {
    let eventListContainer = document.getElementById('event-list-container');
    let noEventsMsg = document.getElementById('no-events');

    if (!eventListContainer) {
        // Create the event list container if it doesn't exist
        eventListContainer = document.createElement('div');
        eventListContainer.id = 'event-list-container';
        eventListContainer.classList.add('event-list');
        document.body.appendChild(eventListContainer);
    }

    if (!noEventsMsg) {
        // Create the no events message if it doesn't exist
        noEventsMsg = document.createElement('div');
        noEventsMsg.id = 'no-events';
        noEventsMsg.classList.add('empty-message');
        noEventsMsg.style.display = 'none';
        noEventsMsg.textContent = 'No events for the selected date';
        eventListContainer.appendChild(noEventsMsg);
    }

    if (events.length > 0) {
        noEventsMsg.style.display = 'none';
        eventListContainer.innerHTML = events.map(event => `
            <div class="event">
                
                <strong>${clickedDate} ${selectedMonthYear1}</strong><br>
                <strong>${event.event_name}</strong><br>
                <span>Venue: ${event.hall_name}</span><br>
                <span>Time: ${event.start_time} - ${event.end_time}</span><br>
                <!-- Add more event details as needed -->
            </div>
        `).join('');
    } else {
        eventListContainer.innerHTML = 'No events';
        noEventsMsg.style.display = 'block';
    }
}
            
               
const handleDateClick = (event) => {
    
    const clickedDate = parseInt(event.target.innerText) + 1; // Increment the clicked date by 1
    // Get parsed integer value
    const selectedMonthYear1=currentDate.innerText
  const selectedMonthYear = currentDate.innerText.split(" "); // Split current date text
  console.log("abcd",selectedMonthYear1);


  // Validate and sanitize input (optional, but recommended)
  if (isNaN(clickedDate) || clickedDate < 1 || clickedDate > 31 || months.indexOf(selectedMonthYear[0]) === -1) {
    console.error("Invalid date selection. Please choose a valid date between 1 and 31.");
    return; // Prevent further processing
  }

  const selectedMonthIndex = months.indexOf(selectedMonthYear[0]); // Get month index
  const selectedDate = new Date(currYear, selectedMonthIndex, clickedDate);
  console.log("Selected Date:", clickedDate);
  
  document.querySelectorAll('.days li').forEach(day => {
    day.classList.remove('active');
  });

  // Add the 'active' class to the clicked date
  event.target.classList.add('active');

  // Send the selected date to the Flask route using Fetch API
  fetch('/fetch-events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ selectedDate: selectedDate.toISOString()}) // Convert to ISO string
  })
  .then(response => response.json())
  .then(data => {
    const clickedDate1 = parseInt(event.target.innerText);
    // Handle and display the received events data (e.g., update calendar or list)
    console.log("Fetched Events:", data.events);
    updateEventList(data.events,clickedDate1,selectedMonthYear1);
  })
  .catch(error => {
    console.error("Error fetching events:", error);
    // Handle errors gracefully (e.g., display an error message)
  });
};



const renderCalendar = () => {
  let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(),  // Get first day of month
      lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // Get last date of month
      lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // Get last day of month
      lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // Get last date of previous month

  let liTag = "";

  for (let i = firstDayofMonth; i > 0; i--) { // Create previous month's last days (inactive)
    liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
  }

  for (let i = 1; i <= lastDateofMonth; i++) { // Create current month's days
    let isToday = i === date.getDate() && currMonth === new Date().getMonth() && currYear === new Date().getFullYear() ? "active" : "";
    /* liTag += <li class="<span class="math-inline">\{isToday\}" onclick\="handleDateClick\(event\)"\></span>{i}</li>; // Add click event listener */
    liTag += `<li class="${isToday}" onclick="handleDateClick(event)">${i}</li>`;

  }

  for (let i = lastDayofMonth + 1; i <= 6; i++) { // Create next month's first days (inactive)
    liTag += `<li class="inactive">${i - lastDayofMonth}</li>`;
  }

  currentDate.innerText = `${months[currMonth]} ${currYear}`
  daysTag.innerHTML = liTag;
};

renderCalendar();
prevNextIcon.forEach(icon => { // getting prev and next icons
    icon.addEventListener("click", () => { // adding click event on both icons
        // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;

        if(currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
            // creating a new date of current year & month and pass it as date value
            date = new Date(currYear, currMonth, new Date().getDate());
            currYear = date.getFullYear(); // updating current year with new date year
            currMonth = date.getMonth(); // updating current month with new date month
        } else {
            date = new Date(); // pass the current date as date value
        }
        renderCalendar(); // calling renderCalendar function
    });
});
