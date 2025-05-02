//Play requested sound
function playSound(soundFile) {
  fetch('/play', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
      body: JSON.stringify({ 'sound_file': soundFile }),
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

//Kill sound playing
function stopSound() {
  fetch('/stop', {
  method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

//Filter search results
function searchSound() {
  var input, filter, sounds, a, i, textValue, label;
  input = document.getElementById('search-box');
  filter = input.value.toUpperCase();
  sounds = document.getElementById('button-container');
  results = sounds.getElementsByTagName('button');
  label = document.getElementById('msg-label');

  let anyVisible = false;
  label.style.display = "none";
  for (i = 0; i < results.length; i++) {
    textValue = results[i].textContent || results[i].innnerText;
    if (textValue.toUpperCase().indexOf(filter) > -1) {
      results[i].style.display = "";
      anyVisible = true;
      label.style.display = "none";
	  } else {
	    results[i].style.display = "none";
    }
    if (!anyVisible) {
      label.style.display = "";
      label.innerHTML = "<br> No matching sounds found";
    }
  }
}
