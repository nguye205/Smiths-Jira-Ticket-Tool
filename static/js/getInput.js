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
////////////////////////////////////////////////////////////////////////////

var searchNews = 'https://api.currentsapi.services/v1/search?' +
     'keywords=Apple&language=en&' +
     'apiKey=OIsqDsDGS2GagUTvcQ5V63nG6osMGg2zbKQbXn_QaWY71_7Z';

var latestNews = 'https://api.currentsapi.services/v1/latest-news?' +
     'apiKey=OIsqDsDGS2GagUTvcQ5V63nG6osMGg2zbKQbXn_QaWY71_7Z';

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
window.onload = postData;
