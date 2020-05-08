function FormValidation(inputToValidate){
  console.log(inputToValidate.value);
  if (inputToValidate.value != "" && inputToValidate.value != "-"){
    console.log('valid');
    inputToValidate.style.borderColor = "green";
    inputToValidate.style.borderWidth = "thin";
  }
  else {
    console.log('invalid');
    inputToValidate.style.borderColor = "red";
    inputToValidate.style.borderWidth = "medium";
  }
}
