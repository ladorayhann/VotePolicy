let currentTab = 0;
showTab(currentTab)

function showTab(n) {
    // This function will display the specified tab of the form
    let tabs = document.getElementsByClassName('tab')
    tabs[n].style.display = "block"
    // fix the Previous/Next buttons:
    // if (n == 0) {
    //   document.getElementById("prev").style.display = "none";
    // } else {
    //   document.getElementById("prev").style.display = "inline";
    // }

    if (n == (tabs.length - 1)) {
      document.getElementById("next").innerHTML = "SUBMIT";
      
    } else {
      document.getElementById("next").innerHTML = "LANJUT";
    }
    updateStep(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    let tabs = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;


    // if you have reached the end of the form... :
    if (currentTab >= tabs.length) {
      //...the form gets submitted:
      document.getElementById("campaign-form").submit();
      return false;
    }
    // Hide the previous tab:
    tabs[currentTab-1].style.display = "none";
    // Otherwise, display the correct tab:
    showTab(currentTab);
  }

  function validateForm() {
    // This function deals with validation of the form fields
    let valid = true;
    switch(currentTab) {
      case 0:
        if (document.querySelectorAll('.input-radio:checked').length < 1) {
          valid = false
        }
        break;
      case 1:
      case 2:
        const tabs = document.getElementsByClassName('tab')
        const inputs = tabs[currentTab].getElementsByClassName('input-text')
        for (i =0; i < inputs.length; i++) {
          inputs[i].className = (inputs[i].value === '') ? 'input-text invalid': 'input-text'
          if (inputs[i].value === '') {
            valid = false;
            // restore classname onclick
            inputs[i].addEventListener('click',(e) => {e.currentTarget.className = 'input-text'})
          }
        }
        break;
      case 3:
        break;
    }

    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
      document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
  }

  function updateStep(n) {
    // This function removes the "active" class of all steps...
    let i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
      x[i].className = x[i].className.replace(" active", "");
      let desc = x[i].nextElementSibling
      x[i].nextElementSibling.style.display = "none";
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
    x[n].nextElementSibling.style.display = "block"
  }

  function showFile(e) {
    const fileName = e.target.files[0].name
    const inputFileName = document.querySelector('.input-file-name')
    const inputButton = document.querySelector('.input-button')
    inputFileName.textContent = fileName;
    inputFileName.style.display = 'block';
    inputButton.textContent = 'Ubah File'
  }

  document.querySelector('.input-file').addEventListener('change', (e) => {showFile(e)})
