var channel_token = "見せられないよ"
var url = "https://api.line.me/v2/bot/message/reply"

function doPost(e) {
  var json = e.postData.contents
  var events = JSON.parse(json).events;
  
  events.forEach(function(event) {
    if(event.type == "follow") {
      follow(event);
    } 
    else if(event.type == "message"){
      if(event.message.type == "text"){
        oumu(event);
      }
    }
 });
}

function follow(e) {
  var message = {
    "replyToken" : e.replyToken,
    "messages" : [{
        "type": "text",
        "text" : "フォローありがとう！"
      },{
        "type": "sticker",
        "packageId": "11539",
        "stickerId": "52114131"
      }]};
  var options = {
    "method" : "post",
    "headers" : {
      "Content-Type" : "application/json",
      "Authorization" : "Bearer " + channel_token
    },
    "payload" : JSON.stringify(message)
  };
  UrlFetchApp.fetch(url, options);
}

function oumu(e) {
  var message = {
    "replyToken" : e.replyToken,
    "messages" : [{
        "type": "text",
        "text" : e.message.text + "\uDBC0\uDC39"
      }]};
  var options = {
    "method" : "post",
    "headers" : {
      "Content-Type" : "application/json",
      "Authorization" : "Bearer " + channel_token
    },
    "payload" : JSON.stringify(message)
  };
  UrlFetchApp.fetch(url, options);
}