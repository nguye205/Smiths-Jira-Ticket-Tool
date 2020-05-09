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
    "parent": {
      "key": "SAN"
    },
    "issuetype": {
      "id": "10000"
    },
    "components": [
      {
        "id": "10000"
      }
    ],
    "customfield_20000": "06/Jul/19 3:25 PM",
    "customfield_40000": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Occurs on all orders",
              "type": "text"
            }
          ]
        }
      ]
    },
    "customfield_70000": [
      "jira-administrators",
      "jira-software-users"
    ],
    "project": {
      "id": "10000"
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
    "reporter": {
      "id": "5b10a2844c20165700ede21g"
    },
    "fixVersions": [
      {
        "id": "10001"
      }
    ],
    "customfield_10000": "09/Jun/19",
    "priority": {
      "id": "20000"
    },
    "labels": [
      "bugfix",
      "blitz_test"
    ],
    "timetracking": {
      "remainingEstimate": "5",
      "originalEstimate": "10"
    },
    "customfield_30000": [
      "10000",
      "10002"
    ],
    "customfield_80000": {
      "value": "red"
    },
    "security": {
      "id": "10000"
    },
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
    },
    "versions": [
      {
        "id": "10000"
      }
    ],
    "duedate": "2019-05-11T00:00:00.000Z",
    "customfield_60000": "jira-software-users",
    "customfield_50000": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Could impact day-to-day work.",
              "type": "text"
            }
          ]
        }
      ]
    },
    "assignee": {
      "id": "5b109f2e9729b51b54dc274d"
    }
  }
}`;

function sendTicketToJira() {
  var credential = username + ':' + api;
  console.log(btoa(credential.toString()));

  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Basic `+btoa(credential.toString()),
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: bodyData
  };
  fetch('https://smithsfodddrge.atlassian.net/rest/api/3/issue', options);
}
