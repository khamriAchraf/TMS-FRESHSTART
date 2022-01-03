var myinput = document.querySelector('input[type="file"]');

function validateForm() {
  if (myinput.files.length == 0) {
    document.getElementById('submit').disabled=true;
  } else {
    document.getElementById('submit').disabled=false;
  }
}

myinput.addEventListener('change', validateForm);

