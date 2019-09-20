var channel_token = ""
var url = "https://api.line.me/v2/bot/message/reply"
var pushUrl = "https://api.line.me/v2/bot/message/push"

function doPost(e) {
  var json = e.postData.contents
  var events = JSON.parse(json).events;
  
  events.forEach(function(event) {
    if(event.type == "follow") {
      follow(event);
      followmsg(event);
    } 
    else if(event.type == "message") {
      if(event.message.type == "text") { oumu(event); }
    }
    else if(event.type == "unfollow") { unfollow(event); }
 });
}
/**メイン関数**/
function follow(e) {
  var userId = e.source.userId;
  var options = {"headers" : {"Authorization" : "Bearer " + channel_token}};
  var json = UrlFetchApp.fetch("https://api.line.me/v2/bot/profile/" + userId , options);
  var displayName = JSON.parse(json).displayName;
  var now = new Date();
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var ss = sheet.getSheetByName('user');
  ss.appendRow([userId, displayName, now]); 
  return displayName
}
function unfollow(e) {
  var userId = e.source.userId;
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var ss = sheet.getSheetByName('user');
  var dat = ss.getDataRange().getValues();
  var flg = -1;
  
  for(var i=0;i<dat.length;i++){
    if(dat[i][0] === userId){//[行][列]
      ss.deleteRow(i+1);
    }
  }
}
/**pushエンジン**/
function pushMsg(message) {
  var receivers = getReceivers()
  var data = {
  "replyToken" : e.replyToken,
  "messages" : [{
      "type": "text",
      "text" : "フォローありがとう！"
    },{
      "type": "sticker",
      "packageId": "11539",
      "stickerId": "52114131"
    }]};
  var options = headOption(data);
  
  UrlFetchApp.fetch(pushUrl, options);
}

/**定型msg**/
function followmsg(e) {
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
/**サブ関数**/
function getReceivers() {
//push配信をするユーザーを取得
}

function headOption(data) {
  var options = {
    "method" : "post",
    "headers" : {
      "Content-Type" : "application/json",
      "Authorization" : "Bearer " + channel_token
    },
    "payload" : JSON.stringify(data)
  };
}
