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
  var input, filter, sounds, results, a, i, textValue;
  input = document.getElementById('search-box');
  filter = input.value.toUpperCase();
  sounds = document.getElementById('button-container');
  results = sounds.getElementsByTagName('button');

  for (i = 0; i < results.length; i++) {
  textValue = results[i].textContent || results[i].innnerText;
  if (textValue.toUpperCase().indexOf(filter) > -1) {
    results[i].style.display = "";
	  } else {
	  results[i].style.display = "none";
	  }
  }
}
