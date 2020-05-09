var username = 'khai.nguyen@smiths-medical.com';
var api = 'cEM3kVmmC9m0YMZvgFvD1D2F';

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

const bodyData = `{
  "update": {},
  "fields": {
    "summary": "Main order flow broken",
    "issuetype": {
      "name": "Bug"
    },
    "project": {
      "key": "SAN"
    },
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Order entry fails when selecting supplier.",
              "type": "text"
            }
          ]
        }
      ]
    },
    "labels": [
      "bugfix",
      "blitz_test"
    ],
    "environment": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "UAT",
              "type": "text"
            }
          ]
        }
      ]
    }
  }
}`;

function sendTicketToJira() {
  var credential = username + ':' + api;
  console.log(btoa(credential.toString()));
  var proxyUrl = 'https://cors-anywhere.herokuapp.com/',
    targetUrl = 'https://smithsforge.atlassian.net/rest/api/3/issue'
  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Basic ` + btoa(credential.toString()),
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: bodyData
  };
  fetch(proxyUrl + targetUrl, options)
    .then(response => {
      console.log(
        `Response: ${response.status} ${response.statusText}`
      );
      return response.text();
    })
    .then(text => console.log(text))
    .catch(err => console.error(err));
}
