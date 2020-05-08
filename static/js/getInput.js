var username;
var api = 'cEM3kVmmC9m0YMZvgFvD1D2F';

function FormValidation(inputToValidate){
  console.log(inputToValidate.value);
  if (inputToValidate.value != "" && inputToValidate.value != "-"){
    console.log('valid');
    inputToValidate.style.boxShadow = "0 0 6px green, 0 0 2px";
  }
  else {
    console.log('invalid');
    inputToValidate.style.boxShadow = "0 0 6px red, 0 0 2px";
  }
}



var searchNews = 'https://api.currentsapi.services/v1/search?' +
     'keywords=Apple&language=en&' +
     'apiKey=OIsqDsDGS2GagUTvcQ5V63nG6osMGg2zbKQbXn_QaWY71_7Z';

var latestNews = 'https://api.currentsapi.services/v1/latest-news?' +
     'apiKey=OIsqDsDGS2GagUTvcQ5V63nG6osMGg2zbKQbXn_QaWY71_7Z';

var jiraTicket = 'https://your-domain.atlassian.net/rest/api/3/issue/DEMO-1'

const myList = document.querySelector('#newsList');

async function postData() {
     fetch(searchNews)
          .then(response => response.json()) //get the response and convert to json object
          .then(data => {
               for (var i = 0; i < data.news.length; i++) {
                    //////////////////
                    var newsListItem = document.createElement('li');
                    var newsLink = document.createElement('a');
                    newsListItem.appendChild(newsLink); //add <a> tag to list
                    newsLink.appendChild(document.createTextNode(data.news[i].title)); //add text to the link
                    newsLink.title = JSON.stringify(data.news[i].title);
                    newsLink.href = JSON.stringify(data.news[i].url);

                    var newsPicture = document.createElement('img');
                    newsListItem.appendChild(newsPicture);
                    newsPicture.src = JSON.stringify(data.news[i].image);
                    newsPicture.alt = JSON.stringify(data.news[i].description);
                    myList.appendChild(newsListItem);
                    /////////
                    console.log(data.news[i].author);
               } //news for loop
               console.log(data);
          }); //then data
}
curl -u "username:password" http://device-name:port/rpc
-d "<get-interface-information/><get-software-information format='text/plain'/>"
—header "Accept: application/json"
window.onload = postData;
