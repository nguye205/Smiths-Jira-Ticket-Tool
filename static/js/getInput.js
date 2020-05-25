function FormValidation(inputToValidate) {
  console.log(inputToValidate.value);
  if (inputToValidate.value != "" && inputToValidate.value != "-") {
    console.log('valid');
    inputToValidate.style.boxShadow = "0 0 6px green, 0 0 2px";
  } else {
    console.log('invalid');
    inputToValidate.style.boxShadow = "0 0 6px red, 0 0 2px";
  }
}
