function FormValidation(inputToValidate){
  console.log(inputToValidate.value);
  if (inputToValidate.value != ""){
    inputToValidate.style.borderColor = "green";
    inputToValidate.style.borderWidth = "thin";
  }
  else {
    inputToValidate.style.borderColor = "red";
    inputToValidate.style.borderWidth = "medium";
  }
}
